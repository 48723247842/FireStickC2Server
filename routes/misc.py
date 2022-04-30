from pprint import pprint

from sanic import Blueprint
from sanic.response import json as json_result
from sanic import response as sanic_response

import utils

misc_blueprint = Blueprint( "misc_blueprint" , url_prefix="/" )

@misc_blueprint.route( "/" )
def home( request ):
	this = utils.get_server_context()
	print( this.config )
	return sanic_response.text( "you found the Fire Stick C2 Server !!\n" )