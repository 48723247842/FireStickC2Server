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
	return json_result({
		"route": "/button/next" ,
		"result": "success" ,
	})

button_blueprint.add_route( home , "/" , methods=[ "GET" ] , strict_slashes=False )
button_blueprint.add_route( next , "/next" , methods=[ "GET" ] , strict_slashes=False )