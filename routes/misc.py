from pprint import pprint
import json
import copy

from sanic import Blueprint
from sanic.response import json as json_result
from sanic import response as sanic_response

from ADBWrapper import ADBWrapper

import utils

import state_functions.twitch as twitch

misc_blueprint = Blueprint( "misc_blueprint" , url_prefix="/" )

async def home( request ):
	this = utils.get_server_context()
	print( this.config )
	return sanic_response.text( "you found the Fire Stick C2 Server !!\n" )

def _update_all():
	this = utils.get_server_context()

	# twitch
	live_users_currated = twitch.update_live_users_currated( this )

	# TODO = youtube

	result = {
		"update_results": {
			"twitch": {
				"live_users_currated": live_users_currated
			} ,
			"youtube": {
				"live_streams": False
			}
		} ,
		"status": {
			"state": current_state ,
			"adb": adb_status ,
		}
	}
	return

async def update_all( request ):
	this = utils.get_server_context()

	# twitch
	live_users_currated = twitch.update_live_users_currated( this )

	# TODO = youtube

	state_status = _status()
	result = {
		"update_results": {
			"twitch": {
				"live_users_currated": live_users_currated
			} ,
			"youtube": {
				"live_streams": False
			}
		} ,
		"status": state_status
	}
	return json_result( result )

def _status():
	this = utils.get_server_context()
	current_state = this.redis.get_state()
	adb = ADBWrapper( { "ip": this.config.adb.ip , "port": this.config.adb.port } )
	adb_status = adb.get_status()
	result = {
		"state": current_state ,
		"adb": adb_status ,
	}
	return result

async def status( request ):
	status = _status()
	return json_result( status )

async def state_check( request ):

	# prep
	this = utils.get_server_context()
	current_state = this.redis.get_state()
	adb = ADBWrapper( { "ip": this.config.adb.ip , "port": this.config.adb.port } )
	adb_status = adb.get_status()

	# keep track of last 10 states created from calling GET /state/check
	STATE_CHECK_LIST_KEY = f"{this.config.redis.prefix}.STATE_CHECK_LIST"
	this.redis.redis.rpush( STATE_CHECK_LIST_KEY , json.dumps( current_state ) )
	check_list_length = int( this.redis.redis.llen( STATE_CHECK_LIST_KEY ) )
	if check_list_length > 10:
		this.redis.redis.lpop( STATE_CHECK_LIST_KEY )

	# build list of the most recent states after the last app change
	previous_states = this.redis.redis.lrange( STATE_CHECK_LIST_KEY , 0 , -1 )
	previous_states = [ json.loads( x ) for x in previous_states ]
	previous_states.reverse()

	# why is the index for sessions backwards to get app name vs meta data ?????
	# TODO : just look at last window on the stack , grab the name , and then filter sessions based on the name ???
	current_adb_session = previous_states[ 0 ][ "adb_status" ][ "now_playing" ][ "sessions" ][ -1 ]
	current_adb_app_name = current_adb_session[ "app_name" ]
	print( current_adb_app_name )
	print( "0 == " ,  previous_states[ 0 ][ "adb_status" ][ "now_playing" ][ "sessions" ][ 0 ][ "meta_data" ][ "description" ] )
	print( "-1 == " , previous_states[ 0 ][ "adb_status" ][ "now_playing" ][ "sessions" ][ -1 ][ "meta_data" ][ "description" ] )
	print( "latest adb == " , adb_status[ "now_playing" ][ "sessions" ][ 0 ][ "meta_data" ][ "description" ] )
	previous_states_of_current_app = []
	still_current_app = True
	while still_current_app == True:
		if len( previous_states ) < 1:
			still_current_app = False
			break
		x = previous_states.pop( 0 )
		if x[ "adb_status" ][ "now_playing" ][ "sessions" ][ -1 ][ "app_name" ] != current_adb_app_name:
			still_current_app = False
			break
		previous_states_of_current_app.append( x )
	# pprint( previous_states_of_current_app )
	# print( len( previous_states_of_current_app ) )

	# heath check decision logic
	result = {}
	result[ "same_app" ] = False

	if current_state[ "adb_status" ][ "now_playing" ][ "now_playing_app" ] == adb_status[ "now_playing" ][ "now_playing_app" ]:
		result[ "same_app" ] = True



	# TODO = 12JUN2022 , tbc

	# custom health checks for different apps
	# pprint( previous_states_of_current_app )
	if current_adb_app_name == "com.spotify.tv.android":
		# latest = list[ 0 ]
		updated = [ x[ "adb_status" ][ "now_playing" ][ "sessions" ][ -1 ][ "state" ][ "updated" ] for x in previous_states_of_current_app ]
		position = [ x[ "adb_status" ][ "now_playing" ][ "sessions" ][ -1 ][ "state" ][ "updated" ] for x in previous_states_of_current_app ]
		track_titles = [ x[ "adb_status" ][ "now_playing" ][ "sessions" ][ -1 ][ "meta_data" ][ "description" ] for x in previous_states_of_current_app ]
		y = {
			"updated": updated ,
			"position": position ,
			"track_titles": track_titles ,
		}
		# pprint( y )
		# for index , state in enumerate( previous_states_of_current_app ):


	elif current_adb_app_name == "tv.twitch.android.viewer":
		pass


	# current_state_function_name = previous_states[ 0 ][ "name" ]
	# print( current_state_function_name )
	# for index , state in enumerate( previous_states ):


	# check_properties = {
	# 	"app_names": [ x[ "adb_status" ][ "now_playing" ][ "now_playing_app" ] for x in previous_states ] ,
	# 	"updated": [ x[ "adb_status" ][ "now_playing" ][ "sessions" ][ 1 ][ "state" ][ "updated" ] for x in previous_states ] ,
	# 	"position": [ x[ "adb_status" ][ "now_playing" ][ "sessions" ][ 1 ][ "state" ][ "position" ] for x in previous_states ] ,
	# 	"track_tit": [ x[ "adb_status" ][ "now_playing" ][ "sessions" ][ 1 ][ "state" ][ "position" ] for x in previous_states ] ,
	# }
	# for index , state in enumerate( previous_states ):
	# result[ "check_properties" ] = check_properties
	return json_result( result )



misc_blueprint.add_route( home , "/" , methods=[ "GET" ] , strict_slashes=False )
misc_blueprint.add_route( update_all , "/update" , methods=[ "GET" ] , strict_slashes=False )
misc_blueprint.add_route( update_all , "/update/all" , methods=[ "GET" ] , strict_slashes=False )
misc_blueprint.add_route( status , "/status" , methods=[ "GET" ] , strict_slashes=False )
misc_blueprint.add_route( state_check , "/state/check" , methods=[ "GET" ] , strict_slashes=False )
# misc_blueprint.add_route( update_all , "/update/twitch" , methods=[ "GET" ] , strict_slashes=False )