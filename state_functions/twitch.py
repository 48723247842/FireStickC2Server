import stackprinter
import time
import requests
from pprint import pprint

import redis_circular_list

from ADBWrapper import ADBWrapper
from PIL import Image
from pathlib import Path

import utils

def next( c2 ):
	result = {}
	try:
		print( "next" )
		previous_state = c2.redis.get_state()
		adb = ADBWrapper( { "ip": c2.config.adb.ip , "port": c2.config.adb.port } )
		previous_adb_status = adb.get_status()

		adb.press_key( 87 )
		time.sleep( 0.5 )
		new_adb_status = adb.get_status()

		previous_state[ "adb_status" ] = new_adb_status
		c2.redis.set_state( previous_state )

		result = previous_state
	except Exception as e:
		print( e )
	return result

def previous( c2 ):
	result = {}
	try:
		print( "previous" )
		previous_state = c2.redis.get_state()
		adb = ADBWrapper( { "ip": c2.config.adb.ip , "port": c2.config.adb.port } )
		previous_adb_status = adb.get_status()

		adb.press_key( 88 )

		# adb.press_key_sequence( [ 21 , 21 , 21 , 21 , 21 , 21 ] )
		# adb.press_key_sequence( [ 22 , 22 ] )
		# adb.press_key_sequence( [ 23 , 23 ] )

		time.sleep( 0.5 )
		new_adb_status = adb.get_status()

		previous_state[ "adb_status" ] = new_adb_status
		c2.redis.set_state( previous_state )

		result = previous_state
	except Exception as e:
		print( e )
	return result

def stop( c2 ):
	result = {}
	try:
		print( "stop" )
		previous_state = c2.redis.get_state()
		adb = ADBWrapper( { "ip": c2.config.adb.ip , "port": c2.config.adb.port } )
		previous_adb_status = adb.get_status()

		adb.press_key( 86 )
		time.sleep( 0.5 )
		new_adb_status = adb.get_status()

		previous_state[ "adb_status" ] = new_adb_status
		c2.redis.set_state( previous_state )

		result = previous_state
	except Exception as e:
		print( e )
	return result

def play( c2 ):
	result = {}
	try:
		print( "play" )
		previous_state = c2.redis.get_state()
		adb = ADBWrapper( { "ip": c2.config.adb.ip , "port": c2.config.adb.port } )
		previous_adb_status = adb.get_status()

		adb.press_key( 126 )
		time.sleep( 0.5 )
		new_adb_status = adb.get_status()

		previous_state[ "adb_status" ] = new_adb_status
		c2.redis.set_state( previous_state )

		result = previous_state
	except Exception as e:
		print( e )
	return result

def pause( c2 ):
	result = {}
	try:
		print( "pause" )
		previous_state = c2.redis.get_state()
		adb = ADBWrapper( { "ip": c2.config.adb.ip , "port": c2.config.adb.port } )
		previous_adb_status = adb.get_status()

		adb.press_key( 127 )
		time.sleep( 0.5 )
		new_adb_status = adb.get_status()

		previous_state[ "adb_status" ] = new_adb_status
		c2.redis.set_state( previous_state )

		result = previous_state
	except Exception as e:
		print( e )
	return result

def resume( c2 ):
	result = {}
	try:
		print( "resume" )
		play( c2 )
	except Exception as e:
		print( e )
	return result

def play_pause( c2 ):
	result = {}
	try:
		print( "play_pause" )
		previous_state = c2.redis.get_state()
		adb = ADBWrapper( { "ip": c2.config.adb.ip , "port": c2.config.adb.port } )
		previous_adb_status = adb.get_status()

		adb.press_key( 85 )
		time.sleep( 0.5 )
		new_adb_status = adb.get_status()

		previous_state[ "adb_status" ] = new_adb_status
		c2.redis.set_state( previous_state )

		result = previous_state
	except Exception as e:
		print( e )
	return result

# "spotify:playlist:0OEHvHh4SQOOYivJGfEXve:play"
def uri( c2 , uri ):
	result = {}
	try:
		print( "uri" )
		previous_state = c2.redis.get_state()
		adb = ADBWrapper( { "ip": c2.config.adb.ip , "port": c2.config.adb.port } )
		previous_adb_status = adb.get_status()

		adb.open_uri( uri )
		time.sleep( 0.5 )
		new_adb_status = adb.get_status()

		result = {
			"name": "twitch" ,
			"function": "uri" ,
			"uri": uri ,
			"time": utils.get_common_time_string( c2.config.time_zone ) ,
			"adb_status": new_adb_status
		}
		c2.redis.set_state( result )
	except Exception as e:
		print( e )
	return result

def shuffle_on( c2 ):
	result = {}
	print( "shuffle_on" )
	return result

def shuffle_off( c2 ):
	result = {}
	print( "shuffle_off" )
	return result


def one_hot_is_user_live( options ):
	try:
		endpoint = 'https://api.twitch.tv/helix/streams'
		my_headers = {
			'Client-ID': options[ 1 ] ,
			'Authorization': f'Bearer {options[ 2 ]}'
		}
		my_params = {'user_login': options[ 0 ]}
		response = requests.get( endpoint , headers=my_headers , params=my_params )
		data = response.json()['data']
		if len(data) == 0:
			return False
		result = data[0]['type'] == 'live'
		if result == True:
			return options[ 0 ]
		return False
	except Exception as e:
		print( e )
		return False

def get_live_users_currated( config ):
	batch_option_list = [ [ x , config.apps.twitch.personal.client_id , config.apps.twitch.personal.oauth_token ] for x in config.apps.twitch.following.currated ]
	results = utils.batch_process({
		"max_workers": 5 ,
		"batch_list": batch_option_list ,
		"function_reference": one_hot_is_user_live
	})
	results = [ x for x in results if x ]
	order = { v: i for i , v in enumerate( config.apps.twitch.following.currated ) }
	currated_results = sorted( results , key=lambda x: order[ x ] )
	return currated_results

def update_live_users_currated( c2 ):
	live_currated_following_key = f"{c2.config.redis.prefix}.APPS.TWITCH.FOLLOWING.CURRATED"
	live_currated_following = get_live_users_currated( c2.config )
	c2.redis.redis.delete( live_currated_following_key )
	for i , x in enumerate( live_currated_following ):
		c2.redis.redis.rpush( live_currated_following_key , x )
	return live_currated_following

def play_next_live_follower( c2 ):
	try:
		previous_state = c2.redis.get_state()
		adb = ADBWrapper( { "ip": c2.config.adb.ip , "port": c2.config.adb.port } )
		previous_adb_status = adb.get_status()

		live_currated_following_key = f"{c2.config.redis.prefix}.APPS.TWITCH.FOLLOWING.CURRATED"
		if previous_state[ "name" ] != "twitch":
			update_live_users_currated( c2 )
			next_live_user = redis_circular_list.next( c2.redis.redis , live_currated_following_key )
		else:
			next_live_user = redis_circular_list.next( c2.redis.redis , live_currated_following_key )
		if next_live_user == False:
			update_live_users_currated( c2 )
			next_live_user = redis_circular_list.next( c2.redis.redis , live_currated_following_key )
		if next_live_user == False:
			print( "None of Currated Users are Online !!" )
			return False

		print( next_live_user )

		# https://open.spotify.com/playlist/75igTPKAdDsBYFtYCHO555
		# https://github.com/justintv/Twitch-API/blob/cf1e6231cc7b22373a5407a9cbd40d5c4ee49dd3/mobile_deeplinks.md
		# uri = f"https://twitch.tv/{next_live_user}"
		# uri = f"twitch://game/{next_live_user}"
		# uri = f"twitch://video/{next_live_user}"
		# uri = f"twitch://channel/{next_live_user}"
		uri = f"twitch://stream/{next_live_user}"
		print( f"ADB :: Launching :: {uri}" )
		adb.open_uri( uri )
		new_adb_status = adb.get_status()

		# make sure chat is open or closed ??
		# adb.press_key_sequence( [ asdf , asdf , ... ] )

		new_state = {
			"name": "twitch" ,
			"function": "play_next_live_follower" ,
			"uri": uri ,
			"time": utils.get_common_time_string( c2.config.time_zone ) ,
			"adb_status": new_adb_status
		}
		c2.redis.set_state( new_state )
		result = {
			"previous_state": previous_state ,
			"previous_adb_status": previous_adb_status ,
			"adb_opened_uri": uri ,
			"new_state": new_state ,
			"new_adb_status": new_adb_status ,
		}
		return result
	except Exception as e:
		print( stackprinter.format() )
		c2.log( e )
		return False