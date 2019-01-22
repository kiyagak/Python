import urllib.request, json, urllib.parse



url = 'https://stats.quake.com/api/v2/Player/GamesSummary?name='

break_queue = False

while break_queue == False:
	print('Type "[STOP]", with square braced included, to stop the process.  ')
	user_prompt = input("Enter a player username: ")
	
	if user_prompt.lower() == '[stop]':
		print('Press N to stop the process.  Press Y to keep running the process.  ')
		break_prompt = input('Are you sure you want to stop?  [Y] [N]')
		
		if break_prompt.lower() == 'y':
			break_queue = True
	
	req = urllib.request.Request(url + urllib.parse.quote(user_prompt))
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
	req.add_header('Referer', 'https://stats.quake.com')


	try:
		if ('matches' not in json.loads(urllib.request.urlopen(req).read())) and (user_prompt.lower() != '[stop]'):
			print('No recent match results found for the following user: ' + user_prompt)
		elif ('matches' not in json.loads(urllib.request.urlopen(req).read())) and (user_prompt.lower() == '[stop]'):
			print('Process has been terminated.  ')
		else:
			matches = json.loads(urllib.request.urlopen(req).read())['matches']
			player_array = []
			team_array = {'items': []}
			tdm_tally = 0



			for match in range(len(matches)):
				game_mode = matches[match]['gameMode']
				match_id = matches[match]['id']
				
				
				if game_mode == 'GameModeTeamDeathmatch':
					if tdm_tally >= 3:
						break
					
					tdm_tally += 1
						
					match_url = 'https://stats.quake.com/api/v2/Player/Games?id=' + match_id + '&playerName=' + urllib.parse.quote(user_prompt)
					match_req = urllib.request.Request(match_url)
					match_req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
					match_req.add_header('Referer', 'www.google.com')
					
					player_team = None
					
					stats_object = json.loads(urllib.request.urlopen(match_req).read())['battleReportPersonalStatistics']
					team_array['items'].append({})
					
					
					for player in stats_object:
						player_nick = player['nickname']
						team_index = player['teamIndex']
						
						if user_prompt.lower() == player_nick.lower():
							player_team = team_index
					
					for player in stats_object:
						team_index = player['teamIndex']
						player_nick = player['nickname']
						
						if team_index == player_team:
							player_array.append(player_nick)
							team_array['items'][tdm_tally-1]['team_index'] = player_team
							team_array['items'][tdm_tally-1]['match_num'] = match
							team_array['items'][tdm_tally-1]['player_array'] = player_array
							team_array['items'][tdm_tally-1]['match_id'] = match_id
					
					player_array = []


			match_obj = team_array['items']

			for team in range(len(match_obj)):
				players = match_obj[team]['player_array']
				
				for player in range(len(players)):
					player_name = players[player]
					
					bool = False
					
					for comp_team in range(len(match_obj)):
						for comp_player in range(len(players)):
							if player_name not in player_array:
								player_array.append(player_name)
								bool = True
						
						if bool == True:
							break



			party_tally = 0
			party_members = []
			
			for player in range(len(player_array)):
				player_freq = 0
				
				player_name = player_array[player]
				
				for team in range(len(match_obj)):
					team_array = match_obj[team]['player_array']
					player_bool = player_name in team_array
					
					if player_bool:
						player_freq += 1
						
					if player_freq >= 3:
						party_tally += 1
						party_members.append(player_name)
			
			

			for team in range(len(match_obj)):
				print(match_obj[team]['player_array'])
				
			print()
			
			if ((party_tally-1) == -1) and (len(match_obj) == 0):
				print('No recent team match results have been found for ' + user_prompt + '.  ')
			elif ((party_tally-1) == -1) and (len(match_obj) != 0):
				print('Based on ' + user_prompt + '\'s most recent three team matches, ' + str(party_tally) + ' other players are a part of this player\'s party.  ')
			else:
				print('Based on ' + user_prompt + '\'s most recent three team matches, ' + str(party_tally-1) + ' other players are a part of this player\'s party.  ')
			
			if (len(party_members) > 1):
				print('The party members are: ' + str(party_members))
		print()
	except urllib.error.HTTPError:
		print('HTTP error exception.  ')