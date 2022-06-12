import yaml
import redis
import signal
import datetime
import inspect
import imagehash
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


# Manually Sets Required Stuff For State Functions
def store_config_in_db( config , redis ):
	## Spotify - Set Currated Playlists
	currated_playlists_list_key = f"{config.redis.prefix}.APPS.SPOTIFY.PLAYLISTS.CURRATED"
	redis.redis.delete( currated_playlists_list_key )
	for i , x in enumerate( config.apps.spotify.playlists.currated ):
		redis.redis.rpush( currated_playlists_list_key , x )


def difference_between_two_images( pil_image_1 , pil_image_2 ):
	pil_image_1_hash = imagehash.phash( pil_image_1 )
	pil_image_2_hash = imagehash.phash( pil_image_2 )
	difference = ( pil_image_1_hash - pil_image_2_hash )
	return difference


