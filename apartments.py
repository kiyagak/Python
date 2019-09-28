'''	Name:		Kuteesa Kiyaga
	Date:		June 30, 2019
	Function:	Scrape Kijiji for processor advertisements.  
'''

# import modules
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from multiprocessing import Process, freeze_support, Manager
import re, urllib.parse, json

# declare a function that scrapes Kijiji for advertisements
# for processors found in the URL array
# function takes radius in kilometers as a parameter
def kijiji_scrape(radius):
	# if the radius is not a float type
	if (type(radius) != float) and (type(radius) != int):
		# print that an incorrect, non-numeric parameter was passed
		print('You have entered an invalid parameter.  Please enter a number and try again.  ')
	else:
		# initialize a JSON object
		json_object = {}
		# JSON object key to store an array information about
		# the listed ads for a processor
		json_object['kijiji_ads'] = []
		
		# cast the radius parameter as a float datatype
		radius = float(radius)
		
		# variable containing the page number
		a = 0
		
		# create an infinite loop
		while True:
			# increment the page number
			a += 1
			
			# variable storing a URL to a Kijiji search for the processor
			url = 'https://www.kijiji.ca/b-for-rent/brantford/page-' + str(a) + '/c30349001l1700206r' + str(radius) + '?sort=priceAsc&ad=offering'
			
			# variable storing the HTML contents of the Kijiji search page
			# after connecting to it
			main_con = BeautifulSoup(urlopen(Request(url)).read().decode(), 'html.parser').select('div.regular-ad')
			# variable containing the HTML element for the next page button
			next_page = BeautifulSoup(urlopen(Request(url)).read().decode(), 'html.parser').select('div.pagination a[title=\"Next\"]')
			
			# if there are one or more advertisements
			if (len(main_con) != 0):
				# iterate through the advertisements
				for post in range(len(main_con)):
					# if ad's element has the data-third-party-id attribute
					# and the ad's element is not empty
					if (main_con[post].has_attr('data-third-party-id') == False):
						# initiate a JSON object for information about the ad
						result_object = {}
						
						# variable to store strings to be
						# part of a regular expression
						rgx_terms = '-storage-parking|-commercial-office-space'
						
						# if the ad's URL doesn't contain "-storage-parking"
						# or "-commercial-office-space"
						if len(re.split(rgx_terms, main_con[post].select('div.info div.title a.title')[0]['href'])) < 2:
							# try
							try:
								# store the ad's price in the JSON object's price key
								# cast as a float data type
								result_object['price'] = float(main_con[post].select('div.info div.price')[0].text.replace('$', '').replace('\n', '').replace(' ', '').replace(',', ''))
							# if casting is attempted on alphabetical characters
							except ValueError:
								# store the value zero in the JSON object's price key
								result_object['price'] = 0.0
							# store the ad's title in the JSON object's title key
							result_object['title'] = main_con[post].select('div.info div.title')[0].text.replace('\n', '').replace('  ', '')
							# store the ad's URL in the JSON object's ad_url key
							result_object['ad_url'] = 'https://www.kijiji.ca' + '/'.join(main_con[post].select('div.info div.title a.title')[0]['href'].split('/', 5)[0:5])
							# store the ad's distance in the JSON object's distance key
							result_object['distance'] = main_con[post].select('div.info div.distance')[0].text.replace('\n', '').replace('  ', '')
							# store the ad's location in the JSON object's location key
							result_object['location'] = main_con[post].select('div.info div.location')[0].text.replace('\n', '').replace('  ', '')
							# store the ad's description in the JSON object's description key
							result_object['description'] = main_con[post].select('div.info div.description')[0].text.replace('\n', ' ').replace('  ', '')
							# store the query's page in the JSON object's page key
							result_object['page'] = a
							
							# add the ad's JSON object to the kijiji_ads key
							json_object['kijiji_ads'].append(result_object)
			
			# if the next_page HTML element is empty
			if (len(next_page) == 0):
				# stop the infinite loop
				break
				
		# variable containing a sorted JSON object
		# sorted based on lowest price
		sorted_object = {'kijiji_ads': sorted(json_object['kijiji_ads'], key=lambda x : x['price'])}
		
		# return the JSON object
		return sorted_object
				
# print the function
print(json.dumps(kijiji_scrape(12), indent=4))
