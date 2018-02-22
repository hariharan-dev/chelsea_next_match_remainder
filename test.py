import requests
import bs4
from datetime import datetime
from dateutil import tz


# since we dont get year details from the match details, we manually attach the current date`s year 
# to next match year, but there is a edge case in this which needs to be handled.
# which is when the next match is happening in jan of next year but we are still in dec of current year,
# since we assign the date current date`s year to next match`s year, this will produce the wrong result for this case,
# on when the next match`s month is jan, and current date`s month is december, we manually increment the year by 1
# and attach it to the next match` year

def time_conversion(match_date_text):

	# Auto-detect zones:
	from_zone = tz.gettz('GMT') 
	to_zone = tz.tzlocal()

	gmt_match_time = datetime.strptime(match_date_text, '%H:%M, %a %d %b')

	# Tell the datetime object that it's in UTC time zone since 
	# datetime objects are 'naive' by default
	gmt_match_time = gmt_match_time.replace(tzinfo=from_zone)

	# Convert time zone

	local_match_time = gmt_match_time.astimezone(to_zone)

	print(local_match_time.strftime('%H %M, %a %d %b'));

	now = datetime(
		int('2018'),
		int('12'),
		int('31'),
		int('01'),
		int('15'),
		0,0)

	print(now.strftime('%H %M, %a %d %b'))

	year = int(now.strftime('%Y'))

	if local_match_time.strftime('%b') == 'Jan' and now.strftime('%b') == 'Dec':
		year = year + 1
		print('year incremented')

	match_time = datetime(
		year,
		int(local_match_time.strftime('%m')),
		int(local_match_time.strftime('%d')),
		int(local_match_time.strftime('%H')),
		int(local_match_time.strftime('%M')),
		0,0)

	diff = match_time - now

	days, seconds = diff.days, diff.seconds
	hours = days * 24 + seconds // 3600

	#hours should be 48
	
	print(hours)

time_conversion('19:45, Tue 1 Jan');
