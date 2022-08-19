import urllib.parse, json, requests
from bs4 import BeautifulSoup



def get_tags_lfm(json_object, query):
	json_object['lfm'] = {}
	
	query = urllib.parse.quote(query)
	url_track = 'https://www.last.fm' + BeautifulSoup(requests.get('https://www.last.fm/search/tracks?q=' + query).text, 'html.parser').select('tbody tr.chartlist-row td.chartlist-name a')[0]['href']

	con_track = BeautifulSoup(requests.get(url_track).text, 'html.parser')
	
	json_object['lfm']['artists'] = con_track.select('div.header-new-content .header-new-crumb span')[0].text
	json_object['lfm']['title'] = con_track.select('div.header-new-content h1.header-new-title')[0].text
	json_object['lfm']['tags'] = []

	elm_tags = con_track.select('div.col-sm-8 section.catalogue-tags  ul.tags-list li.tag a')
	array_tags = []

	for tag in elm_tags:
		json_object['lfm']['tags'] .append(tag.text)

	return json_object

def artist_songs_popular(json_object, object_query, object_songs, key_name):
	array = []
	
	for index in object_songs[key_name]:
		if index['api_path'] != object_query['primary_artist']['api_path']:
			array_songs = json.loads(requests.get('https://genius.com/api' + index['api_path'] + '/songs?page=1&sort=popularity').text)['response']['songs']
			
			json_object['gen'][key_name] = {}
			json_object['gen'][key_name]['name'] = index['name']
			json_object['gen'][key_name]['array_songs'] = []
			
			for song in array_songs:
				json_object['gen'][key_name]['array_songs'].append(song['title'])

def get_producers(json_object, query):
	json_object['gen'] = {}
	
	query = urllib.parse.quote(query)
	object_query = json.loads(requests.get('https://genius.com/api/search/multi?per_page=5&q=' + query).text)['response']['sections'][0]['hits']#[0]['result']
	
	for result in object_query:
		if (result['index'] == 'song') and (result['type'] == 'song'):
			object_json = result['result']
			
			object_songs = json.loads(requests.get('https://genius.com/api' + object_json['api_path']).text)['response']['song']
			artist_songs_popular(json_object, object_json, object_songs, 'producer_artists')
			artist_songs_popular(json_object, object_json, object_songs, 'writer_artists')
			#break
			
	#print(json.dumps(object_query, indent=4))
	

query = input('Enter a song name:  ')

json_object = {}
get_tags_lfm(json_object, query)
get_producers(json_object, query)
print(json.dumps(json_object, indent=4))