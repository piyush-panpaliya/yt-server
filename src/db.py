import pickledb
import os


if not os.path.exists("data.db"):
  os.system("touch data.db")

db = pickledb.load('data.db', True)


if not db.get('users'):
  db.dcreate('users')

if not db.get('songs'):
  db.lcreate('songs')

if not db.get('config'):
  db.dcreate('config')
  db.set('config',{"AD": "", "AUDIO": "", "KEY": "", "VIDEO": "", "adInterval": 3, "backupCommand": "ffmpeg -i ./media/backup/a.mp3 -re -stream_loop -1 -i ./media/video/bg1.mp4 -map 0:a -map 1:v:0   -shortest -hide_banner -loglevel error -f flv rtmp://a.rtmp.youtube.com/live2/","command": "ffmpeg -i break -re -stream_loop -1 -i break -map 0:a -map 1:v:0  -shortest -hide_banner -loglevel error -f flv rtmp://a.rtmp.youtube.com/live2/", "forceUpdateMusic": True, "playAd": False, "totalsongs": 50,"current":1,"running":False})


def dbset(name,value):
  return db.dadd('config',(name,value))

def dbget(name):
  return db.dget('config',name)