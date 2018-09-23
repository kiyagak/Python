import urllib.request, json, time, datetime, threading, calendar
from datetime import date, timedelta



def last_rel_date():
	today = date.today()
	day_of_week = calendar.day_name[today.weekday()]
	prevDate = today
	breakDate = None

	for day in range(8):
		if (calendar.day_name[today.weekday() - day] == "Friday"):
			prevDate = today - timedelta(days=day)
			break
	
	return prevDate