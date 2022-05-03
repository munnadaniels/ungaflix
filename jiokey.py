import requests, json
import os, sys
import argparse

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
    res = requests.post(url = Request_URL + VideoID , data = '{"uniqueId":"' + uniqueID + '"}' , headers = headers)
    print(res.json())


          
    
load_config()
if ssotoken == "" and uniqueID == "":
    M_No = input ('Enter Mobile Number: ')
    login (M_No)
    load_config()
arguments = argparse.ArgumentParser()
arguments.add_argument("-id", "--id", dest="id", help="content id ")
arguments.add_argument("-q", "--quality", dest="res", help="quality of video")
args = arguments.parse_args()
VideoID = args.id
manifest = get_manifest(VideoID)
