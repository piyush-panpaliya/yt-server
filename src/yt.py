import subprocess
from os import path
import gdown
from variable import *

adCommand="ffmpeg -re -i ./media/ad/ad.mp4 -shortest -f flv rtmp://a.rtmp.youtube.com/live2/"+key

def downloadMedia(): 
  global downloading
  downloading=True
  downloaded=path.exists("./media/music/1.mp3") or forceUpdateMusic
  videodownloaded=path.exists("./media/video/bg1.mp4")
  addownloaded=path.exists("./media/ad/ad.mp4")
  if(not downloaded):
    gdown.download(id=AUDIO,output='./media/zip/audio.zip',quiet=True)
    subprocess.run("unzip ./media/zip/audio.zip -d ./media/music && rm ./media/zip/audio.zip",shell=True)

  if(not addownloaded):
    gdown.download(id=AD,output='./media/ad/ad.mp4',quiet=True)
    
  if(not videodownloaded):
    gdown.download(id=VIDEO,output='./media/video/video.mp4',quiet=True)
  print("downloaded media")
  downloading=False
  return


def commandtoplay(id):
  carray=command.split("break")
  return carray[0]+" ./media/music/"+str(id)+".mp3 "+carray[1]+" ./media/video/bg1.mp4 "+carray[2]

def stream():
  global current,totalsongs
  current=1
  while downloading:
    print("running backup stream")
    subprocess.run(BackupCommand,shell=True)
    
  while not downloading:

    subprocess.run(commandtoplay(current),shell=True)
    print("running "+str(current))
    if (totalsongs==current):
      current=1
    else:
      current+=1

    if(current % int(adInterval) == 0 and playAd):
      print("running ad")
      subprocess.run(adCommand,shell=True)

 