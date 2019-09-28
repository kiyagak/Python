'''
Name:		Kuteesa Kiyaga
Date:		September 27, 2019
Function:	Iterate through a JSON object array and 
			add the keys to an array if the array
			doesn't already contain the key.  
			
			Useful for determing the complete list of columns
			a .csv file will need.  
'''

def get_csv_column_headers(array_writerow):
	# initialize an empty array variable used to 
	# store the JSON objects' keys, which will be used as
	# column headers
	column_headers = []

	# iterate through the JSON object array
	for a in range(len(array_writerow)):
		# variable containing an array of the JSON object's keys
		row_json_keys = list(array_writerow[a].keys())
		
		# iterate through the JSON object's keys
		for b in range(len(row_json_keys)):
			# variable containing the JSON object key
			json_object_key = row_json_keys[b]
			
			# if the key is not an existing element in the 
			# column header array
			# done to prevent duplicates from being added
			# to the array
			if (row_json_keys[b] not in column_headers):
				# add the JSON object's key to the column header array
				column_headers.append(row_json_keys[b])

	# return the column headers
	return column_headers

# array variable containing multiple JSON objects
array_writerow = [
	{'first_name': 'Baked', 'last_name': 'Beans'},
	{'first_name': 'Lovely', 'last_name': 'Spam'},
	{'first_name': 'Wonderful', 'last_name': 'Spam'},
	{'first_name': 'Wonderful', 'last_name': 'Spam', 'Butts': 'Stuff'}
]

print(get_csv_column_headers(array_writerow))
