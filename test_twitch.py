#!/usr/bin/env python3
import sys
from box import Box
import requests
import yaml

def read_yaml( file_path ):
	with open( file_path ) as f:
		return yaml.safe_load( f )

# https://dev.twitch.tv/docs/authentication/register-app
# https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/#client-credentials-grant-flow

# POST Request
# https://id.twitch.tv/oauth2/token?client_id=${}&client_secret=${}&grant_type=client_credentials

# GET Request
# https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=${}&redirect_uri=http://localhost:${}&scope=analytics%3aread%3aextensions%20analytics%3aread%3agames%20bits%3aread%20channel%3aedit%3acommercial%20channel%3amanage%3abroadcast%20channel%3amanage%3aextensions%20channel%3amanage%3aredemptions%20channel%3amanage%3avideos%20channel%3aread%3aeditors%20channel%3aread%3ahype_train%20channel%3aread%3aredemptions%20channel%3aread%3astream_key%20channel%3aread%3asubscriptions%20clips%3aedit%20moderation%3aread%20user%3aedit%20user%3aedit%3afollows%20user_follows_edit%20user%3aread%3ablocked_users%20user%3amanage%3ablocked_users%20user%3aread%3abroadcast%20user%3aread%3aemail

# https://api.twitch.tv/helix/streams?user_login=pawelqhd
def is_user_live( username , client_id , oauth_token ):
	endpoint = 'https://api.twitch.tv/helix/streams'
	my_headers = {
		'Client-ID': client_id,
		'Authorization': f'Bearer {oauth_token}'
	}
	my_params = {'user_login': username}
	response = requests.get(endpoint, headers=my_headers, params=my_params)
	data = response.json()['data']
	if len(data) == 0:
		return False
	return data[0]['type'] == 'live'

if __name__ == "__main__":
	config = Box( read_yaml( sys.argv[ 1 ] ) )
	is_live = is_user_live(
		sys.argv[ 2 ] ,
		config.apps.twitch.personal.client_id ,
		config.apps.twitch.personal.oauth_token ,
	)
	print( is_live )