from box import Box
from pprint import pprint
import redis
import datetime
from pytz import timezone
import json

class RedisWrapper:
	def __init__( self , config={} ):
		self.config = config
		self.config.time_zone = timezone( self.config.time_zone )
		self.connect()

	def connect( self ):
		self.redis = redis.StrictRedis(
			host=self.config.host ,
			port=self.config.port ,
			db=self.config.db ,
			password=self.config.password ,
			decode_responses=True
		)

	def get_log_date_prefix( self ):
		now = datetime.datetime.now().astimezone( self.config.time_zone )
		return now.strftime( "%Y.%m.%d" ).upper()

	def log( self , message ):
		log_date_prefix = self.get_log_date_prefix()
		log_key = f"{self.config.prefix}.LOG.{log_date_prefix}"
		self.redis.rpush( log_key , message )

	def set_state( self , state_object ):
		# pprint( state_object )
		self.redis.set( f"{self.config.prefix}.STATE" , json.dumps( state_object ) )

	def get_state( self ):
		return json.loads( self.redis.get( f"{self.config.prefix}.STATE" ) )

	def push_state_list( self , state_object ):
		list_key = f"{self.config.prefix}.STATE_LIST"
		self.redis.rpush( list_key , json.dumps( state_object ) )
		length = self.redis.llen( list_key )
		if length > 100:
			self.redis.lpop( list_key )
		return json.loads( self.redis.get( f"{self.config.prefix}.STATE" ) )

	def get_state_list_last_two( self ):
		list_key = f"{self.config.prefix}.STATE_LIST"
		last_two = self.redis.lrange( list_key , -2 , -1 )
		return {
			"previous": json.loads( last_two[ 0 ] ) ,
			"current": json.loads( last_two[ 1 ] )
		}