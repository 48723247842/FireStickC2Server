import stackprinter
import time
from pprint import pprint

import redis_circular_list

from ADBWrapper import ADBWrapper
from PIL import Image
from pathlib import Path

import utils

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

		## TODO === check if out of bounds , and reset across negative difference
		# "/Users/morpheous/WORKSPACE/PYTHON/FireStickC2Server/venv/lib/python3.9/site-packages/PIL/Image.py", line 1206
		# if box[2] < box[0]:
		#     raise ValueError("Coordinate 'right' is less than 'left'")
		# elif box[3] < box[1]:
		#     raise ValueError("Coordinate 'lower' is less than 'upper'")

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

		adb.press_key( 87 ) # press media 'next' key
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
		result = {
			"previous_state": previous_state ,
			"previous_adb_status": previous_adb_status ,
			"adb_opened_uri": uri ,
			"new_adb_status": new_adb_status
		}
		return result
	except Exception as e:
		print( stackprinter.format() )
		c2.log( e )
		return False