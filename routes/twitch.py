from pprint import pprint

from sanic import Blueprint
from sanic.response import json as json_result
from sanic import response as sanic_response

import utils

twitch_blueprint = Blueprint( "twitch_blueprint" , url_prefix="/twitch" )

async def home( request ):
	this = utils.get_server_context()
	return sanic_response.text( "you found the twitch main endpoint !!\n" )

twitch_blueprint.add_route( home , "/" , methods=[ "GET" ] , strict_slashes=False )