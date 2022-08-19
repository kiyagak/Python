import re, pgeocode

def get_location(json_location, location_postal_code):	
	location_postal_code = location_postal_code.upper()
	
	json_location['location_postal_code'] = location_postal_code
	json_location['location_country'] = None
	
	rgx_postal_code = '[a-zA-Z]'
	
	if re.search(rgx_postal_code, json_location['location_postal_code']) != None:
		json_location['location_country'] = 'Canada'
		json_location['location_country_code'] = 'ca'
		location_postal_code = location_postal_code[0:3].upper()
	else:
		json_location['location_country'] = 'United States'
		json_location['location_country_code'] = 'us'
	
	json_location['location_metropolitan_area'] = None
	
	nomi = pgeocode.Nominatim(json_location['location_country_code'])
	location = nomi.query_postal_code(location_postal_code)
	
	json_location['location_state'] = None
	json_location['location_state_code'] = None
	
	if type(location.state_name) != float:
		json_location['location_state'] = location.state_name
	
	if type(location.state_code) != float:
		json_location['location_state_code'] = location.state_code
	
	if type(location.place_name) != float:
		rgx_strings_replace = r'^(North|Northern|South|Southern|East|Eastern|West|Western|Downtown|Central|City of) |(Central|Inner|Outer|Core)| (North|Northeast|Northwest|North Central|South|Southeast|Southwest|Southeast|Southwest|East|West|Region)$'
		location_city = location.place_name
		location_city_no_brackets = location_city.split(' (')[0]
		
		json_location['location_city'] = re.sub(rgx_strings_replace, '', location_city_no_brackets).rstrip(' ')
	
	return json_location

print(get_location({}, 'L0S'))