#!/usr/bin/env python3
import sys
import stackprinter
from ADBWrapper import ADBWrapper
from box import Box
from LGTVController import LGTVController
import utils

if __name__ == "__main__":
	# config_file_path = sys.argv[ 1 ] if len( sys.argv ) > 1 else "./config.yaml"
	config_file_path = "./config.yaml"
	config = Box( utils.read_yaml( config_file_path ) )

	tv_controller = LGTVController( config.tv )
	tv_controller.set_input( "HDMI_1" )
	tv_controller.set_volume( 11 )

	adb = ADBWrapper( { "ip": config.adb.ip , "port": config.adb.port } )
	uri = f"vlc://{sys.argv[ 1 ]}"
	print( f"ADB :: Launching :: {uri}" )
	adb.open_uri( uri )
	new_adb_status = adb.get_status()
