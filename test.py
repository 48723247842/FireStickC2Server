from pylgtv import WebOsClient
import sys
import logging
import stackprinter
import json
import random
from pprint import pprint

import pdb

from wakeonlan import send_magic_packet
import socket
import websocket # pip install websocket-client

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def write_json( file_path , python_object ):
	with open( file_path , 'w', encoding='utf-8' ) as f:
		json.dump( python_object , f , ensure_ascii=False , indent=4 )

def read_json( file_path ):
	with open( file_path ) as f:
		return json.load( f )

def pair():
	pass

def get_apps():

	client_id = "18370ed9f27f11668f899ca71e479bc6"
	IP = "192.168.1.6"
	PORT = 3000
	message_id = f"getapps_3"
	message_type = "request"
	uri = "com.webos.applicationManager/listLaunchPoints"
	payload = {}
	websocket_url = f"ws://{IP}:{PORT}/"

	handshake_data = read_json( "./handshake_test.json" )
	# handshake_data = { IP: client_id }
	# handshake_data = { "192.168.1.6": "18370ed9f27f11668f899ca71e479bc6" }

	# https://github.com/websocket-client/websocket-client/blob/a8a409999280e8b90d856113cd109a46b1d465b7/websocket/_core.py#L221
	ws = websocket.create_connection( websocket_url , sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),) , suppress_origin=True )
	# ws = websocket.create_connection( websocket_url )
	ws.timeout = 10
	print( f"Connected === {ws.connected}" )
	ws.send( json.dumps( handshake_data ) )
	print( f"Connected === {ws.connected}" )
	print( ws.recv() )
	# https://github.com/websocket-client/websocket-client/blob/a8a409999280e8b90d856113cd109a46b1d465b7/websocket/_core.py#L365
	# opcode, data = ws.recv_data()
	# print( opcode , data )


	message = {
		'id':  message_id ,
		'type': message_type ,
		'uri': f"ssap://{uri}" ,
		'payload': payload ,
	}
	ws.send( json.dumps( message ) )
	print( f"Connected === {ws.connected}" )
	response = ws.recv()
	# response = ws.recv()
	pprint( response )
	ws.close()

def set_input():
	client_id = "18370ed9f27f11668f899ca71e479bc6"
	IP = "192.168.1.6"
	PORT = 3000
	message_id = f"getapps_3"
	message_type = "request"
	uri = "tv/switchInput"
	payload = {}
	websocket_url = f"ws://{IP}:{PORT}/"

	handshake_data = read_json( "./handshake_test.json" )
	ws = websocket.create_connection( websocket_url , sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),) , suppress_origin=True )
	ws.timeout = 10
	print( f"Connected === {ws.connected}" )
	ws.send( json.dumps( handshake_data ) )
	print( f"Connected === {ws.connected}" )
	print( ws.recv() )

	message = {
		'id':  message_id ,
		'type': message_type ,
		'uri': f"ssap://{uri}" ,
		'payload': {
			"inputId": "HDMI_1"
		} ,
	}
	ws.send( json.dumps( message ) )
	print( f"Connected === {ws.connected}" )
	response = ws.recv()
	# response = ws.recv()
	pprint( response )
	ws.close()

def original():
	# pdb.set_trace()
	webos_client = WebOsClient( "192.168.1.6" )
	apps = list( webos_client.get_apps() )
	print( apps )

try:
	# original()
	get_apps()
	# set_input()
except Exception as e:
	# print( stackprinter.format() )
	print( e )