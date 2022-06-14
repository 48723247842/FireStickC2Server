import sys
import stackprinter
import utils
from RedisWrapper import RedisWrapper
from box import Box
from pytz import timezone

from sanic import Sanic
from sanic.response import json as sanic_json
from sanic import response
from sanic.signals import Event as sanic_event

from routes.misc import misc_blueprint
from routes.button import button_blueprint
from routes.stream_deck import streamdeck_blueprint

from routes.twitch import twitch_blueprint
from routes.youtube import youtube_blueprint

# https://stackoverflow.com/questions/59434725/retrieve-call-logs-android-throught-adb
# https://stackoverflow.com/questions/29099061/sending-intent-using-adb
# https://stackoverflow.com/questions/29099061/sending-intent-using-adb#29103873
# adb shell am start -a barcodescanner.RECVR -c android.intent.category.DEFAULT -n WMSMobileApp.WMSMobileApp/wmsmobileapp.activities.MainActivity -e com.motorolasolutions.emdk.datawedge.source scanner -e com.motorolasolutions.emdk.datawedge.data_string 508919007526
# https://stackoverflow.com/questions/49159172/how-to-pass-intent-data-when-starting-app-via-adb
# https://www.xgouchet.fr/android/index.php?article42/launch-intents-using-adb

# discover Intents buried in .apk files
# https://developer.android.com/training/app-links/deep-linking
# https://f-droid.org/en/packages/com.oF2pks.applicationsinfo/
	# com.amazon.firetv.youtube
# adb shell pm list packages
# adb shell pm path com.amazon.firetv.youtube
	# package:/data/app/com.amazon.firetv.youtube-w7soWc29LVuZZsacd3FOzQ==/base.apk
# adb pull /data/app/com.amazon.firetv.youtube-w7soWc29LVuZZsacd3FOzQ==/base.apk firetv-youtube.apk
# /Users/morpheous/Library/Android/sdk/build-tools/30.0.2/aapt d xmltree firetv-youtube.apk AndroidManifest.xml

# com.amazon.firetv.youtube
# 	Activities =
# 		com.google.android.gms.common.api.GoogleApi.Activity
# 		dev.cobalt.app.MainActivity
# 		dev.cobalt.coat.MediaPlaybackService

# StreamDeck.py should be sanic server
# for restart , blank screen but still on , etc

class C2Server:
	def __init__( self , options={} ):
		try:
			self.options = Box( options )
			self.config = Box( utils.read_yaml( self.options.config_file_path ) )
			self.config.time_zone = timezone( self.config.redis.time_zone )
			utils.setup_signal_handlers( self.on_signal_interrupt )
			self.redis = RedisWrapper( self.config.redis )
			print( self.config )
			utils.store_config_in_db( self.config , self.redis )
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
			self.redis.log( log_message )
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
			# self.redis.set_state({
			# 	"status": "online" ,
			# 	"time": utils.get_common_time_string( self.config.time_zone )
			# })
			# print( self.redis.get_state() )
			self.app.blueprint( misc_blueprint )
			self.app.blueprint( button_blueprint )
			self.app.blueprint( streamdeck_blueprint )

			self.app.blueprint( twitch_blueprint )
			self.app.blueprint( youtube_blueprint )
			self.log( "Server Online" )
			self.app.run( host=self.config.sanic.host , port=self.config.sanic.port )
		except Exception as e:
			self.log( stackprinter.format() )
			self.stop()

	def stop( self , *args , **kwargs ):
		self.log( "Server Offline" )
		# sys.exit( 1 ) # this throws error , because sanic is calling loop.run_until_complete(app._server_event("shutdown", "after"))