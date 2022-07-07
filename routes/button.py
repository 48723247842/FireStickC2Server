import sys
from pprint import pprint

from sanic import Blueprint
from sanic.response import json as json_result
from sanic import response as sanic_response

import utils

# https://github.com/48723247842/WebsiteControllers/blob/6b70c72bbb4c02f3e659c39f1a75853fb0f683c4/python_app/api/disney/disney_utils.py

button_blueprint = Blueprint( "buttons_blueprint" , url_prefix="/" )

import state_functions.spotify as spotify
import state_functions.twitch as twitch

# async def home( request ):
# 	this = utils.get_server_context()
# 	return sanic_response.text( "you found the button main endpoint !!\n" )

# TODO : Decode which uri we want ? or leave as generic uri open ?
async def uri( request ):
	result = {}
	if "uri" not in request.args:
		return json_result( { "failed" : "no uri sent in request" } )
	if len( request.args ) != 1:
		return json_result( { "failed" : "no uri sent in request" } )
	uri = request.args[ "uri" ][ 0 ]
	this = utils.get_server_context()
	try:
		tv_setup_result = utils.setup_tv( this.tv )
		start_result = twitch.play_next_live_follower( this )
		result = {
			"route": "/uri" ,
			"state_function": "button.uri" ,
			"result": start_result ,
			"tv_result": tv_setup_result
		}
	except Exception as e:
		print( e )
	return json_result( result )

async def next( request ):
	result = {}
	this = utils.get_server_context()
	try:
		current_state = this.redis.get_state()
		if "name" not in current_state:
			return json_result( result )
		module_name = f"state_functions.{current_state[ 'name' ]}"
		if module_name not in sys.modules:
			return json_result( result )
		current_state = sys.modules[ module_name ].next( this )
		result = {
			"route": "/next" ,
			"result": "success" ,
			"current_state": current_state
		}
	except Exception as e:
		print( e )
	return json_result( result )

async def previous( request ):
	result = {}
	this = utils.get_server_context()
	try:
		current_state = this.redis.get_state()
		if "name" not in current_state:
			return json_result( result )
		module_name = f"state_functions.{current_state[ 'name' ]}"
		if module_name not in sys.modules:
			return json_result( result )
		current_state = sys.modules[ module_name ].previous( this )
		result = {
			"route": "/previous" ,
			"result": "success" ,
			"current_state": current_state
		}
	except Exception as e:
		print( e )
	return json_result( result )

async def stop( request ):
	result = {}
	this = utils.get_server_context()
	try:
		current_state = this.redis.get_state()
		if "name" not in current_state:
			return json_result( result )
		module_name = f"state_functions.{current_state[ 'name' ]}"
		if module_name not in sys.modules:
			return json_result( result )
		current_state = sys.modules[ module_name ].stop( this )
		result = {
			"route": "/stop" ,
			"result": "success" ,
			"current_state": current_state
		}
	except Exception as e:
		print( e )
	return json_result( result )

async def play( request ):
	result = {}
	this = utils.get_server_context()
	try:
		current_state = this.redis.get_state()
		if "name" not in current_state:
			return json_result( result )
		module_name = f"state_functions.{current_state[ 'name' ]}"
		if module_name not in sys.modules:
			return json_result( result )
		current_state = sys.modules[ module_name ].play( this )
		result = {
			"route": "/play" ,
			"result": "success" ,
			"current_state": current_state
		}
	except Exception as e:
		print( e )
	return json_result( result )

async def pause( request ):
	result = {}
	this = utils.get_server_context()
	try:
		current_state = this.redis.get_state()
		if "name" not in current_state:
			return json_result( result )
		module_name = f"state_functions.{current_state[ 'name' ]}"
		if module_name not in sys.modules:
			return json_result( result )
		current_state = sys.modules[ module_name ].pause( this )
		result = {
			"route": "/pause" ,
			"result": "success" ,
			"current_state": current_state
		}
	except Exception as e:
		print( e )
	return json_result( result )

async def resume( request ):
	result = {}
	this = utils.get_server_context()
	try:
		current_state = this.redis.get_state()
		if "name" not in current_state:
			return json_result( result )
		module_name = f"state_functions.{current_state[ 'name' ]}"
		if module_name not in sys.modules:
			return json_result( result )
		current_state = sys.modules[ module_name ].resume( this )
		result = {
			"route": "/resume" ,
			"result": "success" ,
			"current_state": current_state
		}
	except Exception as e:
		print( e )
	return json_result( result )

async def play_pause( request ):
	result = {}
	this = utils.get_server_context()
	try:
		current_state = this.redis.get_state()
		if "name" not in current_state:
			return json_result( result )
		module_name = f"state_functions.{current_state[ 'name' ]}"
		if module_name not in sys.modules:
			return json_result( result )
		current_state = sys.modules[ module_name ].play_pause( this )
		result = {
			"route": "/playpause" ,
			"result": "success" ,
			"current_state": current_state
		}
	except Exception as e:
		print( e )
	return json_result( result )

async def shuffle_on( request ):
	result = {}
	this = utils.get_server_context()
	try:
		current_state = this.redis.get_state()
		if "name" not in current_state:
			return json_result( result )
		module_name = f"state_functions.{current_state[ 'name' ]}"
		if module_name not in sys.modules:
			return json_result( result )
		current_state = sys.modules[ module_name ].shuffle_on( this )
		result = {
			"route": "/shuffle/on" ,
			"result": "success" ,
			"current_state": current_state
		}
	except Exception as e:
		print( e )
	return json_result( result )

async def shuffle_off( request ):
	result = {}
	this = utils.get_server_context()
	try:
		current_state = this.redis.get_state()
		if "name" not in current_state:
			return json_result( result )
		module_name = f"state_functions.{current_state[ 'name' ]}"
		if module_name not in sys.modules:
			return json_result( result )
		current_state = sys.modules[ module_name ].shuffle_off( this )
		result = {
			"route": "/shuffle/off" ,
			"result": "success" ,
			"current_state": current_state
		}
	except Exception as e:
		print( e )
	return json_result( result )

# button_blueprint.add_route( home , "/" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( uri , "/uri" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( next , "/next" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( previous , "/previous" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( stop , "/stop" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( play , "/play" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( pause , "/pause" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( resume , "/resume" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( play_pause , "/playpause" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( shuffle_on , "/shuffle" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( shuffle_on , "/shuffle/on" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( shuffle_off , "/shuffle/off" , methods=[ "GET" ] , strict_slashes=False )