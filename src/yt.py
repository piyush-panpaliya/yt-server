import subprocess
from os import path,system
import gdown
from db import *
import random 


adCommand="ffmpeg -re -i ./media/ad/ad.mp4 -shortest -f flv "+dbget('KEY')
downloaded=path.exists("./media/music/1.mp3") 
gif="2.mp4"

def downloadMedia(): 
  dbset('downloading',True)
  downloaded=path.exists("./media/music/1.mp3") 
  videodownloaded=path.exists("./media/video/bg1.mp4")
  addownloaded=path.exists("./media/ad/ad.mp4")
  gifdownloaded=path.exists("./media/video/gif/2.mp4")

  if(not downloaded):
    gdown.download(id=dbget('AUDIO'),output='./media/zip/audio.zip',quiet=True)
    subprocess.run("unzip -j ./media/zip/audio.zip -d ./media/music && rm ./media/zip/audio.zip",shell=True)

  if(not addownloaded):
    gdown.download(id=dbget('AD'),output='./media/ad/ad.mp4',quiet=True)
    
  if(not gifdownloaded):
    gdown.download(id=dbget('GIF'),output='./media/zip/gif.zip',quiet=True)
    subprocess.run("unzip -j ./media/zip/gif.zip -d ./media/video/gif && rm ./media/zip/gif.zip",shell=True)

  if(not videodownloaded):
    gdown.download(id=dbget('VIDEO'),output='./media/video/bg1.mp4',quiet=True)

  print("downloaded media")
  
  dbset('downloading',False)
  return


def commandtoplay(id):
  global gif
  agif=os.listdir("./media/video/gif/")

  if(len(agif)==0):
    gif="backup.gif"

  elif(id%5==0):
    gif=random.choice(agif)

  command=dbget('command')+dbget('KEY')
  carray=command.split("break")
  z= (
    carray[0]+" ./media/music/"+str(id)+".mp3 "+
    carray[1]+" ./media/video/gif/"+gif+
    carray[2]+'"'+db.lget('songs',int(id)-1)["name"]+'"'+
    carray[3]
  )
  return z

def stream():
  BackupCommand=dbget('backupCommand')+dbget('KEY')
  adInterval=dbget('adInterval')
  playAd=dbget('playAd')

  while dbget('downloading'):
    print("running backup stream")
    if not downloaded:
      subprocess.run(BackupCommand,shell=True)
    
  while not dbget('downloading'):
    current=dbget('current')
    subprocess.run(commandtoplay(current),shell=True)

    print("running "+str(current))

    if (dbget('totalsongs')==current):
      dbset('current',1)
    else:
      dbset('current',int(current)+1)

    if(current % int(adInterval) == 0 and playAd):
      print("running ad")
      subprocess.run(adCommand,shell=True)

