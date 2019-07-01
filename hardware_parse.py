'''	Name:		Kuteesa Kiyaga
	Date:		June 30, 2019
	Function:	Concurrently scrape Kijiji for processor advertisements.  
'''

# import modules
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from multiprocessing import Process, freeze_support, Manager
import re, urllib.parse, json

# declare a function that takes a 
# minimum benchmark score as a parameter 
def min_mark(min_mark):
	# variable to store the URLs collected
	# URLs contain specification information about the processor
	url_array = []
	
	# url containing the URL to a webpage that has processors
	# ranked based on how well they can perform after being overclocked
	url = 'https://www.cpubenchmark.net/overclocked_cpus.html'
	# variable containing the site's domain name
	base_url = 'https://www.cpubenchmark.net/'
	# variable that connects to the web page containing
	# the ranked processors
	main_con = BeautifulSoup(urlopen(Request(url)).read().decode(), 'html.parser').select('table.chart tr')
	
	# iterate through all processors
	for index in range(1, len(main_con), 2):
		# perform the nested statements if the CPU URL is present
		# within the web page
		if len(main_con[index].select('td.chart a')) != 0:
			
			# initialize a JSON variable
			cpu_object = {}
			# insert a key to the JSON object containing the URL
			# to the webpage containing the processor's 
			# specification information
			cpu_object['cpu_url'] = base_url + main_con[index].select('td.chart a')[0]['href']
			
			# create a JSON object key containing the
			# processor's benchmark
			cpu_object['cpu_mark'] = None
			
			# if the HTML element containing the benchmark
			# is not empty
			if len (main_con[index].select('div.meter span')) != 0:
				# insert a key to the JSON object containing the URL
				# to the webpage containing the processor's benchmark
				cpu_object['cpu_mark'] = float(main_con[index].select('td.value div.meter')[0].text.replace(' ', '').replace(',', ''))
			
			# if the processor's benchmark is below the
			# passed minimum benchmark score
			if cpu_object['cpu_mark'] < min_mark:
				# stop collecting URL and benchmark information
				break
			
			# append the JSON object to the URL array
			url_array.append(cpu_object)
	
	# return the URL object containing a list of
	# processors' benchmark and URL
	return url_array

# declare a function that scrapes Kijiji for advertisements
# for processors found in the URL array
# function takes a URL and a shared list as paramaters
def kijiji_cpu_scrape(cpu_url, manager_list):
	# initialize a JSON object for storing information about
	# a processor's specifications
	json_spec_object = {}
	
	# variable that connects to and stores the HTML contents
	# of the processor page
	con = BeautifulSoup(
		urlopen(
			Request(cpu_url)
		).read().decode(), 'html.parser'
	)
	
	# variable that stores the processor's benchmark
	cpu_mark = float(con.select('table.desc span')[7].text)
	
	# add the benchmark to the CPU Mark key in the JSON object
	json_spec_object['CPU Mark'] = cpu_mark
	
	# variable that stores the processor's name
	cpu_name = con.select('td span.cpuname')[0].text
	# initialize a variable used to store a processor's shortened name
	cpu_name_short = None
	
	# variable that stores the regular expression string
	rgx_string = 'Intel |AMD | @ '
	
	# if the processor name contains AMD, Intel, or an @ symbol
	# and the regular expression splits the processor name into
	# two or more array elements
	if len(re.split(rgx_string, cpu_name)) >= 2:
		# split the name into an array and store the second element
		# as the shortened processor name
		cpu_name_short = re.split(rgx_string, cpu_name)[1]
	# if the processor name contains AMD, Intel, or an @ symbol
	# and the regular expression splits the processor name into
	# two elements
	elif len(re.split(rgx_string, cpu_name)) == 1:
		# split the name into an array and store the first element
		# as the shortened processor name
		cpu_name_short = re.split(rgx_string, cpu_name)[0]
	# if the processor name doesn't contains AMD, Intel, or an @ symbol
	else:
		# store the full processor name in the 
		# shortened processor name variable
		cpu_name_short = cpu_name
	
	# store the shortened processor name in the CPU name key for 
	# processor specification object
	json_spec_object['CPU Name'] = cpu_name_short
	# variable storing HTML contents containing specifications
	# of a processor
	spec_object = con.select('div.content table.desc td em')
	# array containing a processor's specification information
	spec_list = str(spec_object[0]).replace('</em>', '').replace('<br/></br></br></br>', '').replace('<br>', '</br>').replace('</strong>', '').split('<strong>')
	
	# iterate through the processor specifications
	for spec in range(1, len(spec_list)):
		# variable storing a processor's specification information
		spec_item = BeautifulSoup(str('<div>' + spec_list[spec].replace('br>', 'div>')), 'html.parser').text
		# variable storing the specification type
		spec_field = spec_item.split(': ')[0]
		# variable storing the specification value
		spec_value = spec_item.split(': ')[1]
		json_spec_object[spec_field] = spec_value
	
	
	
	# variable storing a URL to a Kijiji search for the processor
	url = 'https://www.kijiji.ca/b-ontario/' + urllib.parse.quote(cpu_name_short).replace('%20', '-') +'/k0l9004?sort=priceAsc&ad=offering'
	# variable storing the HTML contents of the Kijiji search page
	# after connecting to it
	main_con = BeautifulSoup(urlopen(Request(url)).read().decode(), 'html.parser').select('div.regular-ad')
	
	# initialize a JSON object
	json_object = {}
	
	# if there are one or more advertisements for the processor 
	if len(main_con) != 0:
		# add the specifications JSON object to the
		# JSON object's specs key
		json_object['specs'] = json_spec_object
		# JSON object key to store an array information about
		# the listed ads for a processor
		json_object['kijiji_ads'] = []
	
	# iterate through the advertisements
	for post in range(len(main_con)):
		# if ad's element has the data-third-party-id attribute
		# and the ad's element is not empty
		if (main_con[post].has_attr('data-third-party-id') == False) and (len(main_con[post]) != 0):
			# initiate a JSON object for information about the ad
			result_object = {}
			
			# store the ad's price in the JSON object's price key
			result_object['price'] = main_con[post].select('div.info div.price')[0].text.replace('$', '').replace('\n', '').replace(' ', '')
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
			
			# add the ad's JSON object to the kijiji_ads key
			json_object['kijiji_ads'].append(result_object)
			# empty out the JSON object
			result_object = {}
	
	# if the JSON object isn't empty
	if json_object != {}:
		# add the JSON object to an array
		manager_list.append(json_object)

if __name__ == '__main__':
	# variable that stores a share list
	manager_list = Manager().list()
	# variable to store an array containing processes
	processes = []
	
	# variable that stores an array of CPU benchmarks and URLs
	proc_array = min_mark(10000)
	
	# iterate through each processor
	for i in range(len(proc_array)):
		# variable to store a process that calls the 
		# Kijiji scraping function
		p = Process(target=kijiji_cpu_scrape, args=(proc_array[i]['cpu_url'],manager_list))
		# start the process
		p.start()
		# append the process to the processes array
		processes.append(p)
	
	# iterate through the processes
	for p in processes:
		# block a calling thread until the process whose
		# join method ends
		p.join()
	
	# variable storing the JSON object, sorted by CPU Mark
	sorted_object = sorted(manager_list._getvalue(), key=lambda x : x['specs']['CPU Mark'], reverse=True)
	# append sorted array object to a JSON object
	final_object = {'items': sorted_object}	
	
	# print the beautified and sorted JSON object
	print(json.dumps(final_object, indent=4))