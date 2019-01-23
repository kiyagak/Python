# import libraries
import urllib.request, json, urllib.parse

'''
Name: Kuteesa Kiyaga
Date: January 22, 2019
Function: Determine whether individual Quake Champions users
		  are playing as part of a party with one or more 
		  other players.  
'''



#define function to contain code block
def party_finder():
	# url string that will have a username parameter appended to it
	# contains user's recent match IDs
	player_stats_url = 'https://stats.quake.com/api/v2/Player/GamesSummary?name='

	# boolean variable that terminates the program once it equals True
	break_queue = False

	# repeat prompting user for the desired user to look up
	while break_queue == False:
		# print instructions outlining how to terminate the program
		print('Type "[STOP]", with square braced included, to stop the process.  ')
		# prompt the user to enter a username
		user_prompt = input("Enter a player username: ")
		
		# make the program perform an action if the 
		# user enters the termination phrase
		if user_prompt.lower() == '[stop]':
			# instruct the user the press either Y or NT
			# Y terminates the program
			# N resumes the program
			print('Press N to stop the process.  Press Y to keep running the process.  ')
			# ask the user to press Y or N
			break_prompt = input('Are you sure you want to stop?  [Y] [N]')
			
			# terminate the program if the user presses Y
			if break_prompt.lower() == 'y':
				# variable terminates program if set to True
				break_queue = True
		
		
		
		# create a HTTP GET request using the player stats URL 
		# and the username parameter
		
		# URL encode the username that the user enters in case it 
		# contains spaces or other non-alphabetical characters
		req = urllib.request.Request(player_stats_url + urllib.parse.quote(user_prompt))
		
		# add user-agent and referer headers to avoid HTTP 403 forbidden error
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
		req.add_header('Referer', 'https://stats.quake.com')
		
		#variable containing designed to contain HTTP GET results
		match_con = None

		
		try:
			#assign HTTP GET results to its appropriate variable
			match_con = json.loads(urllib.request.urlopen(req).read())
		# catch any HTTP 400 bad request errors
		except urllib.error.HTTPError:
			print('HTTP error exception.  ')
			print()
		
		# inform the user that the searched user does not have a
		# Quake account
		if match_con == None:
			print(user_prompt + ' is an invalid account.  Try again.  ')
			print()
		
		# inform the user that the user they're searching for
		# has not played any recent matches or is not an existing user
		elif ('matches' not in match_con) and (user_prompt.lower() != '[stop]'):
			print('No recent match results found for the following user: ' + user_prompt)
			print()
		# inform the user that they have successfully terminated the process
		# if they enter "[STOP]" and press Y
		elif ('matches' not in match_con) and (user_prompt.lower() == '[stop]') and (break_prompt.lower() == 'y'):
			print('Process has been terminated.  ')
			print()
		# inform the user that the process has resumed
		# if they enter "[STOP]" and press N
		elif ('matches' not in match_con) and (user_prompt.lower() == '[stop]') and (break_prompt.lower() == 'n'):
			print('Resuming process.  ')
			print()
		# inform the user that they haven't pressed Y or N
		# after entering [STOP]
		elif ('matches' not in match_con) and (user_prompt.lower() == '[stop]') and (break_prompt.lower() != 'y' or break_prompt.lower() != 'n'):
			print('You have not entered N or Y.  Press N or Y to stop the process.  ')
		else:
			# variable containing the user's match data
			matches = match_con['matches']
			# array containing the searched user's team players
			player_array = []
			# JSON object containing array of all teams the searched user played on
			team_array = {'items': []}
			# variable storing the number of Team Deathmatch matches
			# the program has iterated through
			tdm_tally = 0



			# iterate through the individual matches
			for match in range(len(matches)):
				# variable containing the match's game mode
				game_mode = matches[match]['gameMode']
				# ID of the individual match
				match_id = matches[match]['id']
				
				# stop iterating through individual matches if the 
				# number of Team Deathmatch matches is equal to or exceeds 3
				if game_mode == 'GameModeTeamDeathmatch':
					# variable breaks at 3 because there are cases where
					# two matches place two players on the same team
					# even though they are not in a party together
					if tdm_tally >= 3:
						break
					
					# increment the number of Team Deathmatch matches
					# the program has iterated through by 1
					tdm_tally += 1
					
					# variable containing the match URL with 
					# match ID and username parameters included
					match_url = 'https://stats.quake.com/api/v2/Player/Games?id=' + match_id + '&playerName=' + urllib.parse.quote(user_prompt)
					# create HTTP GET request using the match URL
					match_req = urllib.request.Request(match_url)
					# add user-agent and referer headers to avoid HTTP 403 forbidden error
					match_req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
					match_req.add_header('Referer', 'www.google.com')
					
					# variable to store the searched user's team number
					# in each individual match
					player_team = None
					
					# variable containing match statistics of all players
					# from both teams
					stats_object = json.loads(urllib.request.urlopen(match_req).read())['battleReportPersonalStatistics']
					
					# add an empty JSON object to the items JSON array key
					team_array['items'].append({})
					
					# iterate through all players found in the stats object
					for player in stats_object:
						# variable containing the player's nickname
						player_nick = player['nickname']
						# variable containing all players' team number
						# i.e. 0 or 1 in Team Deathmatch mode
						team_index = player['teamIndex']
						
						# if the searched user matches a match player's nickname
						# set the player team to the match player's team number
						if user_prompt.lower() == player_nick.lower():
							player_team = team_index
					
					# iterate through all players found in the stats object
					for player in stats_object:
						# variable containing all players' team number
						# i.e. 0 or 1 in Team Deathmatch mode
						team_index = player['teamIndex']
						# variable containing the player's nickname
						player_nick = player['nickname']
						
						# add players to player array if they share the same
						# team number as the searched user's team number
						if team_index == player_team:
							player_array.append(player_nick)
							team_array['items'][tdm_tally-1]['player_array'] = player_array
					
					# empty the player array after adding it to 
					# the team array JSON object
					player_array = []

			# team array key containing data from each match
			match_obj = team_array['items']
			
			
			# iterate through the match objects
			for match in range(len(match_obj)):
				# variable containing the searched user's 
				# individual match team members
				players = match_obj[match]['player_array']
				
				# iterate through all members of the searched user's team
				for player in range(len(players)):
					# variable containing the team player's nick name
					player_name = players[player]
					
					# boolean that stops comparing whether or not the team player
					# reoccurs in other matches
					player_bool = False
					
					# nested loop to allow each player to be compared to other matches
					# to determine if they reoccur in other matches
					for comp_match in range(len(match_obj)):
						for comp_player in range(len(players)):
							# add players that aren't already in the player array
							if player_name not in player_array:
								player_array.append(player_name)
								# stops comparing whether or not the 
								# team player reoccurs in other matches
								player_bool = True
						
						# stop the nested loop if the player
						# isn't in the player array
						if player_bool == True:
							break


			# variable containing how often each player reoccurs
			# throughout each match
			party_tally = 0
			# array containing which players reoccur throughout the matches
			party_members = []
			
			# iterate through the player array
			for player in range(len(player_array)):
				# variable containing how often a player reoccurs throughout
				# the matches
				player_freq = 0
				
				# variable containing the player's nickname
				player_name = player_array[player]
				
				# iterate through the match objects
				for match in range(len(match_obj)):
					# variable containing an array of the 
					# searched user's teammates
					team_array = match_obj[match]['player_array']
					# variable that determines whether or not the player
					# is in the team array
					player_bool = player_name in team_array
					
					# increment the player frequency if the player is found
					# within the team array
					if player_bool:
						player_freq += 1
					
					# increment the number of people that are 
					# part of a party if a player's name reoccurs
					# in 3 matches or more
					
					# will equal 1 if the searched player isn't 
					# part of a party
					if player_freq >= 3:
						party_tally += 1
						
						# add the reoccuring player to the array
						# containing the party's members
						party_members.append(player_name)
			
			
			# iterate through the match objects
			for match in range(len(match_obj)):
				# display the team members of each match
				print(match_obj[match]['player_array'])
				
			print()
			
			# state that no matches were found due to the player not
			# having played any recent Team Deathmatch mode games
			if ((party_tally-1) == -1) and (len(match_obj) == 0):
				print('No recent team match results have been found for ' + user_prompt + '.  ')
				print()
			
			# display how many other players are part of the 
			# searched user's party if the user has played at least
			# one Team Deathmatch game
			elif ((party_tally-1) == -1) and (len(match_obj) != 0):
				print('Based on ' + user_prompt + '\'s most recent three team matches, ' + str(party_tally) + ' other players are a part of this player\'s party.  ')
				print()
				
			# display that the user is not playing with a party
			else:
				print('Based on ' + user_prompt + '\'s most recent three team matches, ' + str(party_tally-1) + ' other players are a part of this player\'s party.  ')
				
			# display the party's members if at least two people
			# belong to the partys
			if (len(party_members) > 1):
				print('The party members are: ' + str(party_members))
			print()

#execute code block contained within function
party_finder()
