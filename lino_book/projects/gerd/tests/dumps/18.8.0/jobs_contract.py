# -*- coding: UTF-8 -*-
logger.info("Loading 16 objects to table jobs_contract...")
# fields: id, signer1, signer2, user, company, contact_person, contact_role, printed_by, client, language, applies_from, applies_until, date_decided, date_issued, user_asd, exam_policy, ending, date_ended, duration, reference_person, responsibilities, remark, type, job, regime, schedule, hourly_rate, refund_rate
loader.save(create_jobs_contract(1,148,163,6,188,114,1,48,118,u'',date(2012,10,4),date(2013,10,3),None,None,None,3,None,date(2013,10,3),312,u'',None,u'',1,1,None,None,None,u''))
loader.save(create_jobs_contract(2,148,163,6,189,None,None,49,126,u'',date(2012,10,14),date(2014,4,13),None,None,None,3,None,date(2014,4,13),480,u'',None,u'',4,5,None,None,None,u''))
loader.save(create_jobs_contract(3,148,163,6,189,None,None,50,130,u'',date(2012,11,3),date(2013,11,2),None,None,None,3,None,date(2013,11,2),312,u'',None,u'',2,2,None,None,None,u''))
loader.save(create_jobs_contract(4,148,163,5,191,115,1,51,130,u'',date(2013,11,3),date(2014,11,3),None,None,None,3,None,date(2014,11,3),480,u'',None,u'',1,6,None,None,None,u''))
loader.save(create_jobs_contract(5,148,163,6,191,115,1,52,133,u'',date(2012,11,13),date(2014,11,12),None,None,None,3,None,date(2014,11,12),624,u'',None,u'',5,3,None,None,None,u''))
loader.save(create_jobs_contract(6,148,163,6,188,114,1,53,142,u'',date(2012,12,3),date(2014,12,2),None,None,None,3,None,date(2014,12,2),624,u'',None,u'',2,7,None,None,None,u''))
loader.save(create_jobs_contract(7,148,163,6,188,114,1,54,146,u'',date(2012,12,13),date(2013,12,12),None,None,None,3,None,date(2013,12,12),312,u'',None,u'',3,4,None,None,None,u''))
loader.save(create_jobs_contract(8,148,163,4,189,None,None,55,146,u'',date(2013,12,13),date(2014,12,13),None,None,None,3,None,date(2014,12,13),480,u'',None,u'',5,8,None,None,None,u''))
loader.save(create_jobs_contract(9,148,163,6,188,114,1,56,155,u'',date(2013,1,2),date(2014,1,1),None,None,None,3,None,date(2014,1,1),312,u'',None,u'',1,1,None,None,None,u''))
loader.save(create_jobs_contract(10,148,163,4,189,None,None,57,155,u'',date(2014,1,2),date(2015,1,2),None,None,None,3,None,date(2015,1,2),480,u'',None,u'',4,5,None,None,None,u''))
loader.save(create_jobs_contract(11,148,163,6,189,None,None,58,158,u'',date(2013,1,12),date(2015,1,11),None,None,None,3,None,date(2015,1,11),624,u'',None,u'',2,2,None,None,None,u''))
loader.save(create_jobs_contract(12,148,163,6,191,115,1,59,166,u'',date(2013,2,1),date(2015,1,31),None,None,None,3,None,date(2015,1,31),624,u'',None,u'',1,6,None,None,None,u''))
loader.save(create_jobs_contract(13,148,163,4,191,115,1,60,173,u'',date(2013,2,11),date(2014,2,10),None,None,None,3,None,date(2014,2,10),312,u'',None,u'',5,3,None,None,None,u''))
loader.save(create_jobs_contract(14,148,163,5,188,114,1,61,173,u'',date(2014,2,11),date(2015,2,11),None,None,None,3,None,date(2015,2,11),480,u'',None,u'',2,7,None,None,None,u''))
loader.save(create_jobs_contract(15,148,163,6,188,114,1,62,180,u'',date(2013,3,3),date(2014,3,2),None,None,None,3,None,date(2014,3,2),312,u'',None,u'',3,4,None,None,None,u''))
loader.save(create_jobs_contract(16,148,163,5,189,None,None,63,180,u'',date(2014,3,3),date(2015,3,3),None,None,None,3,None,date(2015,3,3),480,u'',None,u'',5,8,None,None,None,u''))

loader.flush_deferred_objects()
