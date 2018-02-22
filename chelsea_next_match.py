import requests
import bs4
from datetime import datetime
from dateutil import tz
import chelsea_mail_sender
import logging

# match_date_text format is '01:15, Wed 21 Feb' and it is GMT, so we need to convert it to local time
# and also it needs a year, refer the testing file for explanation on how we are adding the year to it
def time_conversion(match_date_text,teams_text):
	# Auto-detect zones:
	from_zone = tz.gettz('GMT') 
	to_zone = tz.tzlocal()

	gmt_match_time = datetime.strptime(match_date_text, '%H:%M, %a %d %b')

	# Tell the datetime object that it's in UTC time zone since 
	# datetime objects are 'naive' by default
	gmt_match_time = gmt_match_time.replace(tzinfo=from_zone)

	# Convert time zone
	local_match_time = gmt_match_time.astimezone(to_zone)

	formatted_time = 'Time - ' +local_match_time.strftime('%H %M, %a %d %b')

	year = int(datetime.now().strftime('%Y'))

	if local_match_time.strftime('%b') == 'Jan' and datetime.now().strftime('%b') == 'Dec':
		year = year + 1;

	match_time = datetime(
		year,
		int(local_match_time.strftime('%m')),
		int(local_match_time.strftime('%d')),
		int(local_match_time.strftime('%H')),
		int(local_match_time.strftime('%M')),
		0,0)

	now = datetime.now()

	#finding diffference between the next match time and current time

	diff = match_time - now

	days, seconds = diff.days, diff.seconds
	hours_diff = days * 24 + seconds // 3600

	print(formatted_time)
	print(teams_text)
	
	if hours_diff <= 12:
		chelsea_mail_sender.send_email(formatted_time,teams_text)
	else:
		print("Not need to send alert, remaining hours are " + str(hours_diff))


def get_match_details():

	try:
		resp = requests.get('https://www.chelseafc.com/matches/fixtures---results.html')
		resp.raise_for_status()
		soup = bs4.BeautifulSoup(resp.text,"html.parser")
		next_match_date = soup.select('.next-match .header span')
		match_date_text = next_match_date[0].getText()[2:]
		teams = soup.select('.next-match p')
		teams_text = teams[0].get_text(" ", strip=True)
		teams_text = 'Teams - ' +teams_text

		time_conversion(match_date_text,teams_text)
	except Exception as e:
		print e.__doc__
		print e.message
	
get_match_details()

