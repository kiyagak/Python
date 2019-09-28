'''
	Name:		Kuteesa Kiyaga
	Date: 		September 28, 2019
	Function:	Convert date strings into a uniform date format.  
'''

# import modules
from datetime import datetime, timedelta, date
import time

# declare function
# taking the string containing the date string
# and the format of the date
def reformat(dateStr, refmtStr):
	# if the the date string is a string type
	if type(dateStr) == str:
		# convert the date string to all lowercase
		dateStr = dateStr.lower()
	
	# string variables for various time metrics
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
	
	
	
	# initialize variable to determine if the date string 
	# is Unix/epoch timestamp
	epochBool = None
	
	# # initialize boolean variable to determine if the date string 
	# contains a time metric within its date string
	# i.e. 2 hours ago, 4 weeks ago, 1 year ago, etc.
	dateMetricBool = None
	
	# if the date string parameter is an integer type
	if type(dateStr) == int:
		# set the epoch boolean to check if
		# the date string is an integer type
		# and its lengths is between ten and thirteen digits
		epochBool = (type(dateStr) == int) and (len(str(dateStr)) >= 10 and len(str(dateStr)) <= 13)
	# otherwise
	else:
		# set the time metric boolean to check if
		# the date string parameter contains a time metric string,
		# such as min, hour, week, year, etc.
		dateMetricBool = (sec in dateStr) or (min in dateStr) or (hour in dateStr) or (hr in dateStr) or (day in dateStr) or (week in dateStr) or (month in dateStr) or (year in dateStr)
	
	
	# variable containing the format to convert the date string
	# parameter to YYYY-MM-DD format, i.e. 2019-09-27
	dateFormat = "%Y-%m-%d"
	
	# initialize a variable that will store the date string
	# formatted in YYYY-MM-DD format
	pubDate = None
	
	# variable containing today's date
	cal = datetime.now().date()
	
	
	
	# if the date string parameter is an Epoch/Unix time
	if epochBool:
		# variable containing the Unix/Epoch time date string
		epoch = dateStr
		
		# if the length of the date string parameter is 13
		if len(str(dateStr)) == 13:
			# divide the date string integer by 1000
			epoch = int(dateStr / 1000)
		
		# convert the Epoch/Unix time into YYYY-MM-DD format
		pubDate = time.strftime("%Y-%m-%d", time.localtime(epoch))
	
	# or if the date string parameter contains a time metric string
	elif (dateMetricBool):
		# set the date string parameter to all lower case
		dateStr = dateStr.lower();
		# initialize a variable to store the numeric value associated
		# with the time metric
		prevInt = None;
		
		# if the date string contains "sec"
		if sec in dateStr:
			# variable storing the second's numeric value
			prevInt = int(dateStr.split(" " + sec)[0]);
			# set today's date to the date minus prevInt's seconds 
			cal = cal - timedelta(seconds=prevInt)
		# if the date string contains "min"
		elif min in dateStr:
			# variable storing the minute's numeric value
			prevInt = int(dateStr.split(" " + min)[0])
			# set today's date to the date minus pevInt's minutes 
			cal = cal - timedelta(minutes=prevInt)
		# if the date string contains "an hour"
		elif anHour in dateStr:
			# set today's date to the date minus one hour
			cal = cal - timedelta(hours=1)
		# if the date string contains "hr"
		elif (hr) in dateStr:
			# variable storing the hour's numeric value
			prevInt = int(dateStr.split(" " + hr)[0])
			# set today's date to the date minus prevInt's hours 
			cal = cal - timedelta(hours=prevInt)
		# if the date string contains "hour"
		elif hour in dateStr:
			# variable storing the hour's numeric value
			prevInt = int(dateStr.split(" " + hour)[0])
			# set today's date to the date minus prevInt's hours
			cal = cal - timedelta(hours=prevInt)
		# if the date string contains "day"
		# without containing "yesterday"
		elif (day in dateStr) and ("yesterday" not in dateStr):
			# variable storing the day's numeric value
			prevInt = int(dateStr.split(" " + day)[0])
			# set today's date to the date minus prevInt's days
			cal = cal - timedelta(days=prevInt)
		# if the date string contains "yesterday"
		elif yesterday in dateStr:
			# set today's date to the date minus one day
			cal = cal - timedelta(days=1)
		# if the date string contains "week"
		elif week in dateStr:
			# variable storing the week's numeric value
			prevInt = int(dateStr.split(" " + week)[0])
			# set today's date to the date minus prevInt's weeks
			cal = cal - timedelta(weeks=prevInt)
		# if the date string contains "month"
		elif month in dateStr:
			# variable storing the month's numeric value
			prevInt = int(dateStr.split(" " + month)[0])
			# set today's date to the date minus prevInt's months
			cal = date.today().replace(month=date.today().timetuple()[1] - prevInt)
		# if the date string contains "year"
		elif year in dateStr:
			# variable storing the year's numeric value
			prevInt = int(dateStr.split(" " + year)[0])
			# set today's date to the date minus prevInt's year
			cal = date.today().replace(year=date.today().timetuple()[0] - prevInt)
		
		# if the altered date is a datetime type
		if type(cal) is datetime:
			# reformat the altered date to YYYY-MM-DD
			cal = cal.strftime(dateFormat)
		
		# assign the altered, formatted date to pubDate
		pubDate = cal
	
	# otherwise
	else:
		# convert the date string parameter to the
		# standard datetime format
		# then convert it to YYYY-MM-DD format
		pubDate = datetime.strptime(dateStr, refmtStr).date().strftime(dateFormat)
	
	# assign the reformatted date to a variable
	pubDate = datetime.strptime(str(pubDate), "%Y-%m-%d").date()
	# return the date in YYYY-MM-DD format
	return pubDate
	

# execute the function using various date format
print(reformat(1533754439, ""))
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