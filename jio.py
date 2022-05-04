import requests, json
import os, sys
import argparse
import subprocess
import pathlib
import shutil

FILE_DIRECTORY=str(pathlib.Path(__file__).parent.absolute())
TEMPORARY_PATH = FILE_DIRECTORY+"/cache"
OUTPUT_PATH = FILE_DIRECTORY+"/output"
ENCODES = FILE_DIRECTORY+"/encodes"


# define paths
currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)
ytdl_path = "yt-dlp"
filedir=str(pathlib.Path(__file__).parent.absolute())
outputpath = filedir+"/output"

# define 
def load_config():
    global ssotoken, uniqueID
    with open ("creds.txt", "r") as f:
        try:
            Creds = json.load(f)
            ssotoken = Creds['ssotoken']
            uniqueID = Creds['uniqueID']
        except json.JSONDecodeError:
            ssotoken = ''
            uniqueID = ''    

Request_URL = "https://prod.media.jio.com/apis/common/v3/playbackrights/get/"
Meta_URL = "https://prod.media.jio.com/apis/common/v3/metamore/get/"
#cachePath = 
#outPath = 
OTPSendURL = "https://prod.media.jio.com/apis/common/v3/login/sendotp"
OTPVerifyURL = "https://prod.media.jio.com/apis/common/v3/login/verifyotp"

def login(mobile_number):
    send = requests.post(url = OTPSendURL, headers = {
    'authority': 'prod.media.jio.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'origin': 'https://www.jiocinema.com',
    'referer': 'https://www.jiocinema.com/',
    },
     data = '{"number":"+91' + mobile_number +'"}'
    )
    if 'success' in str(send.content):
        OTP = input ('Enter OTP Received: ')
        verify = requests.post(url = OTPVerifyURL, headers = {
        'authority': 'prod.media.jio.com',
        'pragma': 'no-cache',
        'origin': 'https://www.jiocinema.com',
        'referer': 'https://www.jiocinema.com/',
        'deviceid': '1727391720'
        },
        data = '{"number":"+91' + mobile_number + '","otp":"' + OTP + '"}')
        creds = json.loads(verify.content)
        print (creds)
        load_creds(creds)
    else:
        print ("Wrong/Unregistered Mobile Number (ensure there's no +91 or 0 in the beginning)")
        sys.exit()

def load_creds(creds):
    try:
        ssotoken = creds['ssoToken']
        uniqueID = creds['uniqueId']
    except KeyError:
        print ("Wrong OTP, Try again!")
        sys.exit()
    Creds = {
        "ssotoken" : ssotoken,
        "uniqueID" : uniqueID
    }
    with open("creds.txt", "w") as f:
        f.write(json.dumps(Creds))

def get_manifest(VideoID):
    headers = {
    'authority': 'prod.media.jio.com',
    'pragma': 'no-cache',
    'ssotoken': ssotoken,
    'bitrates': 'true',
    'os': 'Android',
    'user-agent': 'JioOnDemand/1.5.2.1 (Linux;Android 4.4.2) Jio',
    'content-type': 'application/json',
    'accept': 'application/json, text/plain, */*',
    'devicetype': 'tv',
    }
    response = requests.post(url = Request_URL + VideoID , data = '{"uniqueId":"' + uniqueID + '"}' , headers = headers)
    return json.loads(response.text)

def get_m3u8(manifest):
    m3u8 = manifest['m3u8']['high']
    return m3u8

def divider():
	print ('-' * shutil.get_terminal_size().columns)

def mod_m3u8(url):
    mod = url.replace("jiovod.cdn.jio.com", "jiobeats.cdn.jio.com")
    lst = mod.split("/")
    if args.res == 'low':
         lst[-1] = "playlist_HD_TV_L.m3u8"
    elif args.res == 'med':
         lst[-1] = "playlist_HD_TV_M.m3u8"
    elif args.res == 'high':
         lst[-1] = "playlist_HD_TV_H.m3u8"
    else:
         lst[-1] = "chunklist.m3u8"
    mod = "/".join(lst)
    return mod

def get_metadata(VideoID):
    response = requests.get (url= Meta_URL + VideoID)
    return json.loads(response.text)

print ('JioCinema Content Downloading Tool')
load_config()
if ssotoken == "" and uniqueID == "":
    M_No = input ('Enter Mobile Number: ')
    login (M_No)
    load_config()
arguments = argparse.ArgumentParser()
arguments.add_argument("-id", "--id", dest="id", help="content id ")
arguments.add_argument("-q", "--quality", dest="res", help="quality") 
args = arguments.parse_args()
VideoID = args.id
TroopOriginals = args.res
manifest = get_manifest(VideoID)
metadata = get_metadata(VideoID)
try:
    content_name = metadata['name']
except KeyError:
    print ("Incorrect/Malformed VideoID")
    sys.exit()
print (f'Downloading: {content_name} | {metadata["year"]} | {metadata["language"]}')
# print (f'Subtitles available: {metadata["subtitle"]}')    
fileName = f'{content_name}.{metadata["year"]}.{TroopOriginals}.mp4'

def get_streams(m3u8):
    print(f'link: {m3u8}') 
    print ("Downloading A/V")
    os.system(f'{ytdl_path} {m3u8} --allow-unplayable-formats --external-downloader aria2c --user-agent "JioOnDemand/1.5.2.1 (Linux;Android 4.4.2) Jio" -q --no-warnings') # + -P TEMP:{cachePath} -P HOME:{outputpath/fileName}
    if args.res == 'low':
         os.rename(f'playlist_HD_TV_L [playlist_HD_TV_L].mp4', fileName)
    elif args.res == 'med':
         os.rename(f'playlist_HD_TV_M [playlist_HD_TV_M].mp4', fileName)
    elif args.res == 'high':
         os.rename(f'playlist_HD_TV_H [playlist_HD_TV_H].mp4', fileName)
    else:
         os.rename(f'chunklist [chunklist].mp4', OUTPUT_PATH/fileName)
    print ("\nSuccessfully downloaded the stream!") 

def trackname():
        divider()
        os.system('ffmpeg -i %s/%s -hide_banner -map 0:v -map 0:a -map 0:s? -metadata title="TroopOriginals" -metadata:s:v title="TroopOriginals" -metadata:s:a title="TroopOriginals" -metadata:s:s title="TroopOriginals" -codec copy %s/thelidhu.mkv && mv %s/thelidhu.mkv %s/%s'%(OUTPUT_PATH,fileName,OUTPUT_PATH,OUTPUT_PATH,ENCODES,fileName))


def rclone():
    print("Aagu Ra Nakka Pumka")
    output =  ENCODES + '/' + f"{fileName}"
    subprocess.run(['rclone','move', output,'Rose:'])
    print("SHAKTHI HERO THELUSA THAMMUDU NEEKU") 

'''def get_streams(m3u8):
def download_drm_content(mpd_url):
	divider()
	print("Processing Video Info..")
	os.system('yt-dlp --external-downloader aria2c --no-warnings --allow-unplayable-formats --no-check-certificate -F "%s"'%m3u8)
	divider()
	VIDEO_ID = input("ENTER VIDEO_ID (Press Enter for Best): ")
	if VIDEO_ID == "":
		VIDEO_ID = "bv"
	divider()
	print("Downloading Encrypted Video from CDN..")	
	os.system(f'yt-dlp -o "{fileName}.%(ext)s" --no-warnings --external-downloader aria2c --allow-unplayable-formats --no-check-certificate -f {VIDEO_ID} "{m3u8}" -o "{fileName}.%(ext)s"')'''
	
divider()
m3u8_url = get_m3u8(manifest)
nonDRM_m3u8_url = mod_m3u8(m3u8_url)
get_streams(nonDRM_m3u8_url)
trackname()
rclone()

