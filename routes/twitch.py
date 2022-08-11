from pprint import pprint
import requests
import stackprinter

from sanic import Blueprint
from sanic.response import json as json_result
from sanic import response as sanic_response

import utils
import state_functions.twitch as twitch

import json
def write_json( file_path , python_object ):
	with open( file_path , 'w', encoding='utf-8' ) as f:
		json.dump( python_object , f , ensure_ascii=False , indent=4 )

twitch_blueprint = Blueprint( "twitch_blueprint" , url_prefix="/twitch" )

async def home( request ):
	result = {}
	this = utils.get_server_context()
	try:
		tv_setup_result = utils.setup_tv( this.tv )
		start_result = twitch.play_next_live_follower( this )
		result = {
			"route": "/twitch" ,
			"state_function": "twitch.play_next_live_follower" ,
			"result": start_result ,
			"tv_result": tv_setup_result
		}
	except Exception as e:
		this.log( e )
	return json_result( result )

# def one_hot_is_user_live( options ):
# 	try:
# 		endpoint = "https://api.twitch.tv/helix/streams"
# 		my_headers = {
# 			"Client-ID": options[ 1 ] ,
# 			"Authorization": f"Bearer {options[ 2 ]}"
# 		}
# 		my_params = { "user_login": options[ 0 ] }
# 		# print( "waiting ...." )
# 		response = requests.get( endpoint , headers=my_headers , params=my_params )
# 		response.raise_for_status()
# 		response_json = response.json()
# 		if "data" not in response_json:
# 			print( "No 'data' key in response.json()" )
# 			return False
# 		data = response_json[ "data" ]
# 		if len( data ) == 0:
# 			print( "Length of data < 0" )
# 			return False
# 		if "type" not in data[ 0 ]:
# 			print( "No 'type' key in data object" )
# 			return False
# 		is_live = False
# 		if data[ 0 ][ "type" ] == "live":
# 			is_live = True
# 		if is_live == True:
# 			# return username
# 			return options[ 0 ]
# 		return False
# 	except Exception as e:
# 		print( e )
# 		return False

# https://dev.twitch.tv/docs/api/reference#get-streams
def get_live_users( client_id , oauth_code , user_list ):
	try:
		live_users = []

		endpoint = "https://api.twitch.tv/helix/streams"
		my_headers = {
			"Client-ID":client_id ,
			"Authorization": f"Bearer {oauth_code}"
		}
		print( user_list )
		endpoint_suffix = ""
		for index , user_name in enumerate( user_list[ 0 : -2 ] ):
			endpoint_suffix += f"user_login={user_name}&"
		endpoint_suffix += f"user_login={user_list[ -1 ]}"
		endpoint += f"?{endpoint_suffix}"
		print( endpoint )
		response = requests.get( endpoint , headers=my_headers )
		response.raise_for_status()
		response_json = response.json()
		# write_json( "test.json" , response_json )
		if "data" not in response_json:
			print( "No 'data' key in response.json()" )
			return live_users
		data = response_json[ "data" ]
		if len( data ) == 0:
			print( "Length of data < 0" )
			return live_users
		for index , live_user in enumerate( data ):
			if "user_login" in live_user:
				live_users.append( live_user[ "user_login" ] )
		return live_users
	except Exception as e:
		print( stackprinter.format() )
		return []

async def update_live_users( request ):
	result = {}
	try:
		this = utils.get_server_context()
		live_currated_following_key = f"{this.config.redis.prefix}.APPS.TWITCH.FOLLOWING.CURRATED"
		live_currated_following = get_live_users( this.config.apps.twitch.personal.client_id , this.config.apps.twitch.personal.oauth_token , this.config.apps.twitch.following.currated )
		order = { v: i for i , v in enumerate( this.config.apps.twitch.following.currated ) }
		currated_results = sorted( live_currated_following , key=lambda x: order[ x ] )

		this.redis.redis.delete( live_currated_following_key )

		pipeline = this.redis.redis.pipeline()
		for i , x in enumerate( currated_results ):
			# c2.redis.redis.rpush( live_currated_following_key , x )
			pipeline.rpush( live_currated_following_key , x )
		pipeline.execute()
		result = currated_results
	except Exception as e:
		print( stackprinter.format() )
	return json_result( result )

# lrange "FSC2.APPS.TWITCH.FOLLOWING.CURRATED" 0 -1
# get "FSC2.APPS.TWITCH.FOLLOWING.CURRATED.INDEX"
# async def update_live_users( request ):
# 	result = {}
# 	try:
# 		this = utils.get_server_context()
# 		live_currated_following_key = f"{this.config.redis.prefix}.APPS.TWITCH.FOLLOWING.CURRATED"
# 		batch_option_list = [ [ x , this.config.apps.twitch.personal.client_id , this.config.apps.twitch.personal.oauth_token ] for x in this.config.apps.twitch.following.currated ]
# 		live_currated_following = utils.batch_process({
# 			"max_workers": 10 ,
# 			"batch_list": batch_option_list ,
# 			"function_reference": one_hot_is_user_live
# 		})
# 		live_currated_following = [ x for x in live_currated_following if x ]
# 		order = { v: i for i , v in enumerate( this.config.apps.twitch.following.currated ) }
# 		currated_results = sorted( live_currated_following , key=lambda x: order[ x ] )

# 		this.redis.redis.delete( live_currated_following_key )

# 		pipeline = this.redis.redis.pipeline()
# 		for i , x in enumerate( currated_results ):
# 			# c2.redis.redis.rpush( live_currated_following_key , x )
# 			pipeline.rpush( live_currated_following_key , x )
# 		pipeline.execute()
# 		result = currated_results
# 	except Exception as e:
# 		print( e )
# 	return json_result( result )


twitch_blueprint.add_route( home , "/" , methods=[ "GET" ] , strict_slashes=False )
twitch_blueprint.add_route( update_live_users , "/update" , methods=[ "GET" ] , strict_slashes=False )