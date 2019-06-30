# import modules
import urllib.request, json, urllib.parse

'''
Name: Kuteesa Kiyaga
Date: January 28, 2019
Function: Find an individual player's best weapon and
		  how often they pick up various map items within
		  the Team Deathmatch game mode.  
'''



#define function to contain code block
def weapons_pickups(user_prompt):
	# initialize kills per shot variable
	kills_per_shot = None
	# initialize accuracy variable
	accuracy = None
	# initialize damage per shot variable
	damage_per_shot = None
	
	
	# url string that will have a username parameter appended to it
	# contains user's recent match IDs
	player_stats_url = 'https://stats.quake.com/api/v2/Player/Stats?name='

	
	
	# create a HTTP GET request using the player stats URL 
	# and the username parameter
	
	# URL encode the username that the user enters in case it 
	# contains spaces or other non-alphabetical characters
	req = urllib.request.Request(player_stats_url + urllib.parse.quote(user_prompt))
	
	# add user-agent and referer headers to avoid HTTP 403 forbidden error
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
	req.add_header('Referer', 'https://stats.quake.com')
	
	#variable containing designed to contain HTTP GET results
	player_con = None
	
	try:
		#assign HTTP GET results to its appropriate variable
		player_con = json.loads(urllib.request.urlopen(req).read())
	# catch any HTTP 400 bad request errors
	except urllib.error.HTTPError as e:
		print(e)
		
	# inform the user that the searched user does not have a
	# Quake account
	if player_con == None:
		print(user_prompt + ' is an invalid account.  Try again.  ')
		print()
	
	# inform the user that the user they're searching for
	# has not played any recent matches or is not an existing user
	elif 'matches' not in player_con:
		print('No recent match results found for the following user: ' + user_prompt)
		print()
	else:
		# JSON object to store data on weapons
		total_weapon_obj = {}
		# JSON object to store data on pickups and kill/death ratio
		# within Team Deathmatch game modes
		pickup_obj = {}
		
		# JSON object storing data about each champion for
		# the searched user
		champs_obj = player_con['playerProfileStats']['champions']
		
		# iterate through all champions
		for champion in champs_obj:
			# JSON object storing data about various game modes
			game_mode_obj = champs_obj[champion]['gameModes']
			
			# iterate through all game modes
			for mode in game_mode_obj:
				# add JSON keys to JSON pickup object
				# if the game mode is Team Deathmatch
				if mode == 'GameModeTeamDeathmatch':
					pickup_obj['total_kills'] = []
					pickup_obj['total_deaths'] = []
					pickup_obj['total_games_played'] = []
					pickup_obj['total_power_pickups'] = []
					pickup_obj['total_mega_health_pickups'] = []
					pickup_obj['total_heavy_armour_pickups'] = []
					pickup_obj['total_tactical_pickups'] = []
					pickup_obj['total_healed'] = []
					pickup_obj['total_small_armour_pickups'] = []
					break
		
		# iterate through all champions
		for champion in champs_obj:
			# JSON object to store data about champions'
			# weapons and abilities
			weapon_obj = champs_obj[champion]['damageStatusList']
			# JSON object to store data of champions' within
			# various game modes
			game_mode_obj = champs_obj[champion]['gameModes']
			
			# iterate through all game modes
			for mode in game_mode_obj:
				# add game modes' various stats to the
				# JSON pickup object if game mode is Team Deathmatch
				if mode == 'GameModeTeamDeathmatch':
					pickup_obj['total_kills'].append(game_mode_obj[mode]['kills'])
					pickup_obj['total_deaths'].append(game_mode_obj[mode]['deaths'])
					pickup_obj['total_games_played'].append((game_mode_obj[mode]['won'] + game_mode_obj[mode]['lost'] + game_mode_obj[mode]['tie']))
					pickup_obj['total_power_pickups'].append(game_mode_obj[mode]['powerPickups'])
					pickup_obj['total_mega_health_pickups'].append(game_mode_obj[mode]['megaHealthPickups'])
					pickup_obj['total_heavy_armour_pickups'].append(game_mode_obj[mode]['heavyArmorPickups'])
					pickup_obj['total_tactical_pickups'].append(game_mode_obj[mode]['tacticalPickups'])
					pickup_obj['total_healed'].append(game_mode_obj[mode]['healed'])
					pickup_obj['total_small_armour_pickups'].append(game_mode_obj[mode]['smallArmorPickups'])
								
		# iterate through all champions
		for champion in champs_obj:
			# iterate through all weapons across all game modes
			for weapon in weapon_obj:
				# initialize JSON object to store tallies of
				# each weapon's hits, shots, kills, and damage
				total_weapon_obj[weapon] = {}
				total_weapon_obj[weapon]['weapon'] = weapon
				total_weapon_obj[weapon]['total_hits'] = []
				total_weapon_obj[weapon]['total_shots'] = []
				total_weapon_obj[weapon]['total_kills'] = []
				total_weapon_obj[weapon]['total_damage'] = []
			break
		
		# iterate through all champions
		for champion in champs_obj:
			# JSON object to store data about champions'
			# weapons and abilities
			weapon_obj = champs_obj[champion]['damageStatusList']
			
			# iterate through all weapons across all game modes
			for weapon in weapon_obj:
				# add weapons' stats to the JSON weapon object
				total_weapon_obj[weapon]['total_hits'].append(weapon_obj[weapon]['hits'])
				total_weapon_obj[weapon]['total_shots'].append(weapon_obj[weapon]['shots'])
				total_weapon_obj[weapon]['total_kills'].append(weapon_obj[weapon]['kills'])
				total_weapon_obj[weapon]['total_damage'].append(weapon_obj[weapon]['damage'])
				
				
				
		# initialize array to store each weapon's total kills
		array_total_kills = []
		# initialize array to store each weapon's total damage
		array_total_damage = []
		
		# variable to store each weapon's total hits
		total_hits = sum(total_weapon_obj[weapon]['total_hits'])
		# variable to store each weapon's total shots fired
		total_shots = sum(total_weapon_obj[weapon]['total_shots'])
		# variable to store each weapon's total kills
		total_kills = sum(total_weapon_obj[weapon]['total_kills'])
		# variable to store each weapon's total damage
		total_damage = sum(total_weapon_obj[weapon]['total_damage'])
		
		# iterate through all total weapons JSON object
		for weapon in total_weapon_obj:
			# variables storing the sum of each weapon's
			# hits, shots, kills, and damage
			total_hits = sum(total_weapon_obj[weapon]['total_hits'])
			total_shots = sum(total_weapon_obj[weapon]['total_shots'])
			total_kills = sum(total_weapon_obj[weapon]['total_kills'])
			total_damage = sum(total_weapon_obj[weapon]['total_damage'])
			
			# add weapon's total kills to total kills array
			array_total_kills.append(total_kills)
			# add weapon's total damage to total damage array
			array_total_damage.append(total_damage)
		
		
		
		# sort the total kills and damage arrays from
		# highest to lowest
		array_total_kills.sort(reverse=True)
		array_total_damage.sort(reverse=True)
		
		# initialize JSON object to store 
		array_weapon_stats = {}
		array_weapon_stats['kills'] = []
		array_weapon_stats['damage'] = []
		
		for weapon in total_weapon_obj:
			# variables storing the sum of each weapon's
			# hits, shots, kills, and damage
			total_hits = sum(total_weapon_obj[weapon]['total_hits'])
			total_shots = sum(total_weapon_obj[weapon]['total_shots'])
			total_kills = sum(total_weapon_obj[weapon]['total_kills'])
			total_damage = sum(total_weapon_obj[weapon]['total_damage'])
			
			# perform error handling in case variables above
			# divide zero by zero
			try:
				# variable to store accuracy
				accuracy = int(round((total_hits / total_shots) * 100, 0))
				# variable to store damage per shot
				damage_per_shot = total_damage / total_shots
				# variable to store kills per shot
				kills_per_shot = total_kills / total_shots
			# perform error handling in case variables above
			# divide zero by zero
			except ZeroDivisionError:
				# set accuracy to 0
				accuracy = 0
			except ZeroDivisionError:
				# set damage per shot to 0
				damage_per_shot = 0
			except ZeroDivisionError:
				# set damage per shot to 0
				kills_per_shot = 0
			
			
			
			# function to fill the weapon stats array with
			# weapon name, percentage of weapon damage,
			# accuracy, and damage per shot
			def array_wep_damage_stats():
				# initialize a JSON object to for storing
				# weapon name, percentage of weapon damage,
				# accuracy, and damage per shot
				stats_damage_obj = {}
				stats_damage_obj['weapon_name'] = None
				stats_damage_obj['percent_of_wep_damage'] = None
				stats_damage_obj['accuracy'] = None
				stats_damage_obj['damage_per_shot'] = None
				
				
				try:			
					# add keys and values for 
					# weapon name, percentage of weapon damage,
					# accuracy, and damage per shot
					stats_damage_obj['weapon_name'] = weapon
					stats_damage_obj['percent_of_wep_damage'] = int((total_damage / sum(array_total_damage)) * 100)
					stats_damage_obj['accuracy'] = accuracy
					stats_damage_obj['damage_per_shot'] = int(damage_per_shot)
				except ZeroDivisionError:
					stats_damage_obj['weapon_name'] = 0
				except ZeroDivisionError:
					stats_damage_obj['percent_of_wep_damage'] = 0
				except ZeroDivisionError:
					stats_damage_obj['accuracy'] = 0
				except ZeroDivisionError:					
					stats_damage_obj['damage_per_shot'] = 0
					
				# append the stats damage JSON object to the
				# array weapon stats damage object array
				array_weapon_stats['damage'].append(stats_damage_obj)
				
				# return the array weapon stats object if executed
				return array_weapon_stats
			
			# function to fill the weapon stats array with
			# weapon name, percentage of weapon damage,
			# accuracy, and damage per shot
			def array_wep_kills_stats():
				# initialize a JSON object to for storing
				# weapon name, percentage of weapon damage,
				# accuracy, and damage per shot
				stats_kills_obj = {}
				
				# add keys and values for 
				# weapon name, percentage of weapon kills,
				# accuracy, and kills per shot 
				stats_kills_obj['weapon_name'] = weapon
				stats_kills_obj['percent_of_wep_kills'] = int((total_kills / sum(array_total_kills)) * 100)
				stats_kills_obj['accuracy'] = accuracy
				stats_kills_obj['kills_per_shot'] = int(kills_per_shot)
				
				# append the stats kills JSON object to the
				# array weapon stats kills object array
				array_weapon_stats['kills'].append(stats_kills_obj)
									
				# return the array weapon stats object if executed
				return array_weapon_stats
			
			
				
			# iterate through total damage array
			for wep_index in range(len(array_total_damage)):
				# execute the array weapon damage stats function
				# if total damage equals the total damage array index
				if array_total_damage[wep_index] == total_damage:
					array_wep_damage_stats()
				# stop iteration if wep_index is greater than one
				# or iterates more than twice 
				elif wep_index > 1:
					break
			
			# iterate through total kills array
			for wep_index in range(len(array_total_kills)):
				# execute the array weapon kills stats function
				# if total kills equals the total kills array index
				if array_total_kills[wep_index] == total_kills:
					array_wep_kills_stats()
				# stop iteration if wep_index is greater than one
				# or iterates more than twice 
				elif wep_index > 1:
					break
		
		
		
		total_kdr = 0
		per_game_mega_health_pickups = 0
		per_game_heavy_armour_pickups = 0
		per_game_power_pickups = 0
		per_game_tactical_pickups = 0
		per_game_healed = 0
		per_game_small_armour_pickups = 0
		
		try:
			# variable to store kill/death ratio through all games
			total_kdr = sum(pickup_obj['total_kills']) / sum(pickup_obj['total_deaths'])
			# variable to store mega health pickups per game
			per_game_mega_health_pickups = sum(pickup_obj['total_mega_health_pickups']) / sum(pickup_obj['total_games_played'])
			# variable to store heavy armour pickups per game
			per_game_heavy_armour_pickups = sum(pickup_obj['total_heavy_armour_pickups']) / sum(pickup_obj['total_games_played'])
			# variable to store power up pickups per game
			per_game_power_pickups = sum(pickup_obj['total_power_pickups']) / sum(pickup_obj['total_games_played'])
			# variable to store tactical pickups per game
			per_game_tactical_pickups = sum(pickup_obj['total_tactical_pickups']) / sum(pickup_obj['total_games_played'])
			# variable to store the amount healed per game
			per_game_healed = sum(pickup_obj['total_healed']) / sum(pickup_obj['total_games_played'])
			# variable to store small armour pickups per game
			per_game_small_armour_pickups = sum(pickup_obj['total_small_armour_pickups']) / sum(pickup_obj['total_games_played'])
		except ZeroDivisionError:
			# variable to store kill/death ratio through all games
			total_kdr = 0
		except ZeroDivisionError:
			# variable to store heavy armour pickups per game
			per_game_heavy_armour_pickups = 0
		except ZeroDivisionError:
			# variable to store power up pickups per game
			per_game_power_pickups = 0
		except ZeroDivisionError:
			# variable to store tactical pickups per game
			per_game_tactical_pickups = 0
		except ZeroDivisionError:
			# variable to store the amount healed per game
			per_game_healed = 0
		except ZeroDivisionError:
			# variable to store small armour pickups per game
			per_game_small_armour_pickups = 0
		
		
		
		# initialize JSON object to store
		# KDR and pickups
		total_pickup_obj = {}
		# assign the variables below to their designated keys
		# rounded to two decimal places
		total_pickup_obj['player_name'] = user_prompt
		total_pickup_obj['total_kdr'] = round(total_kdr, 2)
		total_pickup_obj['per_game_mega_health_pickups'] = round(per_game_mega_health_pickups, 2)
		total_pickup_obj['per_game_heavy_armour_pickups'] = round(per_game_heavy_armour_pickups, 2)
		total_pickup_obj['per_game_power_pickups'] = round(per_game_power_pickups, 2)
		total_pickup_obj['per_game_tactical_pickups'] = round(per_game_tactical_pickups, 2)
		total_pickup_obj['per_game_healed'] = round(per_game_healed, 2)
		total_pickup_obj['per_game_small_armour_pickups'] = round(per_game_small_armour_pickups, 2)
		
		
		# sort weapon stats array based on percentage of total weapon damage
		sorted_array_damage = sorted(array_weapon_stats['damage'], key=lambda k: k['percent_of_wep_damage'], reverse=True)
		# sort weapon stats array based on percentage of total kills
		sorted_array_kills = sorted(array_weapon_stats['kills'], key=lambda k: k['percent_of_wep_kills'], reverse=True)
		
		# display JSON object containing data about pickups and
		# kill death ratio
		print(json.dumps(total_pickup_obj, indent=4))
		print()
		# display JSON object containing data about weapons
		# and how effectively they're used
		print(json.dumps(sorted_array_damage, indent=4))
			
			
			
#execute code block contained within function
weapons_pickups('SyncError')
