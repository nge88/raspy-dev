import calendar
import time
import pytz
import datetime as dt

tz1 = pytz.timezone('Europe/Rome')
utc = pytz.timezone('UTC')
now = utc.localize(dt.datetime.utcnow())
now_tz = now.astimezone(tz1)

now_epoch = calendar.timegm(now_tz.utctimetuple())

print(now_tz)
print(now_epoch)
# 2012-08-28 14:33:50.480725-05:00
# 1346182430

begin_day = now_tz.replace(hour=0, minute=0, second=0)
begin_epoch = calendar.timegm(begin_day.utctimetuple())

print(begin_day)
print(begin_epoch)
# 2012-08-28 00:00:00.480725-05:00
# 1346130000
