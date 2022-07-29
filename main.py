import subprocess
import os
from os import path
import time
from threading import Thread
import gdown

# key="kdmf-1z1p-5e80-u4r8-dtw3"
# AUDIO="1lg_BvNgw4s_6y-xKNlpFf31jJdbP6tRq"
# VIDEO="1-DFjo8aLalapsI1np168JiXjzK7HWw0Q"
# BackupCommand="ffmpeg -i ./media/backup/a.mp3 -re -stream_loop -1 -i ./media/bg1.mp4 -map 0:a -map 1:v:0  -r 24 -f flv rtmp://a.rtmp.youtube.com/live2/"+key
# command="ffmpeg -i ./media/a.mp3 -re -stream_loop -1 -i ./media/bg1.mp4 -map 0:a -map 1:v:0  -r 24 -f flv rtmp://a.rtmp.youtube.com/live2/"+key
VIDEO=str(os.environ['VIDEO'])
key=str(os.environ['KEY'])
AUDIO=str(os.environ['AUDIO'])
command=str(os.environ['command'])+key
BackupCommand=str(os.environ['BackupCommand'])+key

print(command)
print(BackupCommand)
settingUp=True

def setup(): 
  global settingUp
  downloaded=path.exists("./media/a.mp3")
  if(not downloaded):
    gdown.download(id=AUDIO,output='./media/a.mp3',quiet=False)
#     gdown.download(id=VIDEO,output='./media/a.mp3',quiet=False)
  settingUp=False

def main():
  thread = Thread(target = setup, args = ())
  thread.start()

  while settingUp:
    print("running backup stream")
    subprocess.run(BackupCommand,shell=True)
  while True:
    subprocess.run(command,shell=True)

main()
