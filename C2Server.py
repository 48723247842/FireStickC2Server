import sys
import stackprinter
import utils
from box import Box
from pytz import timezone
import time

from sanic import Sanic
from sanic.response import json as sanic_json
from sanic import response
from sanic.signals import Event as sanic_event

from routes.misc import misc_blueprint

class C2Server:
	def __init__( self , options={} ):
		try:
			self.options = Box( options )
			self.config = Box( utils.read_yaml( self.options.config_file_path ) )
			self.config.time_zone = timezone( self.config.time_zone )
			utils.setup_signal_handlers( self.on_signal_interrupt )
			self.redis = utils.redis_connect( self.config.redis.host , self.config.redis.port , self.config.redis.db , self.config.redis.password )
			print( self.config )
		except Exception as e:
			self.log( stackprinter.format() )
			sys.exit( 1 )

	def on_signal_interrupt( self , signal_number , signal ):
		self.log( f"Fire Stick C2 Server Received Interrupt === {str(signal)}" )
		self.stop()

	def log( self , log_message ):
		try:
			now_string = utils.get_common_time_string( self.config.time_zone )
			log_message = f"{now_string} === {log_message}"
			redis_log_date = utils.get_redis_log_date( self.config.time_zone )
			redis_log_key = f"{self.config.redis.prefix}LOG.{redis_log_date}"
			# self.redis.rpush( redis_log_key , log_message )
			print( log_message )
		except Exception as e:
			print( stackprinter.format() )

	def start( self ):
		try:
			self.log( f"Fire Stick C2 Server Starting" )

			# https://sanic.dev/en/guide/advanced/signals.html#built-in-signals
			# self.app.add_signal( self.stop , "boo.bar.baz" )
			# self.app.signal( event="server.shutdown.after" )( self.stop )
			# don't ask , fucking decorators
			app = Sanic( name="FireStick-C2-Server" )
			@app.signal( "server.shutdown.after" )
			def _shutdown( *args , **kwargs ):
				self.stop()
			self.app = app

			self.app.blueprint( misc_blueprint )
			self.app.run( host=self.config.sanic.host , port=self.config.sanic.port )
		except Exception as e:
			self.log( stackprinter.format() )
			self.stop()

	def stop( self , *args ):
		self.log( f"Fire Stick C2 Server Stopping" )
		# sys.exit( 1 ) # this throws error , because sanic is calling loop.run_until_complete(app._server_event("shutdown", "after"))