from pprint import pprint

from sanic import Blueprint
from sanic.response import json as json_result
from sanic import response as sanic_response

import utils

# https://github.com/48723247842/WebsiteControllers/blob/6b70c72bbb4c02f3e659c39f1a75853fb0f683c4/python_app/api/disney/disney_utils.py

button_blueprint = Blueprint( "buttons_blueprint" , url_prefix="/button" )

async def home( request ):
	this = utils.get_server_context()
	return sanic_response.text( "you found the button main endpoint !!\n" )

async def next( request ):
	this = utils.get_server_context()
	previous_state = this.redis.get_state()
	return json_result({
		"route": "/button/next" ,
		"result": "success" ,
		"previous_state": previous_state
	})

async def previous( request ):
	this = utils.get_server_context()
	previous_state = this.redis.get_state()
	return json_result({
		"route": "/button/previous" ,
		"result": "success" ,
		"previous_state": previous_state
	})

async def stop( request ):
	this = utils.get_server_context()
	previous_state = this.redis.get_state()
	return json_result({
		"route": "/button/stop" ,
		"result": "success" ,
		"previous_state": previous_state
	})

async def play( request ):
	this = utils.get_server_context()
	previous_state = this.redis.get_state()
	return json_result({
		"route": "/button/play" ,
		"result": "success" ,
		"previous_state": previous_state
	})

async def pause( request ):
	this = utils.get_server_context()
	previous_state = this.redis.get_state()
	return json_result({
		"route": "/button/pause" ,
		"result": "success" ,
		"previous_state": previous_state
	})

async def resume( request ):
	this = utils.get_server_context()
	previous_state = this.redis.get_state()
	return json_result({
		"route": "/button/resume" ,
		"result": "success" ,
		"previous_state": previous_state
	})

async def play_pause( request ):
	this = utils.get_server_context()
	previous_state = this.redis.get_state()
	return json_result({
		"route": "/button/playpause" ,
		"result": "success" ,
		"previous_state": previous_state
	})

button_blueprint.add_route( home , "/" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( next , "/next" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( previous , "/previous" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( stop , "/stop" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( play , "/play" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( pause , "/pause" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( resume , "/resume" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( play_pause , "/playpause" , methods=[ "GET" ] , strict_slashes=False )