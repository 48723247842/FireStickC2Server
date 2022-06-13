import stackprinter
import time
import json
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
			"name": "youtube" ,
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


def one_hot_get_channel_live_streams( options ):
	try:
		headers = { 'accept': 'application/json, text/plain, */*', }
		params = {
			"part": "snippet" ,
			# "q": options[ 0 ] , # this would be if we wanted to 'search' 'MontereyBayAquarium' instead of using the channelId property
			"channelId": options[ 0 ] ,
			"eventType": "live" ,
			"type": "video" ,
			"key": options[ 1 ] ,
			# "order": "viewCount" ,
			"order": "date" , # makes live_streams[ 0 ] = 'latest' and live_streams[ -1 ] = 'earliest'
			"maxResults": 50 # after 50 you have to start dealing with pageToken and pagnation stuff
		}
		url = f"https://www.googleapis.com/youtube/v3/search"
		response = requests.get( url , headers=headers , params=params )
		response.raise_for_status()
		live_streams = response.json()
		live_streams = [ {
			"id": x[ "id" ][ "videoId" ] ,
			"description": x[ "snippet" ][ "description" ] ,
			"title": x[ "snippet" ][ "title" ] ,
			"published_time": x[ "snippet" ][ "publishTime" ]
		} for x in live_streams[ "items" ] ]
		return live_streams
	except Exception as e:
		try:
			headers = { 'accept': 'application/json, text/plain, */*', }
			params = {
				"part": "snippet" ,
				"q": options[ 0 ] , # this would be if we wanted to 'search' 'MontereyBayAquarium' instead of using the channelId property
				# "channelId": options[ 0 ] ,
				"eventType": "live" ,
				"type": "video" ,
				"key": options[ 1 ] ,
				# "order": "viewCount" ,
				"order": "date" , # makes live_streams[ 0 ] = 'latest' and live_streams[ -1 ] = 'earliest'
				"maxResults": 50 # after 50 you have to start dealing with pageToken and pagnation stuff
			}
			url = f"https://www.googleapis.com/youtube/v3/search"
			response = requests.get( url , headers=headers , params=params )
			response.raise_for_status()
			live_streams = response.json()
			live_streams = [ {
				"id": x[ "id" ][ "videoId" ] ,
				"description": x[ "snippet" ][ "description" ] ,
				"title": x[ "snippet" ][ "title" ] ,
				"published_time": x[ "snippet" ][ "publishTime" ]
			} for x in live_streams[ "items" ] ]
			return live_streams
		except Exception as e:
			print( e )
			return False

def update_currated_live_streams( c2 ):
	# live_currated_following_key = f"{c2.config.redis.prefix}.APPS.YOUTUBE.FOLLOWING.CURRATED"
	live_currated_user_ids_set_key = f"{c2.config.redis.prefix}.APPS.YOUTUBE.FOLLOWING.CURRATED.LIVE.USER_IDS"
	live_currated_user_ids = c2.redis.redis.smembers( live_currated_user_ids_set_key )

	batch_option_list = [ [ x , c2.config.apps.youtube.personal.api_key ] for x in live_currated_user_ids ]
	live_streams = utils.batch_process({
		"max_workers": 5 ,
		"batch_list": batch_option_list ,
		"function_reference": one_hot_get_channel_live_streams
	})
	live_streams = [ x for x in live_streams if x ]

	youtube_currated_live_streams_key = f"{c2.config.redis.prefix}.APPS.YOUTUBE.FOLLOWING.CURRATED.LIVE.STREAMS"
	c2.redis.redis.delete( youtube_currated_live_streams_key )
	for i , x in enumerate( live_streams ):
		c2.redis.redis.rpush( youtube_currated_live_streams_key , json.dumps( x ) )
	return live_streams


def play_next_live_follower( c2 ):
	try:
		previous_state = c2.redis.get_state()
		adb = ADBWrapper( { "ip": c2.config.adb.ip , "port": c2.config.adb.port } )
		previous_adb_status = adb.get_status()

		live_currated_following_key = f"{c2.config.redis.prefix}.APPS.YOUTUBE.FOLLOWING.CURRATED"
		if previous_state[ "name" ] != "youtube":
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

		uri = f"youtube://play/{next_live_user}"
		print( f"ADB :: Launching :: {uri}" )
		adb.open_uri( uri )
		new_adb_status = adb.get_status()

		# make sure chat is open or closed ??
		# adb.press_key_sequence( [ asdf , asdf , ... ] )

		new_state = {
			"name": "youtube" ,
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
			"adb_status": new_adb_status ,
		}
		return result
	except Exception as e:
		print( stackprinter.format() )
		c2.log( e )
		return False


def play_next_currated_normal_playlist( c2 ):
	try:
		previous_state = c2.redis.get_state()
		adb = ADBWrapper( { "ip": c2.config.adb.ip , "port": c2.config.adb.port } )
		previous_adb_status = adb.get_status()

		youtube_currated_normal_playlist_key = f"{c2.config.redis.prefix}.APPS.YOUTUBE.CURRATED.PLAYLISTS.NORMAL"
		next_currated_normal_playlist = redis_circular_list.next( c2.redis.redis , youtube_currated_normal_playlist_key )
		print( next_currated_normal_playlist )
		# uri = f"youtube://play"
		# uri = f"vnd.youtube:https://www.youtube.com/playlist?list={next_currated_normal_playlist}"

		# https://www.youtube.com/watch?v=CihSRS1QL9c&list=PLcW8xNfZoh7edcaS0eHykgKNHhV9oXX4d&index=1
		# https://www.youtube.com/playlist?list=PLcW8xNfZoh7edcaS0eHykgKNHhV9oXX4d
		# https://www.youtube.com/watch?v=CihSRS1QL9c&list=PLcW8xNfZoh7edcaS0eHykgKNHhV9oXX4d&index=1
		# uri = f"https://youtube.com/playlist?list={next_currated_normal_playlist}"
		# uri = f"vnd.youtube://{next_currated_normal_playlist}"
		# uri = f"https://www.youtube.com/watch?v=CihSRS1QL9c&list={next_currated_normal_playlist}&index=1"
		# uri = f"https://www.youtube.com/watch?v=CihSRS1QL9c&list={next_currated_normal_playlist}&index=1"

		# uri = f"vnd.youtube:playlist/{next_currated_normal_playlist}"
		# uri = f"vnd.youtube://playlist/{next_currated_normal_playlist}"
		uri = f"http://www.youtube.com/watch?v=QjVLMU9MdOY"
		print( f"ADB :: Launching :: {uri}" )
		adb.open_uri( uri )

	    # "KEYCODE_CUT": 277 ,
	    # "KEYCODE_COPY": 278 ,
	    # "KEYCODE_PASTE": 279 ,

		# copy_text_result = adb.exec( f'adb shell service call clipboard 2 i32 1 i32 0 s16 "{next_currated_normal_playlist}"' )
		# print( copy_text_result )
		# time.sleep( 2 )
		# adb.press_key( 279 )


		new_adb_status = adb.get_status()

		# make sure chat is open or closed ??
		# adb.press_key_sequence( [ asdf , asdf , ... ] )

		new_state = {
			"name": "youtube" ,
			"function": "play_next_currated_normal_playlist" ,
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
			"adb_status": new_adb_status ,
		}
		return result
	except Exception as e:
		print( stackprinter.format() )
		c2.log( e )
		return False


def play_next_currated_normal_video( c2 ):
	try:
		previous_state = c2.redis.get_state()
		adb = ADBWrapper( { "ip": c2.config.adb.ip , "port": c2.config.adb.port } )
		previous_adb_status = adb.get_status()

		youtube_currated_normal_video_key = f"{c2.config.redis.prefix}.APPS.YOUTUBE.CURRATED.VIDEOS.NORMAL"
		next_currated_normal_video = redis_circular_list.next( c2.redis.redis , youtube_currated_normal_video_key )
		uri = f"http://www.youtube.com/watch?v={next_currated_normal_video}"
		print( f"ADB :: Launching :: {uri}" )
		adb.open_uri( uri )
		new_adb_status = adb.get_status()
		new_state = {
			"name": "youtube" ,
			"function": "play_next_currated_normal_video" ,
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
			"adb_status": new_adb_status ,
		}
		return result
	except Exception as e:
		print( stackprinter.format() )
		c2.log( e )
		return False

def play_next_currated_live_video( c2 ):
	try:
		previous_state = c2.redis.get_state()
		adb = ADBWrapper( { "ip": c2.config.adb.ip , "port": c2.config.adb.port } )
		previous_adb_status = adb.get_status()

		youtube_currated_live_video_key = f"{c2.config.redis.prefix}.APPS.YOUTUBE.CURRATED.VIDEOS.LIVE"
		next_currated_live_video = redis_circular_list.next( c2.redis.redis , youtube_currated_live_video_key )
		uri = f"http://www.youtube.com/watch?v={next_currated_live_video}"
		print( f"ADB :: Launching :: {uri}" )
		adb.open_uri( uri )
		new_adb_status = adb.get_status()
		new_state = {
			"name": "youtube" ,
			"function": "play_next_currated_live_video" ,
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
			"adb_status": new_adb_status ,
		}
		return result
	except Exception as e:
		print( stackprinter.format() )
		c2.log( e )
		return False