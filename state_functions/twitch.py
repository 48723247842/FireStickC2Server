import stackprinter
import time
from pprint import pprint

import redis_circular_list

from ADBWrapper import ADBWrapper
from PIL import Image
from pathlib import Path

import utils

def next():
	result = {}
	try:
		print( "next" )
	except Exception as e:
		print( e )
	return result

def previous():
	result = {}
	try:
		print( "previous" )
	except Exception as e:
		print( e )
	return result

def stop():
	result = {}
	try:
		print( "stop" )
	except Exception as e:
		print( e )
	return result

def play():
	result = {}
	try:
		print( "play" )
	except Exception as e:
		print( e )
	return result

def pause():
	result = {}
	try:
		print( "pause" )
	except Exception as e:
		print( e )
	return result

def resume():
	result = {}
	try:
		print( "resume" )
	except Exception as e:
		print( e )
	return result

def play_pause():
	result = {}
	try:
		print( "play_pause" )
	except Exception as e:
		print( e )
	return result

def uri():
	result = {}
	try:
		print( "uri" )
	except Exception as e:
		print( e )
	return result