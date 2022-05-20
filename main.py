import subprocess
import os
from google_drive_downloader import GoogleDriveDownloader as gdd
import time
from threading import Thread

# AUDIO="1-7nyfzwu9monpNry6l2qyEJkVIMN6kQ-"
# VIDEO="1-DFjo8aLalapsI1np168JiXjzK7HWw0Q"
VIDEO=str(os.environ['VIDEO'])
AUDIO=str(os.environ['AUDIO'])
# command=str(os.environ['cmd']).split() 
# BackupCommand=str(os.environ['bcmd']).split() 
command=['ffmpeg', '-i', './media/backup/a.mp3', '-re', '-stream_loop', '-1', '-i', './media/bg1.mp4', '-vf', 'scale=-1:720', '-shortest', '-strict', '-2', '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '28', '-threads', '8', '-c:a', 'aac', '-b:v', '1500k', '-b:a', '192k', '-pix_fmt', 'yuv420p', '-r', '24', '-x264-params', 'keyint=36:min-keyint=24:scenecut=-1', '-shortest', '-f', 'flv', 'rtmp://a.rtmp.youtube.com/live2/mm56-xc3k-3dq5-5jfj-c9ac']
BackupCommand=['ffmpeg', '-i', './media/a.mp3', '-re', '-stream_loop', '-1', '-i', './media/bg1.mp4', '-vf', 'scale=-1:720', '-shortest', '-strict', '-2', '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '28', '-threads', '8', '-c:a', 'aac', '-b:v', '1500k', '-b:a', '192k', '-pix_fmt', 'yuv420p', '-r', '24', '-x264-params', 'keyint=36:min-keyint=24:scenecut=-1', '-shortest', '-f', 'flv', 'rtmp://a.rtmp.youtube.com/live2/mm56-xc3k-3dq5-5jfj-c9ac']

print(command)
print(BackupCommand)
settingUp=True

def setup(): 
  global settingUp
  gdd.download_file_from_google_drive(file_id=AUDIO,dest_path='./media/a.mp3')
  #gdd.download_file_from_google_drive(file_id=VIDEO,dest_path='./media/bg1.mp4')
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