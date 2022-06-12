#!/usr/bin/env python3
import sys
from box import Box
import requests
from pprint import pprint
import yaml

def read_yaml( file_path ):
	with open( file_path ) as f:
		return yaml.safe_load( f )

# https://dev.twitch.tv/docs/authentication/register-app
# https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/#client-credentials-grant-flow

# POST Request
# https://id.twitch.tv/oauth2/token?client_id=${}&client_secret=${}&grant_type=client_credentials

# GET Request
# urlEncode "analytics:read:extensions analytics:read:games bits:read channel:edit:commercial channel:manage:broadcast channel:manage:extensions channel:manage:redemptions channel:manage:videos channel:read:editors channel:read:hype_train channel:read:redemptions channel:read:stream_key channel:read:subscriptions clips:edit moderation:read user:edit user:read:follows user:edit:follows user_follows_edit user:read:blocked_users user:manage:blocked_users user:read:broadcast user:read:email"
# https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=${}&redirect_uri=http://localhost:${}&scope=analytics%3aread%3aextensions%20analytics%3aread%3agames%20bits%3aread%20channel%3aedit%3acommercial%20channel%3amanage%3abroadcast%20channel%3amanage%3aextensions%20channel%3amanage%3aredemptions%20channel%3amanage%3avideos%20channel%3aread%3aeditors%20channel%3aread%3ahype_train%20channel%3aread%3aredemptions%20channel%3aread%3astream_key%20channel%3aread%3asubscriptions%20clips%3aedit%20moderation%3aread%20user%3aedit%20user%3aread%3afollows%20user%3aedit%3afollows%20user_follows_edit%20user%3aread%3ablocked_users%20user%3amanage%3ablocked_users%20user%3aread%3abroadcast%20user%3aread%3aemail

def get_user_info( username , client_id , oauth_token ):
	endpoint = 'https://api.twitch.tv/helix/users'
	my_headers = {
		'Client-ID': client_id,
		'Authorization': f'Bearer {oauth_token}'
	}
	my_params = {'login': username}
	response = requests.get( endpoint , headers=my_headers , params=my_params )
	data = response.json()['data']
	if len(data) == 0:
		return False
	return data[0]

def get_channel_info( user_id , client_id , oauth_token ):
	endpoint = 'https://api.twitch.tv/helix/channels'
	my_headers = {
		'Client-ID': client_id,
		'Authorization': f'Bearer {oauth_token}'
	}
	my_params = {'broadcaster_id': user_id}
	response = requests.get( endpoint , headers=my_headers , params=my_params )
	data = response.json()['data']
	if len(data) == 0:
		return False
	return data[0]

# https://dev.twitch.tv/docs/api/reference#get-followed-streams
def get_followed_streams( user_id , client_id , oauth_token ):
	endpoint = 'https://api.twitch.tv/helix/streams/followed'
	my_headers = {
		'Client-ID': client_id,
		'Authorization': f'Bearer {oauth_token}'
	}
	my_params = {'user_id': user_id}
	response = requests.get( endpoint , headers=my_headers , params=my_params )
	response.raise_for_status()
	data = response.json()
	return data

# https://api.twitch.tv/helix/streams?user_login=pawelqhd
def is_user_live( username , client_id , oauth_token ):
	endpoint = 'https://api.twitch.tv/helix/streams'
	my_headers = {
		'Client-ID': client_id,
		'Authorization': f'Bearer {oauth_token}'
	}
	my_params = {'user_login': username}
	response = requests.get( endpoint , headers=my_headers , params=my_params )
	data = response.json()['data']
	if len(data) == 0:
		return False
	return data[0]['type'] == 'live'

if __name__ == "__main__":
	config = Box( read_yaml( sys.argv[ 1 ] ) )
	user_info = get_user_info(
		sys.argv[ 2 ] ,
		config.apps.twitch.personal.client_id ,
		config.apps.twitch.personal.oauth_token ,
	)
	pprint( user_info )
	following = get_followed_streams(
		user_info[ "id" ] ,
		config.apps.twitch.personal.client_id ,
		config.apps.twitch.personal.oauth_token ,
	)
	pprint( following )


	# is_live = is_user_live(
	# 	sys.argv[ 2 ] ,
	# 	config.apps.twitch.personal.client_id ,
	# 	config.apps.twitch.personal.oauth_token ,
	# )
	# print( "Is Live ? == " , is_live )

	# channel_info = get_channel_info(
	# 	user_info[ "id" ] ,
	# 	config.apps.twitch.personal.client_id ,
	# 	config.apps.twitch.personal.oauth_token ,
	# )
	# pprint( channel_info )