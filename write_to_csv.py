'''	Name: 		Kuteesa Kiyaga
	Date: 		September 27, 2019
	Function: 	Write to a .csv file.  
'''

# import modules
import csv

# variable containing the CSV file name
csv_file_name = 'eggs.csv'

# create a .csv file if it doesn't exists
# 'w+' argument forces the file to be created
# if it doesn't exist
csvfile = open(csv_file_name, 'w+', newline='')

# variable containing the column headers
fieldnames = ['first_name', 'last_name']

# variable containing an object 
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

# write the column headers into the .csv file
writer.writeheader()

# write values under the specified columns
writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})