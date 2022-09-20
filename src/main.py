from db import dbget
from yt import downloadMedia, stream
from threading import Thread

mediaThread = Thread(target = downloadMedia, args = ())

def main():
  global ytthread
  print(dbget('command'))
  print(dbget('backupCommand'))
  print('ad adInterval'+str(dbget('adInterval')))
  print('ad  playing'+str(dbget('playAd')))
  mediaThread.start()
  
  stream()
  print('exiting script')
  ytthread=True
  return
 
