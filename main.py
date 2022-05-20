import subprocess
import os
from google_drive_downloader import GoogleDriveDownloader as gdd
import time
from threading import Thread

# BackupCommand=[
#   "echo",
#   "2"
# ]
# command=[
#   "echo",
#   "1"
# ]
# AUDIO="1-7nyfzwu9monpNry6l2qyEJkVIMN6kQ-"
# VIDEO="1-DFjo8aLalapsI1np168JiXjzK7HWw0Q"
VIDEO=str(os.environ['VIDEO'])
AUDIO=str(os.environ['AUDIO'])
command=str(os.environ['cmd']).split() 
BackupCommand=str(os.environ['bcmd']).split() 
print(command)
print(BackupCommand)
settingUp=True

def setup(): 
  global settingUp
  gdd.download_file_from_google_drive(file_id=AUDIO,dest_path='./media/a.mp3')
  ##gdd.download_file_from_google_drive(file_id=VIDEO,dest_path='./media/bg1.mp4')
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