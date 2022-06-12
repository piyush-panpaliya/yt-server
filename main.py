import subprocess
import os
from os import path
import time
from threading import Thread
import gdown

# AUDIO="1-7nyfzwu9monpNry6l2qyEJkVIMN6kQ-"
# VIDEO="1-DFjo8aLalapsI1np168JiXjzK7HWw0Q"
# BackupCommand="ffmpeg -i ./media/backup/a.mp3 -re -stream_loop -1 -i ./media/bg1.mp4 -map 0:a -map 1:v:0 -c:v copy -preset ultrafast -g 48 -bufsize 512k -crf 28 -threads 1 -c:a copy -b:v 1500k -b:a 192k -pix_fmt yuv420p -r 24  -shortest -f flv rtmp://a.rtmp.youtube.com/live2/42x8-5w0r-vhqq-wgpc-ehau"
# command="ffmpeg -i ./media/a.mp3 -re -stream_loop -1 -i ./media/bg1.mp4 -map 0:a -map 1:v:0 -c:v copy -preset ultrafast -g 48 -bufsize 512k -crf 28 -threads 1 -c:a copy -b:v 1500k -b:a 192k -pix_fmt yuv420p -r 24  -shortest -f flv rtmp://a.rtmp.youtube.com/live2/42x8-5w0r-vhqq-wgpc-ehau"
VIDEO=str(os.environ['VIDEO'])
AUDIO=str(os.environ['AUDIO'])
command=str(os.environ['cmd']) 
BackupCommand=str(os.environ['bcmd'])

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
    time.sleep(1)
    print("running backup stream")
    subprocess.run(BackupCommand,shell=True)
  while True:
    subprocess.run(command,shell=True)

main()
