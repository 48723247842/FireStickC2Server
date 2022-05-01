from box import Box
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
		self.redis.set( f"{self.config.prefix}.STATE" , json.dumps( state_object ) )

	def get_state( self ):
		return json.loads( self.redis.get( f"{self.config.prefix}.STATE" ) )