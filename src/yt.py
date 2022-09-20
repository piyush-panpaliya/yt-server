import subprocess
from os import path,system
import gdown
from db import *


downloaded=path.exists("./media/music/1.mp3") 
adCommand="ffmpeg -re -i ./media/ad/ad.mp4 -shortest -f flv rtmp://a.rtmp.youtube.com/live2/"+dbget('KEY')

def downloadMedia(): 
  dbset('downloading',True)
  downloaded=path.exists("./media/music") 
  videodownloaded=path.exists("./media/video/bg1.mp4")
  addownloaded=path.exists("./media/ad/ad.mp4")
  if(not downloaded):
    system("mkdir ./media/music")
    if path.exists("./media/zip"):
      system("rm -r  ./media/zip")      
    system("mkdir ./media/zip")

    gdown.download(id=dbget('AUDIO'),output='./media/zip/audio.zip',quiet=True)
    subprocess.run("unzip -j ./media/zip/audio.zip -d ./media/music && rm ./media/zip/audio.zip",shell=True)

  if(not addownloaded):
    gdown.download(id=dbget('AD'),output='./media/ad/ad.mp4',quiet=True)
    
  if(not videodownloaded):
    gdown.download(id=dbget('VIDEO'),output='./media/video/video.mp4',quiet=True)
  print("downloaded media")
  dbset('downloading',False)
  return


def commandtoplay(id):
  command=dbget('command')+dbget('KEY')
  carray=command.split("break")
  return carray[0]+" ./media/music/"+str(id)+".mp3 "+carray[1]+" ./media/video/bg1.mp4 "+carray[2]

def stream():
  BackupCommand=dbget('backupCommand')+dbget('KEY')
  adInterval=dbget('adInterval')
  playAd=dbget('playAd')
  while dbget('downloading'):
    print("running backup stream")
    if not downloaded:
      subprocess.run(BackupCommand,shell=True)
    
  while not  dbget('downloading'):

    subprocess.run(commandtoplay(dbget('current')),shell=True)
    print("running "+str(dbget('current')))
    if (dbget('totalsongs')==dbget('current')):
      dbset('current',1)
    else:
      dbset('current',int(dbget('current'))+1)

    if(dbget('current') % int(adInterval) == 0 and playAd):
      print("running ad")
      subprocess.run(adCommand,shell=True)

 
