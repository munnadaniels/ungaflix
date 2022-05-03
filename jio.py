#!/usr/bin/env python3

import os 
import subprocess
import shutil
import glob
import pathlib
import platform
import time
import argparse


FILE_DIRECTORY=str(pathlib.Path(__file__).parent.absolute())
TEMPORARY_PATH = FILE_DIRECTORY+"/cache"
OUTPUT_PATH = FILE_DIRECTORY+"/output"


arguments = argparse.ArgumentParser()
arguments.add_argument("-l", "--mpd", dest="mpd", help="mpd link")
arguments.add_argument("-o", "--output", dest="output", help="File Name")

args = arguments.parse_args()

def divider():
	print ('-' * shutil.get_terminal_size().columns)

def download_drm_content(mpd_url):
	divider()
        FILENAME= str(args.output)
        LINK= str(args.mpd)
	print("Processing Video Info..")
	os.system('yt-dlp %s --allow-unplayable-formats --downloader aria2c --user-agent "JioOnDemand/1.5.2.1 (Linux;Android 4.4.2) Jio" -o %s'%(LINK,FILENAME)

divider()
print("**** Aagu Ra Nakka Pumka ****")
divider()
download_drm_content(MPD_URL)
