#!/usr/bin/env python3
import sys
import stackprinter
from ADBWrapper import ADBWrapper
from box import Box
from LGTVController import LGTVController
import utils
from pprint import pprint

if __name__ == "__main__":
	config_file_path = "./config.yaml"
	config = Box( utils.read_yaml( config_file_path ) )

	tv_controller = LGTVController( config.tv )
	tv_input = tv_controller.get_input()
	print( "TV Status === " )
	pprint( tv_input )

	adb = ADBWrapper( { "ip": config.adb.ip , "port": config.adb.port } )
	adb_status = adb.get_status()
	print( "ADB Status === " )
	pprint( adb_status )
