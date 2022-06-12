import stackprinter
import time
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

		# this is why we need find grain control
		# spotify does not respect 'KEYCODE_MEDIA_PREVIOUS'
		# adb.press_key( 88 )
		# so we have to go all the way to the left , then right two , then enter twice
		adb.press_key_sequence( [ 21 , 21 , 21 , 21 , 21 , 21 ] )
		# time.sleep( 0.5 )
		adb.press_key_sequence( [ 22 , 22 ] )
		# time.sleep( 0.5 )
		adb.press_key_sequence( [ 23 , 23 ] )

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
			"name": "spotify" ,
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
	try:
		print( "shuffle_on" )
		previous_state = c2.redis.get_state()
		adb = ADBWrapper( { "ip": c2.config.adb.ip , "port": c2.config.adb.port } )
		previous_adb_status = adb.get_status()

		_enable_shuffle( adb )

		time.sleep( 0.5 )
		new_adb_status = adb.get_status()

		result = {
			"name": "spotify" ,
			"function": "shuffle_on" ,
			"time": utils.get_common_time_string( c2.config.time_zone ) ,
			"adb_status": new_adb_status
		}
		c2.redis.set_state( result )
	except Exception as e:
		print( stackprinter.format() )
	return result

def shuffle_off( c2 ):
	result = {}
	try:
		print( "shuffle_off" )
		previous_state = c2.redis.get_state()
		adb = ADBWrapper( { "ip": c2.config.adb.ip , "port": c2.config.adb.port } )
		previous_adb_status = adb.get_status()

		_disable_shuffle( adb )

		time.sleep( 0.5 )
		new_adb_status = adb.get_status()

		result = {
			"name": "spotify" ,
			"function": "shuffle_on" ,
			"time": utils.get_common_time_string( c2.config.time_zone ) ,
			"adb_status": new_adb_status
		}
		c2.redis.set_state( result )
	except Exception as e:
		print( stackprinter.format() )
	return result

def _enable_shuffle( adb ):
	try:
		status = adb.get_status()
		frame_geometry = status[ "window_stack" ][ 0 ][ "frame_geometry" ]
		frame_geometry = " ".join( " ".join( frame_geometry.split( "," ) ).split( "[" ) ).split( "]" )
		frame_geometry = [ x.strip().split( " " ) for x in frame_geometry if x ]
		frame_geometry = frame_geometry[ 1 ]
		print( frame_geometry )
		adb.press_key_sequence( [ 21 , 21 , 21 , 21 , 21 , 21 ] ) # ensures we start all the way to the left
		# adb.press_key_sequence( [ 22 , 23 , ad ] )
		adb.press_key( 22 )
		# time.sleep( 1 )
		# adb.press_key( 23 )
		# time.sleep( 1 )
		adb.take_screen_shot()
		print( adb.screen_shot.size )
		# adb.screen_shot.show()

		# ( left , uppper , right , lower )
		# configure these
		origin = [ 616 , 922 ]
		size = [ 80 , 80 ]

		# then calculate lower-right coordinate
		other_position = [ ( origin[ 0 ] + size[ 0 ] ) , ( origin[ 1 ] + size[ 1 ] ) ]
		cropped_shuffle_symbol = adb.screen_shot.crop( ( origin[ 0 ] , origin[ 1 ] , other_position[ 0 ] , other_position[ 1 ] ) )
		# cropped_shuffle_symbol.show()

		spotify_shuffle_true_image_path = Path.cwd().joinpath( "state_functions" , "images" , "spotify_shuffle_true.png" ).resolve()
		spotify_shuffle_false_image_path = Path.cwd().joinpath( "state_functions" , "images" , "spotify_shuffle_false.png" ).resolve()

		shuffle_true_image = Image.open( spotify_shuffle_true_image_path )
		shuffle_false_image = Image.open( spotify_shuffle_false_image_path )

		true_difference = utils.difference_between_two_images( cropped_shuffle_symbol , shuffle_true_image )
		false_difference = utils.difference_between_two_images( cropped_shuffle_symbol , shuffle_false_image )
		differences = {
			"true" :  true_difference,
			"false": false_difference ,
			true_difference: True ,
			false_difference: False
		}
		differences[ "closest_value" ] = min( differences[ "true" ] , differences[ "false" ] )
		differences[ "closest" ] = differences[ differences[ "closest_value" ] ]
		# pprint( differences )

		shuffled_enabled = differences[ "closest" ]
		if shuffled_enabled == False:
			print( "Enabling Shuffle" )
			adb.press_key( 23 )
			time.sleep( 0.5 )
		return True
	except Exception as e:
		print( stackprinter.format() )
		return False


def _disable_shuffle( adb ):
	try:
		status = adb.get_status()
		frame_geometry = status[ "window_stack" ][ 0 ][ "frame_geometry" ]
		frame_geometry = " ".join( " ".join( frame_geometry.split( "," ) ).split( "[" ) ).split( "]" )
		frame_geometry = [ x.strip().split( " " ) for x in frame_geometry if x ]
		frame_geometry = frame_geometry[ 1 ]
		print( frame_geometry )
		adb.press_key_sequence( [ 21 , 21 , 21 , 21 , 21 , 21 ] ) # ensures we start all the way to the left
		# adb.press_key_sequence( [ 22 , 23 , ad ] )
		adb.press_key( 22 )
		# time.sleep( 1 )
		# adb.press_key( 23 )
		# time.sleep( 1 )
		adb.take_screen_shot()
		print( adb.screen_shot.size )
		# adb.screen_shot.show()

		# ( left , uppper , right , lower )
		# configure these
		origin = [ 616 , 922 ]
		size = [ 80 , 80 ]

		# then calculate lower-right coordinate
		other_position = [ ( origin[ 0 ] + size[ 0 ] ) , ( origin[ 1 ] + size[ 1 ] ) ]
		cropped_shuffle_symbol = adb.screen_shot.crop( ( origin[ 0 ] , origin[ 1 ] , other_position[ 0 ] , other_position[ 1 ] ) )
		# cropped_shuffle_symbol.show()

		spotify_shuffle_true_image_path = Path.cwd().joinpath( "state_functions" , "images" , "spotify_shuffle_true.png" ).resolve()
		spotify_shuffle_false_image_path = Path.cwd().joinpath( "state_functions" , "images" , "spotify_shuffle_false.png" ).resolve()

		shuffle_true_image = Image.open( spotify_shuffle_true_image_path )
		shuffle_false_image = Image.open( spotify_shuffle_false_image_path )

		true_difference = utils.difference_between_two_images( cropped_shuffle_symbol , shuffle_true_image )
		false_difference = utils.difference_between_two_images( cropped_shuffle_symbol , shuffle_false_image )
		differences = {
			"true" :  true_difference,
			"false": false_difference ,
			true_difference: True ,
			false_difference: False
		}
		differences[ "closest_value" ] = min( differences[ "true" ] , differences[ "false" ] )
		differences[ "closest" ] = differences[ differences[ "closest_value" ] ]
		# pprint( differences )

		shuffled_enabled = differences[ "closest" ]
		if shuffled_enabled == True:
			print( "Disabling Shuffle" )
			adb.press_key( 23 )
			time.sleep( 0.5 )
		return True
	except Exception as e:
		print( stackprinter.format() )
		return False


def play_next_currated_playlist( c2 ):
	try:
		previous_state = c2.redis.get_state()
		adb = ADBWrapper( { "ip": c2.config.adb.ip , "port": c2.config.adb.port } )
		previous_adb_status = adb.get_status()
		next_curred_playlist = redis_circular_list.next( c2.redis.redis , f"{c2.config.redis.prefix}.APPS.SPOTIFY.PLAYLISTS.CURRATED" )
		# https://open.spotify.com/playlist/75igTPKAdDsBYFtYCHO555
		uri = f"spotify:playlist:{next_curred_playlist}:play"
		print( f"ADB :: Launching :: {uri}" )
		adb.open_uri( uri )
		new_adb_status = adb.get_status()
		_enable_shuffle( adb )
		adb.press_key( 87 ) # press media 'next' key to start shuffle
		new_state = {
			"name": "spotify" ,
			"function": "play_next_currated_playlist" ,
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