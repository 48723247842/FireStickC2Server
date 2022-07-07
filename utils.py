import time
import yaml
import redis
import signal
import datetime
import inspect
from PIL import Image
import imagehash
import imgcompare
from box import Box
import requests
from pprint import pprint
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# https://github.com/0187773933/PowerPointInteractiveGamesGenerator/blob/ec49a26e6aae66fadda40ffa3b74a2e5e6f6e6e3/utils.py
# https://github.com/0187773933/RaspiCameraMotionTrackerFrameConsumer/blob/master/frame_consumer.py

def write_yaml( file_path , python_object ):
	with open( file_path , 'w' , encoding='utf-8' ) as f:
		yaml.dump( python_object , f )

def read_yaml( file_path ):
	with open( file_path ) as f:
		return yaml.safe_load( f )

def batch_process( options ):
	batch_size = len( options[ "batch_list" ] )
	with ThreadPoolExecutor() as executor:
		result_pool = list( tqdm( executor.map( options[ "function_reference" ] , iter( options[ "batch_list" ] ) ) , total=batch_size ) )
		return result_pool

def setup_signal_handlers( function_pointer ):
	signal.signal( signal.SIGABRT , function_pointer )
	signal.signal( signal.SIGFPE , function_pointer )
	signal.signal( signal.SIGILL , function_pointer )
	signal.signal( signal.SIGSEGV , function_pointer )
	signal.signal( signal.SIGTERM , function_pointer )
	signal.signal( signal.SIGINT , function_pointer )

def get_common_time_string( as_timezone ):
	now = datetime.datetime.now().astimezone( as_timezone )
	milliseconds = round( now.microsecond / 1000.0 )
	milliseconds = str( milliseconds ).zfill( 3 )
	now_string = now.strftime( "%d%b%Y === %H:%M:%S" ).upper()
	return f"{now_string}.{milliseconds}"

# https://stackoverflow.com/q/15608987
def stack_reach( name ):
	for f in inspect.stack():
		if name in f[ 0 ].f_locals:
			return f[ 0 ].f_locals[ name ]
	return None

def get_server_context():
	for f in inspect.stack():
		if "__name__" not in f[ 0 ].f_locals:
			continue
		if "server" not in f[ 0 ].f_locals:
			continue
		return f[ 0 ].f_locals[ "server" ]
	return False

def difference_between_two_images( pil_image_1 , pil_image_2 ):
	pil_image_1_hash = imagehash.phash( pil_image_1 )
	pil_image_2_hash = imagehash.phash( pil_image_2 )
	difference = ( pil_image_1_hash - pil_image_2_hash )
	return difference
	# return imgcompare.image_diff_percent( pil_image_1 , pil_image_2 )

# options = {
# 	"adb": adb_object ,
# 	"file_path": "/path/to/screenshot/of/screen/we/are/comparing/to.png" ,
# 	"cropping": {
# 		"origin": [ 616 , 922 ] ,
# 		"size": [ 80 , 80 ]
# 	}
# 	"tolerance_threshold": 2.5 ,
# 	"time_out_milliseconds": 20000 ,
# 	"check_interval_milliseconds": 500 ,
# }
def wait_on_screen( options ):
	options = Box( options )
	pprint( options )
	if options.cropping != False:
		options.cropping.other_position = [ ( options.cropping.origin[ 0 ] + options.cropping.size[ 0 ] ) , ( options.cropping.origin[ 1 ] + options.cropping.size[ 1 ] ) ]
	start = datetime.datetime.now()
	compare_image = Image.open( options.file_path )
	found = False
	while found == False:
		options.adb.take_screen_shot()
		if "other_position" in options.cropping:
			options.adb.screen_shot = options.adb.screen_shot.crop( ( options.cropping.origin[ 0 ] , options.cropping.origin[ 1 ] , options.cropping.other_position[ 0 ] , options.cropping.other_position[ 1 ] ) )
		# is_same = imgcompare.is_equal( options.adb.screen_shot , compare_image , tolerance=options.tolerance_threshold )
		# if is_same == True:
		# 	found = True
		difference = imgcompare.image_diff_percent( options.adb.screen_shot , compare_image ) # faster , but less acurate than image-hash ?
		print( f"Difference === {difference}" )
		if difference < options.tolerance_threshold:
			# options.adb.screen_shot.show()
			found = True
		else:
			now = datetime.datetime.now()
			duration_milliseconds = ( ( now - start ).total_seconds() * 1000 )
			if duration_milliseconds > options.time_out_milliseconds:
				return False
			print( f"Sleeping for {options.check_interval_milliseconds} milliseconds" )
			options.adb.screen_shot.show()
			# compare_image.show()
			time.sleep( ( options.check_interval_milliseconds / 1000 ) )
			# time.sleep( 30 )
	return True

# The opposite of wait_on_screen()
# this waits for the distance to be great enough that the screen is considered to have been removed/cleared
# def wait_on_screen_to_clear( options ):
# 	options = Box( options )
# 	start = datetime.datetime.now()
# 	screen_image = Image.open( options.file_path )
# 	found = False
# 	while found == False:
# 		time.sleep(  )

def _youtube_get_channel_id( options ):
	try:
		headers = { "accept": "application/json, text/plain, */*" }
		params = {
			"part": "id" ,
			"forUsername": options[ 0 ] ,
			"key": options[ 1 ]
		}
		url = f"https://www.googleapis.com/youtube/v3/channels"
		response = requests.get( url , headers=headers , params=params )
		response.raise_for_status()
		result = response.json()
		if "items" not in result:
			# print( "\nCouldn't find ID , trying /v3/members" )
			# result = _youtube_get_member_info( options )
			# pprint( result )
			# print( options )
			# return False
			return { options[ 0 ]: options[ 0 ] }
		channel_id = result[ "items" ][ 0 ][ "id" ]
		return { options[ 0 ]: channel_id }
	except Exception as e:
		print( e )
		return { options[ 0 ]: options[ 0 ] }


# Manually Sets Required Stuff For State Functions
def store_config_in_db( config , redis ):

	## STEP-1 === Spotify - Set Currated Playlists
	spotify_currated_playlists_list_key = f"{config.redis.prefix}.APPS.SPOTIFY.PLAYLISTS.CURRATED"
	redis.redis.delete( spotify_currated_playlists_list_key )
	for i , x in enumerate( config.apps.spotify.playlists.currated ):
		redis.redis.rpush( spotify_currated_playlists_list_key , x )

	## ON HOLD UNTIL YOUTUBE API LIMITS
	# ## STEP-2 === YouTube - Get Channel IDS For All Currated-Live-Channels
	# youtube_currated_live_channel_ids = batch_process({
	# 	"max_workers": 5 ,
	# 	"batch_list": [ [ x , config.apps.youtube.personal.api_key ] for x in config.apps.youtube.following.currated.live ] ,
	# 	"function_reference": _youtube_get_channel_id
	# })
	# youtube_currated_live_channel_ids = [ x for x in youtube_currated_live_channel_ids if x ]
	# youtube_currated_live_channel_ids_key = f"{config.redis.prefix}.APPS.YOUTUBE.FOLLOWING.CURRATED.LIVE.USER_IDS"
	# redis.redis.delete( youtube_currated_live_channel_ids_key )
	# for i , x in enumerate( youtube_currated_live_channel_ids ):
	# 	# MAYBE TODO = base64 encode usernames for redis key ???
	# 	channel_name = list( x.keys() )[ 0 ]
	# 	redis.redis.sadd( youtube_currated_live_channel_ids_key , x[ channel_name ] )

	# ## STEP-3 === YouTube - Get Channel IDS For All Currated-Normal-Channels
	# youtube_currated_normal_channel_ids = batch_process({
	# 	"max_workers": 5 ,
	# 	"batch_list": [ [ x , config.apps.youtube.personal.api_key ] for x in config.apps.youtube.following.currated.normal ] ,
	# 	"function_reference": _youtube_get_channel_id
	# })
	# youtube_currated_normal_channel_ids = [ x for x in youtube_currated_normal_channel_ids if x ]
	# youtube_currated_normal_channel_ids_key = f"{config.redis.prefix}.APPS.YOUTUBE.FOLLOWING.CURRATED.NORMAL.USER_IDS"
	# redis.redis.delete( youtube_currated_normal_channel_ids_key )
	# for i , x in enumerate( youtube_currated_normal_channel_ids ):
	# 	# MAYBE TODO = base64 encode usernames for redis key ???
	# 	channel_name = list( x.keys() )[ 0 ]
	# 	redis.redis.sadd( youtube_currated_normal_channel_ids_key , x[ channel_name ] )


	## STEP-4 == YouTube - Store - Currated - Normal - Playlists - FOR - StreamDeck - Button 3
	youtube_currated_normal_playlist_key = f"{config.redis.prefix}.APPS.YOUTUBE.CURRATED.PLAYLISTS.NORMAL"
	redis.redis.delete( youtube_currated_normal_playlist_key )
	for i , x in enumerate( config.apps.youtube.playlists.currated.normal ):
		redis.redis.rpush( youtube_currated_normal_playlist_key , x )

	## STEP-5 == YouTube - Store - Currated - Normal - Videos - FOR - StreamDeck - Button 3
	youtube_currated_normal_videos_key = f"{config.redis.prefix}.APPS.YOUTUBE.CURRATED.VIDEOS.NORMAL"
	redis.redis.delete( youtube_currated_normal_videos_key )
	for i , x in enumerate( config.apps.youtube.videos.currated.normal ):
		redis.redis.rpush( youtube_currated_normal_videos_key , x )

	## STEP-6 == YouTube - Store - Currated - Live - Videos - FOR - StreamDeck - Button 3
	youtube_currated_live_videos_key = f"{config.redis.prefix}.APPS.YOUTUBE.CURRATED.VIDEOS.LIVE"
	redis.redis.delete( youtube_currated_live_videos_key )
	for i , x in enumerate( config.apps.youtube.videos.currated.live ):
		redis.redis.rpush( youtube_currated_live_videos_key , x )

	## STEP-7 == Disney - Store - Currated - Random - Video IDS - FOR - StreamDeck - Button 4
	disney_videos_currated_random_key = f"{config.redis.prefix}.APPS.DISNEY.VIDEOS.CURRATED.RANDOM"
	disney_videos_currated_random_watched_key = f"{config.redis.prefix}.APPS.DISNEY.VIDEOS.CURRATED.RANDOM.WATCHED"
	disney_videos_currated_random_watched_temp_key = f"{config.redis.prefix}.APPS.DISNEY.VIDEOS.CURRATED.RANDOM.WATCHED.TEMP"
	redis.redis.delete( disney_videos_currated_random_key )
	# for i , x in enumerate( config.apps.disney.videos.currated ):
	# 	redis.redis.sadd( disney_videos_currated_random_key , x )
	step_7_pipeline = redis.redis.pipeline()
	for i , x in enumerate( config.apps.disney.videos.currated ):
		step_7_pipeline.sadd( disney_videos_currated_random_key , x )
	step_7_pipeline.execute()
	redis.redis.sdiffstore( disney_videos_currated_random_watched_temp_key , disney_videos_currated_random_key , disney_videos_currated_random_watched_key )
	total_unwatched = redis.redis.scard( disney_videos_currated_random_watched_temp_key )
	if int( total_unwatched ) > 0:
		redis.redis.delete( disney_videos_currated_random_key )
		redis.redis.rename( disney_videos_currated_random_watched_temp_key , disney_videos_currated_random_key )


def setup_tv( tv_controller ):
	try:
		tv_controller.set_input( "HDMI_1" )
		tv_controller.set_volume( 11 )
		return True
	except Exception as e:
		print( e )
		return False



