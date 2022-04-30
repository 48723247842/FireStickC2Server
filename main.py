#!/usr/bin/env python3
import sys
from C2Server import C2Server

if __name__ == "__main__":
	server = C2Server({
		"config_file_path": sys.argv[ 1 ]
	})
	server.start()