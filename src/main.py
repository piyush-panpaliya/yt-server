
from time import sleep
from src.variable import *
from src.yt import downloadMedia, stream

from threading import Thread

mediaThread = Thread(target = downloadMedia, args = ())

def main():
  print(command)
  print(BackupCommand)
  print(f'ad adInterval {adInterval}')
  print(f'ad  playing {playAd}')
  mediaThread.start()
  
  stream()
  print('exiting script')
  return
 
