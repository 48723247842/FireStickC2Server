from pprint import pprint

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

misc_blueprint.add_route( home , "/" , methods=[ "GET" ] , strict_slashes=False )
misc_blueprint.add_route( update_all , "/update" , methods=[ "GET" ] , strict_slashes=False )
misc_blueprint.add_route( update_all , "/update/all" , methods=[ "GET" ] , strict_slashes=False )
misc_blueprint.add_route( status , "/status" , methods=[ "GET" ] , strict_slashes=False )
# misc_blueprint.add_route( update_all , "/update/twitch" , methods=[ "GET" ] , strict_slashes=False )