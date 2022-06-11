from pprint import pprint
import stackprinter

from ADBWrapper import ADBWrapper

from sanic import Blueprint
from sanic.response import json as json_result
from sanic import response as sanic_response

import utils

youtube_blueprint = Blueprint( "youtube_blueprint" , url_prefix="/youtube" )

async def home( request ):
	this = utils.get_server_context()
	return sanic_response.text( "you found the youtube main endpoint !!\n" )

async def next( request ):
	this = utils.get_server_context()
	previous_state = this.redis.get_state()
	return json_result({
		"route": "/youtube/next" ,
		"result": "success" ,
		"previous_state": previous_state
	})

async def previous( request ):
	this = utils.get_server_context()
	previous_state = this.redis.get_state()
	return json_result({
		"route": "/youtube/previous" ,
		"result": "success" ,
		"previous_state": previous_state
	})

async def stop( request ):
	this = utils.get_server_context()
	previous_state = this.redis.get_state()
	return json_result({
		"route": "/youtube/stop" ,
		"result": "success" ,
		"previous_state": previous_state
	})

async def play( request ):
	this = utils.get_server_context()
	previous_state = this.redis.get_state()
	response = { "route": "/youtube/play" , "previous_state": previous_state , "result": "failed" }
	if "url" in request.args:
		old_adb_status = False
		new_adb_status = False
		try:
			response[ "url" ] = request.args[ "url" ][ 0 ]
			adb = ADBWrapper( { "ip": this.config.adb.ip , "port": this.config.adb.port } )
			old_adb_status = adb.get_status()
			adb.open_uri( response[ "url" ] )
			new_adb_status = adb.get_status()
			response[ "result" ] = "success"
		except Exception as e:
			this.log( stackprinter.format() )
		if response[ "result" ] == "success":
			new_state = {
				"status": "youtube" ,
				"url": response[ "url" ] ,
				"time": utils.get_common_time_string( this.config.time_zone ) ,
				"adb_status": adb_status
			}
			this.redis.set_state( new_state )
			response[ "new_state" ] = new_state
	return json_result( response )

async def pause( request ):
	this = utils.get_server_context()
	previous_state = this.redis.get_state()
	return json_result({
		"route": "/youtube/pause" ,
		"result": "success" ,
		"previous_state": previous_state
	})

async def resume( request ):
	this = utils.get_server_context()
	previous_state = this.redis.get_state()
	return json_result({
		"route": "/youtube/resume" ,
		"result": "success" ,
		"previous_state": previous_state
	})

async def play_pause( request ):
	this = utils.get_server_context()
	previous_state = this.redis.get_state()
	return json_result({
		"route": "/youtube/playpause" ,
		"result": "success" ,
		"previous_state": previous_state
	})

youtube_blueprint.add_route( home , "/" , methods=[ "GET" ] , strict_slashes=False )
youtube_blueprint.add_route( next , "/next" , methods=[ "GET" ] , strict_slashes=False )
youtube_blueprint.add_route( previous , "/previous" , methods=[ "GET" ] , strict_slashes=False )
youtube_blueprint.add_route( stop , "/stop" , methods=[ "GET" ] , strict_slashes=False )
youtube_blueprint.add_route( play , "/play" , methods=[ "GET" ] , strict_slashes=False )
youtube_blueprint.add_route( pause , "/pause" , methods=[ "GET" ] , strict_slashes=False )
youtube_blueprint.add_route( resume , "/resume" , methods=[ "GET" ] , strict_slashes=False )
youtube_blueprint.add_route( play_pause , "/playpause" , methods=[ "GET" ] , strict_slashes=False )