.. doctest docs/specs/invoicing.rst
.. _xl.specs.invoicing:
.. _cosi.specs.invoicing:

======================================
``invoicing`` : Generating invoices
======================================

.. currentmodule:: lino_xl.lib.invoicing

The :mod:`lino_xl.lib.invoicing` plugin adds functionality for
**invoicing**, i.e. automatically generating invoices from data in the
database.

This document describes some general aspects of invoicing and how
applications can handle this topic.  You should have read :doc:`sales`
and :doc:`accounting`.  See also
:doc:`/specs/voga/invoicing` and
:doc:`/specs/tera/invoicing`.


.. contents::
   :depth: 1
   :local:

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_book.projects.roger.settings.demo')
>>> from lino.api.doctest import *
>>> ses = rt.login("robin")
>>> translation.activate('en')

Overview
========

As an application developer you define **invoice generators** by
having one or several models of your application inherit from
:class:`InvoiceGenerator`.


API
===

On the API level it defines the :class:`InvoiceGenerator
<lino_xl.lib.invoicing.InvoiceGenerator>` mixin.

This plugin requires the :mod:`lino_xl.lib.sales` plugin.

>>> dd.plugins.invoicing.needs_plugins
['lino_xl.lib.sales']

The plugin adds a main menu command :menuselection:`Sales --> Create invoices`:

>>> show_menu_path(invoicing.Plan.start_plan)
Sales --> Create invoices





The ``InvoiceGenerator`` model mixin
====================================


.. class:: InvoiceGenerator

    Mixin for things that can generate invoices.

    An invoice generator must produce a series of **invoiceable events** (the
    :term:`application developer` must implement a method :meth:`get_invoiceable_events`).
    These events can be instances of any model, but the generator's
    :meth:`get_invoiceable_event_formatter` must understand them.

    Methods and class attributes:

    .. attribute:: default_invoiceable_qty

        The default value to return by :meth:`get_invoiceable_qty`.

    .. method:: get_invoice_items(self, info, invoice, ar)

        Yield one or several invoice items generated by this object.

        These must be instances of :class:`lino_xl.lib.sales.InvoiceItem`.

    .. method:: get_invoiceable_events(self, start_date, max_date)

        Return a Django query that represents the *invoiceable events*.

        The query must be sorted in the order they are to be considered for
        invoicing.

    .. method:: get_invoiceable_event_formatter(self)

        Return a callable which formats an *invoiceable event* as a HTML etree
        element.

    .. method:: get_invoiceables_for_plan(cls, plan, partner=None)

        Yield a sequence of invoiceable candidates (objects of this
        class) for the given plan.  If a `partner` is given, use it as
        an additional filter condition.

        Not every yielded candidate will become an invoice.  This is a
        pre-selection.  For every candidate Lino will call
        :meth:`get_invoiceable_product`

    .. method:: get_invoiceable_product(self, plan)

      To be implemented by subclasses.  Return the product to put
      into the invoice item.

      >>> obj = rt.models.courses.Enrolment.objects.all()[0]
      >>> print(obj.get_invoiceable_product())
      Journeys

    .. method:: get_invoiceable_qty(self)

      Return the quantity to use for each generated invoice item.

      May be overridden by subclasses.
      The default implementation simply returns :attr:`default_invoiceable_qty`.

      >>> obj = rt.models.courses.Enrolment.objects.all()[0]
      >>> print(obj.get_invoiceable_qty())
      1

    .. method:: get_invoiceable_title(self, invoice=None)

      Return the title to put into the invoice item.

      May be overridden by subclasses.

    .. attribute:: invoicings

        A simple `GenericRelation
        <https://docs.djangoproject.com/ja/1.9/ref/contrib/contenttypes/#reverse-generic-relations>`_
        to all invoice items pointing to this enrolment.

        This is preferred over :meth:`get_invoicings`.

    .. method:: get_invoicings(**kwargs)

        Get a queryset with the invoicings which point to this
        enrolment.

        This is deprecated. Preferred way is to use
        :attr:`invoicings`.

    .. method:: get_last_invoicing()

        Return the last invoicing that was created by this generator.
        According to the invoice's :attr:`voucher_date
        <lino_xl.lib.ledger.Voucher.voucher_date>`.


.. class:: InvoicingInfo

    A volatile object which holds cached information about a given invoice
    generator.

    .. attribute:: generator

        The invoice generator this is about.

    .. attribute:: max_date

        The latest date of events considered when computing this.

    .. attribute:: invoicings

        Existing invoice items generated by this generator for earlier
        periods.

    .. attribute:: invoiced_qty

        Sum of quantities invoiced earlier.

    .. attribute:: invoiced_events

        Number of events invoiced earlier.

    .. attribute:: used_events

        A list of the "events" used for computing this.

    .. attribute:: invoiceable_product

        Which fee to apply. If this is `None`, no invoicing should get
        generated.



Sales rules
===========

Every partner can have a sales rule.

.. class:: SalesRule

    The Django model used to represent a *sales rule*.

    .. attribute:: partner

        The partner to which this sales rule applies.

    .. attribute:: invoice_recipient

        The partner who should get the invoices caused by this partner.

    .. attribute:: paper_type

        The default paper type to be used for invoicing.


>>> fld = rt.models.invoicing.SalesRule._meta.get_field('invoice_recipient')
>>> print(fld.help_text)
The partner who should get the invoices caused by this partner.




.. class:: SalesRules



Flatrates
=========

Every product can have a **flatrate**.

.. class:: Tariff

    The Django model used to represent a *flatrate*.

    .. attribute:: number_of_events

        Number of calendar events paid per invoicing.

    .. attribute:: min_asset

        Minimum quantity required to trigger an invoice.




The invoicing plan
==================

.. class:: Plan

    The Django model used to represent an *invoicing plan*.

    An **invoicing plan** is a rather temporary database object which
    represents the plan of a given user to have Lino generate a series
    of invoices.

    It inherits from :class:`lino.modlib.users.UserPlan`.

    .. attribute:: user

         The user who manages this plan.

    .. attribute:: journal

        No longer exists. Replaced by :attr:`area`.

    .. attribute:: area

        The *invoicing area* of this plan.

        A pointer to :class:`Area`.

    .. attribute:: today

         This invoice date to be used for the invoices to generate.

    .. attribute:: max_date

        Don't invoice events after this date.  If this is empty, Lino will
        use the day before the invoice date.

    .. attribute:: partner

    .. attribute:: update_plan

        Update this plan (fill the list of suggestions).

    .. attribute:: execute_plan

        Execute this plan (create an invoice for each selected suggestion).

    .. method:: start_plan(user, **options)

        Start an invoicing plan for the given `user` on the database
        object defined by `k` and `v`. Where `k` is the name of the
        field used to select the plan (e.g. `'partner'` or
        `'journal'`) and `v` is the value for that field.

        This will either create a new plan, or check whether the
        currently existing plan for this user was for the same
        database object. If it was for another object, then clear all
        items.

    .. method:: fill_plan(ar)

        Add items to this plan, one for each invoice to generate.

        This also groups the invoiceables by their invoiceable
        partner.

        Note a case we had (20171007) : One enrolment for Alfons whose
        invoice_recipient points to Erna, a second enrolment for Erna
        directly. The first enrolment returned Erna as Partner, the
        second returned Erna as Pupil, so they were not grouped.

.. class:: Item

    The Django model used to represent a *item* of an *invoicing plan*.

    The items of an invoicing plan are called **suggestions**.

    .. attribute:: plan
    .. attribute:: partner
    .. attribute:: preview

        A textual preview of the invoiceable items to be included in
        the invoice.


    .. attribute:: amount
    .. attribute:: invoice

        The invoice that has been generated. This field is empty for
        new items. When an item has been executed, this field points
        to the generated invoice.

    .. attribute:: workflow_buttons

    The following fields are maybe not important:

    .. attribute:: first_date
    .. attribute:: last_date
    .. attribute:: number_of_invoiceables

    .. method:: create_invoice(ar):

        Create the invoice corresponding to this item of the plan.


.. class:: Plans
.. class:: MyPlans
.. class:: AllPlans
.. class:: Items
.. class:: ItemsByPlan
.. class:: InvoicingsByInvoiceable

.. class:: StartInvoicing

    Start an *invoicing plan* for the authenticated user.

    Base for :class:`StartInvoicingForPartner`.

    Inherits from :class:`lino.modlib.users.StartPlan` and just
    overrides the label.

.. class:: StartInvoicingByArea

    Start an invoicing plan for this area.

    This is installed onto the VouchersByJournal table of the
    VoucherType for the configured :attr:`voucher_model
    <lino_xl.lib.invoicing.Plugin.voucher_model>` as
    `start_invoicing`.


.. class:: StartInvoicingForPartner

    Start an invoicing plan for this partner.

    This is installed onto the :class:`contacts.Partner
    <lino_xl.lib.contacts.Partner>` model as `start_invoicing`.


.. class:: ExecutePlan

   Execute this invoicing plan.
   Create an invoice for each selected suggestion.


.. class:: ExecuteItem

    Create an invoice for this suggestion.

.. class:: ToggleSelection

    Invert selection status for all suggestions.


Invoicing areas
===============

An **invoicing area** is is used to classify business activities into different
parts for which end users can start separate invoicing plans.

This is used in :ref:`presto` to differentiate between activities for which
invoicing is often run manually based on occasional work from those that are invoiced
monthly automatically based on regular work.
In :ref:`tera` they might get used to
separate the therapy centres in different towns.

The application is responsible for selecting only invoiceables that belong to
the area of the current plan. For example :ref:`presto` does this by defining a
field :attr:`lino_presto.lib.cal.Room.invoicing_area`.

>>> rt.show(invoicing.Areas)
===== ============= ================== ================== ======================
 No.   Designation   Designation (de)   Designation (fr)   Journal
----- ------------- ------------------ ------------------ ----------------------
 1     First         Erster             Premier            Sales invoices (SLS)
===== ============= ================== ================== ======================
<BLANKLINE>


.. class:: Area

    The Django model used to represent a *flatrate*.

    .. attribute:: journal

        The journal into which invoices are to be generated.



Manually editing automatically generated invoices
=================================================

Resetting title and description of a generated invoice item
===========================================================

When the user sets `title` of an automatically generated invoice
item to an empty string, then Lino restores the default value for
both title and description
