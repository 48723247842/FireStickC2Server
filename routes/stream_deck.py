from pprint import pprint

from sanic import Blueprint
from sanic.response import json as json_result
from sanic import response as sanic_response

import stackprinter

import utils
import state_functions.spotify as spotify

# https://github.com/48723247842/WebsiteControllers/blob/6b70c72bbb4c02f3e659c39f1a75853fb0f683c4/python_app/api/disney/disney_utils.py

streamdeck_blueprint = Blueprint( "streamdeck_blueprint" , url_prefix="/streamdeck" )

async def home( request ):
	this = utils.get_server_context()
	return sanic_response.text( "you found the streamdeck main endpoint !!\n" )

def verify_token( request , comparing_token ):
	if "x" not in request.args:
		return False
	if len( request.args[ "x" ] ) != 1:
		return False
	if request.args[ "x" ][ 0 ] != comparing_token:
		return False
	return True

# Hardcoded as Spotify --> play_next_currated_playlist()
async def one( request ):
	result = {}
	this = utils.get_server_context()
	try:
		if verify_token( request , this.config.personal.streamdeck_route_token ) == False:
			return json_result( result )
		start_result = spotify.play_next_currated_playlist( this )
		result = {
			"route": "/streamdeck/1" ,
			"state_function": "spotify.play_next_currated_playlist()" ,
			"result": start_result ,
		}
	except Exception as e:
		print( stackprinter.format() )
		this.log( e )
	return json_result( result )

# Hardcoded as Twitch --> play_next_live_follower()
async def two( request ):
	result = {}
	this = utils.get_server_context()
	try:
		if verify_token( request , this.config.personal.streamdeck_route_token ) == False:
			return json_result( result )
		previous_state = this.redis.get_state()
		result = {
			"route": "/streamdeck/2" ,
			"result": "success" ,
			"previous_state": previous_state
		}
	except Exception as e:
		this.log( e )
	return json_result( result )

# Hardcoded as YouTube --> play_next_live_follower()
async def three( request ):
	result = {}
	this = utils.get_server_context()
	try:
		if verify_token( request , this.config.personal.streamdeck_route_token ) == False:
			return json_result( result )
		previous_state = this.redis.get_state()
		result = {
			"route": "/streamdeck/3" ,
			"result": "success" ,
			"previous_state": previous_state
		}
	except Exception as e:
		this.log( e )
	return json_result( result )

async def four( request ):
	result = {}
	this = utils.get_server_context()
	try:
		if verify_token( request , this.config.personal.streamdeck_route_token ) == False:
			return json_result( result )
		previous_state = this.redis.get_state()
		result = {
			"route": "/streamdeck/4" ,
			"result": "success" ,
			"previous_state": previous_state
		}
	except Exception as e:
		this.log( e )
	return json_result( result )

async def five( request ):
	result = {}
	this = utils.get_server_context()
	try:
		if verify_token( request , this.config.personal.streamdeck_route_token ) == False:
			return json_result( result )
		previous_state = this.redis.get_state()
		result = {
			"route": "/streamdeck/5" ,
			"result": "success" ,
			"previous_state": previous_state
		}
	except Exception as e:
		this.log( e )
	return json_result( result )

async def six( request ):
	result = {}
	this = utils.get_server_context()
	try:
		if verify_token( request , this.config.personal.streamdeck_route_token ) == False:
			return json_result( result )
		previous_state = this.redis.get_state()
		result = {
			"route": "/streamdeck/6" ,
			"result": "success" ,
			"previous_state": previous_state
		}
	except Exception as e:
		this.log( e )
	return json_result( result )


streamdeck_blueprint.add_route( home , "/" , methods=[ "GET" ] , strict_slashes=False )
streamdeck_blueprint.add_route( one , "/1" , methods=[ "GET" ] , strict_slashes=False )
streamdeck_blueprint.add_route( two , "/2" , methods=[ "GET" ] , strict_slashes=False )
streamdeck_blueprint.add_route( three , "/3" , methods=[ "GET" ] , strict_slashes=False )
streamdeck_blueprint.add_route( four , "/4" , methods=[ "GET" ] , strict_slashes=False )
streamdeck_blueprint.add_route( five , "/5" , methods=[ "GET" ] , strict_slashes=False )
streamdeck_blueprint.add_route( six , "/6" , methods=[ "GET" ] , strict_slashes=False )