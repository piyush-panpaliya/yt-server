import subprocess
from os import path
import gdown
from .db import *
import random


adCommand = "ffmpeg -re -i ./media/ad/ad.mp4 -shortest -f flv " + \
  db.dget('config', 'KEY')
downloaded = path.exists(
  "./media/music/1.mp3") and not db.dget('config', 'forceUpdateMusic')
BackupCommand = db.dget('config', 'backupCommand') + db.dget('config', 'KEY')
adInterval = db.dget('config', 'adInterval')
playAd = db.dget('config', 'playAd')

gif = "1.mp4"


def downloadMedia():
  global downloaded
  try:
    db.dadd('config', ('downloading', True))

    if (db.dget('config', 'forceUpdateMusic')):
      os.system('rm -r ./media/music/*')
      os.system('rm -r ./media/ad/*')
      os.system(
        'mv media/video/gif/backup.mp4 . && rm -r media/video/gif/* && mv backup.mp4 media/video/gif')
      os.system('rm ./media/video/bg1.mp4')

    downloaded = path.exists("./media/music/1.mp3")
    videodownloaded = path.exists("./media/video/bg1.mp4")
    addownloaded = path.exists("./media/ad/ad.mp4")
    gifdownloaded = path.exists("./media/video/gif/2.mp4")

    if (not downloaded):
      gdown.download(id=db.dget('config', 'AUDIO'),
                     output='media/zip/audio.zip', quiet=True)
      subprocess.run(
        "unzip -j media/zip/audio.zip -d media/music && rm media/zip/audio.zip", shell=True)

    if (not addownloaded):
      gdown.download(id=db.dget('config', 'AD'),
                     output='media/ad/ad.mp4', quiet=True)

    if (not gifdownloaded):
      gdown.download(id=db.dget('config', 'GIF'),
                     output='media/zip/gif.zip', quiet=True)
      subprocess.run(
        "unzip -j media/zip/gif.zip -d media/video/gif && rm media/zip/gif.zip", shell=True)

    if (not videodownloaded):
      gdown.download(id=db.dget('config', 'VIDEO'),
                     output='media/video/bg1.mp4', quiet=True)

    print("downloaded media")
  except Exception as e:
    print(e)
    print("error downloading media")
  finally:
    db.dadd('config', ('downloading', False))
  return


def commandtoplay(id):
  global gif
  agif = os.listdir("./media/video/gif/")

  if (len(agif) == 0):
    gif = "backup.mp4"

  elif (id % 5 == 0):
    gif = random.choice(agif)

  command = db.dget('config', 'command') + db.dget('config', 'KEY')
  carray = command.split("break")

  z = f"{carray[0]} \"./media/music/{str(id)}.mp3\" {carray[1]} \"./media/video/gif/{gif}\" {carray[2]} \"{db.lget('songs', int(id) - 1)['name']}\" {carray[3]}"
  return z


def stream():
  while db.dget('config', 'downloading'):
    print("running backup stream")
    if not downloaded:
      subprocess.run(BackupCommand, shell=True)

  while not db.dget('config', 'downloading'):
    current = db.dget('config', 'current')
    subprocess.run(commandtoplay(current), shell=True)

    print("running " + str(current))

    if (db.dget('config', 'totalsongs') <= int(current)):
      db.dadd('config', ('current', 1))
    else:
      db.dadd('config', ('current', int(current) + 1))

    if (int(current) % int(adInterval) == 0 and playAd):
      print("running ad")
      subprocess.run(adCommand, shell=True)
