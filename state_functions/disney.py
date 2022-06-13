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
			"name": "disney" ,
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

def play_next_currated_video_random( c2 ):
	try:
		previous_state = c2.redis.get_state()
		adb = ADBWrapper( { "ip": c2.config.adb.ip , "port": c2.config.adb.port } )
		previous_adb_status = adb.get_status()

		disney_videos_currated_random_key = f"{c2.config.redis.prefix}.APPS.DISNEY.VIDEOS.CURRATED.RANDOM"
		disney_videos_currated_random_watched_key = f"{c2.config.redis.prefix}.APPS.DISNEY.VIDEOS.CURRATED.RANDOM.WATCHED"
		next_currated_random_video_id = c2.redis.redis.srandmember( disney_videos_currated_random_key )
		c2.redis.redis.srem( disney_videos_currated_random_key , next_currated_random_video_id )
		c2.redis.redis.sadd( disney_videos_currated_random_watched_key , next_currated_random_video_id )

		uri = f"https://www.disneyplus.com/video/{next_currated_random_video_id}"
		print( f"ADB :: Launching :: {uri}" )
		adb.open_uri( uri )
		new_adb_status = adb.get_status()

		# restarts from the last watched position
		# so need to rewind ???
		time.sleep( 7 )
		adb.press_key_sequence( [ 21 , 21 , 21 , 21 , 21 , 23 , 23 , 23 ] )


		new_state = {
			"name": "disney" ,
			"function": "play_next_currated_video_random" ,
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