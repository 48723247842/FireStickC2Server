#!/usr/bin/env python3
import sys
import os
import requests

sys.path.append( os.getcwd() + "/.." )
import utils
from box import Box

def get_json( url , params={} ):
	headers = { 'accept': 'application/json, text/plain, */*' }
	response = requests.get( url , headers=headers , params=params )
	response.raise_for_status()
	print( response.json() )

if __name__ == "__main__":
	# config = utils.read_yaml( sys.argv[ 1 ] )
	config = Box( utils.read_yaml( "../config.yaml" ) )

	# get_json( f"http://{config.sanic.host}:{config.sanic.port}/youtube/next" )
	# get_json( f"http://{config.sanic.host}:{config.sanic.port}/youtube/previous" )
	# get_json( f"http://{config.sanic.host}:{config.sanic.port}/youtube/stop" )
	get_json( f"http://{config.sanic.host}:{config.sanic.port}/youtube/play" , {
		"url": "https://www.youtube.com/watch?v=naOsvWxeYgo&list=PLcW8xNfZoh7fCLYJi0m3JXLs0LdcAsc0R&index=1"
	})
	# get_json( f"http://{config.sanic.host}:{config.sanic.port}/youtube/pause" )
	# get_json( f"http://{config.sanic.host}:{config.sanic.port}/youtube/resume" )
	# get_json( f"http://{config.sanic.host}:{config.sanic.port}/youtube/play_pause" )