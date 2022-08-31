
import subprocess
import os
from os import path
# import time
from threading import Thread
# import gdown
# import wget
import json

import cloudinary
import cloudinary.uploader
import cloudinary.api


f = open('var.json')
jsondata = json.load(f)

cloudinary.config( 
  cloud_name = "pshop", 
  api_key = "459352598841221", 
  api_secret = jsondata["cloudinary"]
)

VIDEO=str(jsondata['VIDEO'])
key=str(jsondata['KEY'])
AUDIO=str(jsondata['AUDIO'])
AD=str(jsondata['AD'])
playAd=str(jsondata['playAd'])
interval=str(jsondata['interval'])
totalsongs=str(jsondata['totalsongs'])
command=str(jsondata['command'])+key
BackupCommand=str(jsondata['BackupCommand'])+key

f.close()

adCommand="ffmpeg -re -i ./media/ad/ad.mp4 -r 24 -f flv rtmp://a.rtmp.youtube.com/live2/"+key
current=1

print(command)
print(BackupCommand)
print(f'ad interval {interval}')
print(f'ad  playing {playAd}')
settingUp=True

def setup(): 
  global settingUp
  downloaded=path.exists("./media/music/1.mp3")
  addownloaded=path.exists("./media/ad/ad.mp4")
  
  if(not downloaded):
    result = cloudinary.Search().expression('folder:songs').max_results(200).execute()
    for r in result["resources"]:
      print(r["url"])    
      wget.download(r["url"],out='media/music')

  if(not addownloaded):
    gdown.download(id=AD,output='./media/ad/ad.mp4',quiet=False)
    
  settingUp=False


def commandtoplay(id):
  carray=command.split("./media/a.mp3")
  return carray[0]+" ./media/music/"+str(id)+".mp3 "+carray[1]

def main():
  thread = Thread(target = setup, args = ())
  thread.start()

  while settingUp:
    print("running backup stream")
    subprocess.run(BackupCommand,shell=True)
    
  while not settingUp:
    global current,totalsongs
    # thinking of a for loop but i need to change current in fitre by asking audience
    
    subprocess.run(commandtoplay(current),shell=True)
    if (totalsongs==current):
      current=1
    else:
      current+=1

    if(current % int(interval) == 0):
      subprocess.run(adCommand,shell=True)
      

main()