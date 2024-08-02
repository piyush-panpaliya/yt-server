import os
from src.yt import commandtoplay


def run(songs):
  for i in songs:
    try:
      cmd = commandtoplay(i)
      os.system(cmd)
    except Exception as e:
      print(e)
      print("error playing song")


songs = list(map(str, range(1, 11)))
while True:
  run(songs)
