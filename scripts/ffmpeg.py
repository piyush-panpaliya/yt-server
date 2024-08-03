import os
from src import yt


def run(songs):
  for i in songs:
    try:
      cmd = yt.commandtoplay(i)
      os.system(cmd)
    except Exception as e:
      print(e)
      print("error playing song")


songs = list(map(str, range(1, 11)))
while True:
  run(songs)
