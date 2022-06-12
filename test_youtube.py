#!/usr/bin/env python3
import sys
from box import Box
import requests
from pprint import pprint
import yaml
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def read_yaml( file_path ):
	with open( file_path ) as f:
		return yaml.safe_load( f )

def batch_process( options ):
	batch_size = len( options[ "batch_list" ] )
	with ThreadPoolExecutor() as executor:
		result_pool = list( tqdm( executor.map( options[ "function_reference" ] , iter( options[ "batch_list" ] ) ) , total=batch_size ) )
		return result_pool

# https://developers.google.com/youtube/v3/docs/channels/list
def get_channels_id( channel_user_name , api_key ):
	headers = { 'accept': 'application/json, text/plain, */*', }
	params = {
		"part": "snippet" ,
		"forUsername": channel_user_name ,
		"key": api_key
	}
	url = f"https://www.googleapis.com/youtube/v3/channels"
	response = requests.get( url , headers=headers , params=params )
	response.raise_for_status()
	result = response.json()
	channel_id = result[ "items" ][ 0 ][ "id" ]
	return channel_id


# https://youtube.com/MontereyBayAquarium/%7Bchannel%20id%7D/live
# https://www.googleapis.com/youtube/v3/search?part=snippet&q=MontereyBayAquarium&eventType=live&type=video&key=${API_KEY}
# https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=MontereyBayAquarium&eventType=live&type=video&key=${API_KEY}


# https://console.cloud.google.com
# https://developers.google.com/youtube/v3/live/docs/liveStreams/list#examples
# https://developers.google.com/apis-explorer/#p%2Fyoutube%2Fv3%2F=
# https://developers.google.com/youtube/v3/docs/search/list
# https://developers.google.com/youtube/v3/docs/channels/list?apix=true
def one_hot_get_channel_live_streams( options ):
	headers = { 'accept': 'application/json, text/plain, */*', }
	params = {
		"part": "snippet" ,
		# "q": options[ 0 ] , # this would be if we wanted to 'search' 'MontereyBayAquarium' instead of using the channelId property
		"channelId": options[ 0 ] ,
		"eventType": "live" ,
		"type": "video" ,
		"key": options[ 1 ] ,
		"order": "viewCount" ,
		"maxResults": 50 # after 50 you have to start dealing with pageToken and pagnation stuff
	}
	url = f"https://www.googleapis.com/youtube/v3/search"
	response = requests.get( url , headers=headers , params=params )
	response.raise_for_status()
	result = response.json()
	pprint( result )

if __name__ == "__main__":
	config = Box( read_yaml( sys.argv[ 1 ] ) )

	channel_id = get_channels_id( "MontereyBayAquarium" , config.apps.youtube.personal.api_key )
	print( channel_id )
	one_hot_get_channel_live_streams( [ channel_id , config.apps.youtube.personal.api_key ] )

	# results = batch_process({
	# 	"max_workers": 5 ,
	# 	"batch_list": batch_option_list ,
	# 	"function_reference": one_hot_is_user_live
	# })