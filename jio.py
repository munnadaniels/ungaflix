import os 
import subprocess
import shutil
import glob
import pathlib
import platform
import time
import argparse
 

arguments = argparse.ArgumentParser()
arguments.add_argument("-l", "--mpd", dest="mpd", help="mpd link")
arguments.add_argument("-o", "--output", dest="output", help="File Name")

args = arguments.parse_args()

m3u8 = str(args.mpd)
FILENAME = args.output

def get_streams(m3u8):
    print ("Downloading A/V")
    os.system(f'yt-dlp "{m3u8}" --allow-unplayable-formats --downloader aria2c --user-agent "JioOnDemand/1.5.2.1 (Linux;Android 4.4.2) Jio" -q --no-warnings -o "{FILENAME}"')

def rclone():
    print("Aagu Ra Nakka Pumka")
    output = f"{FILENAME}"
    subprocess.run(['rclone','copy', output,'Rose:'])
    print("SHAKTHI HERO THELUSA THAMMUDU NEEKU")

get_streams(m3u8)
rclone()
