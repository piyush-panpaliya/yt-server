import pickledb
import os

db = pickledb.load('db/data.db', True)

if not db.get('users'):
  db.lcreate('users')

if not db.get('songs'):
  db.lcreate('songs')

if not db.get('config'):
  db.dcreate('config')
  db.set('config', {"AD": "", "AUDIO": "", "KEY": "", "VIDEO": "", "GIF": "", "adInterval": 3,
                    "backupCommand": "ffmpeg -i ./media/backup/a.mp3 -re -stream_loop -1 -i ./media/video/backup.mp4 -map 0:a -map 1:v:0  -vf 'scale=-1:720' -shortest -strict -2 -c:v libx264 -preset ultrafast -crf 28 -threads 8 -c:a aac -b:v 1500k -b:a 192k -pix_fmt yuv420p -r 24 -x264-params keyint=36:min-keyint=24:scenecut=-1 -shortest -hide_banner -f flv rtmp://a.rtmp.youtube.com/live2/",
                    "command": "ffmpeg -i break -re -stream_loop -1 -i break -map 0:a -map 1:v:0  -vf 'scale=-1:720,drawtext=fontfile=font.otf:text=break:fontcolor=white:fontsize=44:x=20:y=20' -shortest -strict -2 -c:v libx264 -preset ultrafast -crf 28 -threads 8 -c:a aac -b:v 1500k -b:a 192k -pix_fmt yuv420p -r 24 -x264-params keyint=36:min-keyint=24:scenecut=-1  -shortest -hide_banner  -f flv rtmp://a.rtmp.youtube.com/live2/",
                    "forceUpdateMusic": True, "playAd": False, "totalsongs": 50, "current": 1, "running": False, "downloading": False})

db.dadd('config', ("current", 1))
db.dadd('config', ("running", False))
