'''	Name:		Kuteesa Kiyaga
	Date:		June 30, 2019
	Function:	Concurrently scrape Kijiji for processor advertisements.  
'''

# import modules
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from multiprocessing import Process, freeze_support, Manager
import re, urllib.parse, json
from socket import timeout

# declare a function that takes a 
# minimum benchmark score as a parameter 
def min_mark_gpu(min_mark):
	if (type(min_mark) != int) and (type(min_mark) != float):
		return 'You have entered a non-numeric value.  Try again.  '
	else:
		# variable to store the URLs collected
		# URLs contain specification information about the processor
		url_array = []
		
		# url containing the URL to a webpage that has processors
		# ranked based on how well they can perform after being overclocked
		url = 'https://www.videocardbenchmark.net/GPU_mega_page.html'
		# variable containing the site's domain name
		base_url = 'https://www.videocardbenchmark.net/'
		# variable that connects to the web page containing
		# the ranked processors
		main_con = BeautifulSoup(urlopen(Request(url)).read(), 'html.parser').select('table.tablesorter')[0]
		
		# variable containing the table columns
		table_columns = main_con.select('thead tr th')
		# variable containing records for each row
		items1 = main_con.select('tr[id^=gpu]')
		# variable containing more information about a graphics card
		#items2 = main_con.select('tr.tablesorter-childRow')
		
		# variable to store hardware information as a JSON object
		spec_object = {}
		
		# variable to store hardware information as a JSON object
		json_object = {}
		# JSON key storing an array of JSON objects
		# for the hardware's specs
		json_object['items'] = []
		
		# array variable to store graphics cards' JSON object's keys
		key_array_gpu = [
			'Hardware Name', 
			'Price', 
			'Benchmark', 
			'Videocard Value', 
			'G2D Mark', 
			'TDP (W)', 
			'Power Perf', 
			'Test Date', 
			'Category'
		]
		
		# iterate through the hardware rows
		for item in range(len(items1)):
			# variable storing records found within
			# each hardware component's rows
			items1_sub = items1[item].select('td')
			
			# append specs key to JSON specs object
			spec_object['specs'] = {}
			
			# iterate through the row's records
			for sub_item in range(len(items1_sub)):
				# if index equals zero
				# the key array's element index containing the hardware's name
				if sub_item == 0:
					# variable containing the record
					value = items1_sub[sub_item].text
					
					# variable that stores the regular expression string
					# regular expression looks for brackets
					rgx_brackets = '\(|\)'
					rgx_terms = 'GeForce '
					
					# if the regular expression splits the value into
					if len(re.split(rgx_brackets, value)) >= 2:
						# join the split value into one string
						# with the brackets removed
						value = ''.join(re.split(rgx_brackets, value))
					
					# if the regular expression splits the value into
					if len(re.split(rgx_terms, value)) >= 2:
						# join the split value into one string
						# with the brackets removed
						value = re.split(rgx_terms, value)[1]
				# if index equals two
				# the key array's element index containing the G3D Mark
				elif sub_item == 2:
					# variable containing the record
					# cast as a float variable
					value = float(items1_sub[sub_item].text)
				else:
					# variable containing the record
					value = items1_sub[sub_item].text
				
				# append a key to the JSON specs object
				spec_object['specs'][key_array_gpu[sub_item]] = value
			
			# if the G3D mark is equal to or above a specific value
			if spec_object['specs'][key_array_gpu[2]] >= min_mark:		
				# append the JSON specs object to the JSON object
				json_object['items'].append(spec_object)
				
			# empty out the JSON specs object
			spec_object = {}
		
		# return the JSON object
		return json_object

# declare a function that takes a 
# minimum benchmark score as a parameter 
def min_mark_cpu(min_mark):
	if (type(min_mark) != int) and (type(min_mark) != float):
		return 'You have entered a non-numeric value.  Try again.  '
	else:
		# url containing the URL to a webpage that has processors
		# ranked based on how well they can perform after being overclocked
		url = 'https://www.cpubenchmark.net/CPU_mega_page.html'
		# variable containing the site's domain name
		base_url = 'https://www.cpubenchmark.net/'
		# variable that connects to the web page containing
		# the ranked processors
		main_con = BeautifulSoup(urlopen(Request(url)).read(), 'html.parser').select('table.tablesorter')[0]
		
		# variable containing the table columns
		table_columns = main_con.select('thead tr th')
		
		# variable containing records for each row
		items1 = main_con.select('tr[id^=cpu]')
		
		# variable to store hardware information as a JSON object
		spec_object = {}
		
		# variable to store hardware information as a JSON object
		json_object = {}
		# JSON key storing an array of JSON objects
		# for the hardware's specs
		json_object['items'] = []
		
		# array variable to store processors' JSON object's keys
		key_array_cpu = [
			'Hardware Name',
			'Price',
			'Benchmark',
			'CPU Value',
			'Thread Mark',
			'Thread Value',
			'TDP (W)',
			'Power Performance',
			'Test Date',
			'Socket',
			'Category'
		]
		
		# iterate through the hardware rows
		for item in range(len(items1)):
			# variable storing records found within
			# each hardware component's rows
			items1_sub = items1[item].select('td')
			
			# append specs key to JSON specs object
			spec_object['specs'] = {}
			
			# iterate through the row's records
			for sub_item in range(len(items1_sub)):
				# if index equals zero
				# the key array's element index containing the hardware's name
				if sub_item == 0:
					# variable containing the record
					value = items1_sub[sub_item].text
					
					# variable that stores the regular expression string
					# regular expression looks for brackets
					rgx_brackets = '\(|\)'
					rgx_terms = 'Intel |AMD | @ '
					
					# if the processor name contains AMD, Intel, or an @ symbol
					# and the regular expression splits the processor name into
					# two or more array elements
					if len(re.split(rgx_terms, value)) >= 2:
						# split the name into an array and store the second element
						# as the shortened processor name
						value = re.split(rgx_terms, value)[1]
					# if the processor name contains AMD, Intel, or an @ symbol
					# and the regular expression splits the processor name into
					# two elements
					elif len(re.split(rgx_terms, value)) == 1:
						# split the name into an array and store the first element
						# as the shortened processor name
						value = re.split(rgx_terms, value)[0]
					# if the processor name doesn't contains AMD, Intel, or an @ symbol
					else:
						# store the full processor name in the 
						# shortened processor name variable
						value = value
				# if index equals two
				# the key array's element index containing the G3D Mark
				elif sub_item == 2:
					# variable containing the record
					# cast as a float variable
					value = float(items1_sub[sub_item].text)
				else:
					# variable containing the record
					value = items1_sub[sub_item].text
				
				# append a key to the JSON specs object
				spec_object['specs'][key_array_cpu[sub_item]] = value
			
			# if the CPU Mark is equal to or above a specific value
			if (float(spec_object['specs'][key_array_cpu[2]])) >= min_mark:		
				# append the JSON specs object to the JSON object
				json_object['items'].append(spec_object)
				
			# empty out the JSON specs object
			spec_object = {}
		
		# return the JSON object
		return json_object

# declare a function that scrapes Kijiji for advertisements
# for processors found in the URL array
# function takes a URL and a shared list as paramaters
def kijiji_scrape(json_parameter, manager_list):
	# variable containing the page number
	a = 0
	
	# initialize a JSON object
	json_object = {}
	
	# JSON object key to store an array information about
	# the hardware's specs
	json_object['specs'] = json_parameter['specs']
	
	# JSON object key to store an array information about
	# the listed ads for a processor
	json_object['kijiji_ads'] = []
	
	# create an infinite loop
	while True:
		# increment the page number
		a += 1
		
		# variable storing a URL to a Kijiji search for the processor
		url = 'https://www.kijiji.ca/b-ontario/' + urllib.parse.quote(json_parameter['specs']['Hardware Name']).replace('%20', '-') + '/page-' + str(a) + '/k0l9004?sort=priceAsc&ad=offering'
		
		try:
			# variable storing the HTML contents of the Kijiji search page
			# after connecting to it
			main_con = BeautifulSoup(urlopen(Request(url), timeout=5).read().decode(), 'html.parser').select('div.regular-ad')
		except timeout:
			print(url)
			pass
		except urllib.error.HTTPError:
			print(url)
			pass
		
		# initialize a variable containing the 
		# HTML element for the next page button
		next_page = None
		
		# if there are one or more advertisements for the processor 
		if (len(main_con) != 0):
			# iterate through the advertisements
			for post in range(len(main_con)):
				# if ad's element has the data-third-party-id attribute
				# and the ad's element is not empty
				if (main_con[post].has_attr('data-third-party-id') == False) and (len(main_con[post]) != 0):
					# initiate a JSON object for information about the ad
					result_object = {}
					
					if len(main_con[post].select('div.info div.price')) != 0:
						# store the ad's price in the JSON object's price key
						result_object['price'] = main_con[post].select('div.info div.price')[0].text.replace('$', '').replace('\n', '').replace(' ', '')
					else:
						# store zero as the ad's price in the 
						# JSON object's price key
						result_object['price'] = 0
					
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
		
		try:
			# variable containing the HTML element for the next page button
			next_page = BeautifulSoup(urlopen(Request(url)).read().decode(), 'html.parser').select('a[title=\"Next\"]')
		except urllib.error.HTTPError:
			# add the JSON object to an array
			manager_list.append(json_object)
			
			# return the JSON object
			#return json.dumps(json_object, indent=4)
			print(json.dumps(json_object, indent=4))
			
			# stop the infinite loop
			break
		
		# if the next_page HTML element is empty
		# and the JSON object isn't empty
		
		if (len(next_page) == 0):
			# if there is one or more ad for the processor
			if len(json_object['kijiji_ads']) != 0:
				# add the JSON object to an array
				manager_list.append(json_object)
			
			# return the JSON object
			return json.dumps(json_object, indent=4)
			
			# stop the infinite loop
			break

#meme = {'items': [{'specs': {'Hardware Name': 'i7 3770'}}]}
#print(kijiji_scrape(meme['items'][0], []))

if __name__ == '__main__':
	# variable that stores a share list
	manager_list = Manager().list()
	# variable to store an array containing processes
	processes = []
	
	# variable that stores an array of CPU benchmarks and URLs
	proc_array = min_mark_gpu(10000)['items']
	
	# iterate through each processor
	for i in range(len(proc_array)):
		# variable to store a process that calls the 
		# Kijiji scraping function
		p = Process(target=kijiji_scrape, args=(proc_array[i], manager_list))
		# start the process
		p.start()
		# append the process to the processes array
		processes.append(p)
	
	# iterate through the processes
	for p in processes:
		# block a calling thread until the process whose
		# join method ends
		p.join()
	
	# variable containing a sorted JSON object
	sorted_object = sorted(manager_list._getvalue(), key=lambda x : x['specs']['Benchmark'], reverse=True)
	
	# append sorted array object to a JSON object
	final_object = {'items': sorted_object}	
	
	# print the sorted JSON object
	print(json.dumps(final_object, indent=4))