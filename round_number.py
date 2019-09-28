'''
	Name:		Kuteesa Kiyaga
	Date: 		September 28, 2019
	Function:	Use various positions to round an incoming number.  
'''


# declare a function that takes the price as a parameter
def round_number(raw_number):
	# if the price parameter is not a numeric data type
	if (type(raw_number) != float) and ((type(raw_number) != int)):
		return 'You have entered a non-numeric value.  Please try again.  '
	# otherwise
	else:
		# the number without decimals
		number_whole_value = str(raw_number).split('.')[0]
		# number of digits in the whole number
		whole_number_digits = len(number_whole_value)
		# initialize a rounding position integer variable	
		rounding_position = whole_number_digits - 2
		
		# if number of digits is greater than or equal to five
		if whole_number_digits >= 5:
			# round three positions to the left of the decimal
			rounding_position = 3
		# or if number of digits is greater than or equal to four
		elif whole_number_digits == 4:
			# round two positions to the left of the decimal
			rounding_position = 2
		# or if number of digits is greater than or equal to three
		elif whole_number_digits <= 3:
			# round one positions to the left of the decimal
			rounding_position = 1
		
		# variable containing the rounded number
		rounded_number = round(int(number_whole_value), -rounding_position)
		
		# return the rounded number
		return rounded_number

# call the function to round numbers of various length
print(round_number(4.62))
print(round_number(6.62))
print(round_number(14.62))
print(round_number(458.62))
print(round_number(7554.62))
print(round_number(105745.62))
print(round_number(8452345.62))
print(round_number(67445345.62))
print(round_number(67499345))
print(round_number(67499345442))
print(round_number('text'))