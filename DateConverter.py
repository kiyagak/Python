from datetime import datetime, timedelta, date
import time

def reformat(dateStr, refmtStr):
	if type(dateStr) == str:
		dateStr = dateStr.lower()
	
	sec = "sec"
	min = "min"
	hour = "hour"
	anHour = "an hour"
	hr = "hr"
	day = "day"
	yesterday = "yesterday"
	week = "week"
	month = "month"
	year = "year"
	
	
	
	epochBool = None
	dateMetricBool = None
	dateHasStrBool = None
	
	if type(dateStr) == int:
		epochBool = (type(dateStr) == int) and (len(str(dateStr)) >= 10 and len(str(dateStr)) <= 13)
	else:
		dateMetricBool = (sec in dateStr) or (min in dateStr) or (hour in dateStr) or (hr in dateStr) or (day in dateStr) or (week in dateStr) or (month in dateStr) or (year in dateStr)
	
	
	
	dateParseForm = None
	dateFormat = "%Y-%m-%d"
	dateParse = None
	pubDate = None
	
	cal = datetime.now().date()
	
	
	
	if epochBool:
		epoch = dateStr
		
		if len(str(dateStr)) == 13:
			epoch = int(dateStr / 1000)
		
		pubDate = time.strftime("%Y-%m-%d", time.localtime(epoch))
	
	elif (dateMetricBool):
		dateStr = dateStr.lower();
		prevInt = None;
		
		if sec in dateStr:
			prevInt = int(dateStr.split(" " + sec)[0]);
			cal = cal - timedelta(seconds=prevInt)
		elif min in dateStr:
			prevInt = int(dateStr.split(" " + min)[0])
			cal = cal - timedelta(minutes=prevInt)
		elif anHour in dateStr:
			cal = cal - timedelta(hours=1)
		elif (hr) in dateStr:
			prevInt = int(dateStr.split(" " + hr)[0])
			cal = cal - timedelta(hours=prevInt)
		elif hour in dateStr:
			prevInt = int(dateStr.split(" " + hour)[0])
			cal = cal - timedelta(hours=prevInt)
		elif (day in dateStr) and ("yesterday" not in dateStr):
			prevInt = int(dateStr.split(" " + day)[0])
			cal = cal - timedelta(days=prevInt)
		elif yesterday in dateStr:
			cal = cal - timedelta(days=1)
		elif week in dateStr:
			prevInt = int(dateStr.split(" " + week)[0])
			cal = cal - timedelta(weeks=prevInt)
		elif month in dateStr:
			prevInt = int(dateStr.split(" " + month)[0])
			cal = date.today().replace(month=date.today().timetuple()[1] - prevInt)
		elif year in dateStr:
			prevInt = int(dateStr.split(" " + year)[0])
			cal = date.today().replace(year=date.today().timetuple()[0] - prevInt)
		
		if type(cal) is datetime:
			cal = cal.strftime(dateFormat)
			
		pubDate = cal
	
	else:
		pubDate = datetime.strptime(dateStr, refmtStr).date().strftime(dateFormat)
	
	
	pubDate = datetime.strptime(str(pubDate), "%Y-%m-%d").date()
	return pubDate
	

print(type(reformat(1533754439, "")))
print(reformat('December 18, 2006', '%B %d, %Y'))
print(reformat('09-12-2018', '%m-%d-%Y'))
print(reformat('2 seconds ago', ""))
print(reformat('8 minutes ago', ""))
print(reformat('an hour ago', ""))
print(reformat('yesterday', ""))
print(reformat('2 months ago', ""))
print(reformat('3 weeks ago', ""))
print(reformat('3 years ago', ""))
print(reformat(1533754439505, ""))
