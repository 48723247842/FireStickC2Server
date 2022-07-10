from pprint import pprint
import requests

from sanic import Blueprint
from sanic.response import json as json_result
from sanic import response as sanic_response

import utils
import state_functions.twitch as twitch

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

def one_hot_is_user_live( options ):
	try:
		endpoint = "https://api.twitch.tv/helix/streams"
		my_headers = {
			"Client-ID": options[ 1 ] ,
			"Authorization": f"Bearer {options[ 2 ]}"
		}
		my_params = { "user_login": options[ 0 ] }
		print( "waiting ...." )
		response = requests.get( endpoint , headers=my_headers , params=my_params )
		data = response.json()[ "data" ]
		if len( data ) == 0:
			return False
		result = data[ 0 ][ "type" ] == "live"
		if result == True:
			return options[ 0 ]
		return False
	except Exception as e:
		print( e )
		return False

# lrange "FSC2.APPS.TWITCH.FOLLOWING.CURRATED" 0 -1
# get "FSC2.APPS.TWITCH.FOLLOWING.CURRATED.INDEX"
async def update_live_users( request ):
	result = {}
	try:
		this = utils.get_server_context()
		live_currated_following_key = f"{this.config.redis.prefix}.APPS.TWITCH.FOLLOWING.CURRATED"
		batch_option_list = [ [ x , this.config.apps.twitch.personal.client_id , this.config.apps.twitch.personal.oauth_token ] for x in this.config.apps.twitch.following.currated ]
		live_currated_following = utils.batch_process({
			"max_workers": 10 ,
			"batch_list": batch_option_list ,
			"function_reference": one_hot_is_user_live
		})
		live_currated_following = [ x for x in live_currated_following if x ]
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
		print( e )
	return json_result( result )


twitch_blueprint.add_route( home , "/" , methods=[ "GET" ] , strict_slashes=False )
twitch_blueprint.add_route( update_live_users , "/update" , methods=[ "GET" ] , strict_slashes=False )