import yaml
import redis
import signal
import datetime
import inspect

# https://github.com/0187773933/PowerPointInteractiveGamesGenerator/blob/ec49a26e6aae66fadda40ffa3b74a2e5e6f6e6e3/utils.py
# https://github.com/0187773933/RaspiCameraMotionTrackerFrameConsumer/blob/master/frame_consumer.py

def write_yaml( file_path , python_object ):
	with open( file_path , 'w' , encoding='utf-8' ) as f:
		yaml.dump( python_object , f )

def read_yaml( file_path ):
	with open( file_path ) as f:
		return yaml.safe_load( f )

def setup_signal_handlers( function_pointer ):
	signal.signal( signal.SIGABRT , function_pointer )
	signal.signal( signal.SIGFPE , function_pointer )
	signal.signal( signal.SIGILL , function_pointer )
	signal.signal( signal.SIGSEGV , function_pointer )
	signal.signal( signal.SIGTERM , function_pointer )
	signal.signal( signal.SIGINT , function_pointer )

def redis_connect( host , port , db , password ):
	return redis.StrictRedis(
		host=host ,
		port=port ,
		db=db ,
		password=password ,
		decode_responses=True
	)

def get_redis_log_date( as_timezone ):
	now = datetime.datetime.now().astimezone( as_timezone )
	return now.strftime( "%Y.%m.%d" ).upper()

def get_common_time_string( as_timezone ):
	now = datetime.datetime.now().astimezone( as_timezone )
	milliseconds = round( now.microsecond / 1000.0 )
	milliseconds = str( milliseconds ).zfill( 3 )
	now_string = now.strftime( "%d%b%Y === %H:%M:%S" ).upper()
	return f"{now_string}.{milliseconds}"

# https://stackoverflow.com/q/15608987
def reach( name ):
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