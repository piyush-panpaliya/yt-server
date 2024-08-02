from .db import db
from .yt import downloadMedia, stream
from threading import Thread

mediaThread = Thread(target=downloadMedia, args=())


def main():
  global ytthread
  print(db.dget('config', 'command'))
  print(db.dget('config', 'backupCommand'))
  print('ad adInterval' + str(db.dget('config', 'adInterval')))
  print('ad  playing' + str(db.dget('config', 'playAd')))
  mediaThread.start()

  stream()
  print('exiting script')
  ytthread = None
  return
