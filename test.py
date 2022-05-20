import subprocess


command=['ffmpeg', '-i', './media/backup/a.mp3', '-re', '-stream_loop', '-1', '-i', './media/bg1.mp4', '-vf', 'scale=-1:242', '-shortest', '-strict', '-2', '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '28', '-threads', '8', '-c:a', 'aac', '-b:v', '1500k', '-b:a', '192k', '-pix_fmt', 'yuv420p', '-r', '24', '-x264-params', 'keyint=36:min-keyint=24:scenecut=-1', '-shortest', '-f', 'flv', 'rtmp://a.rtmp.youtube.com/live2/mm56-xc3k-3dq5-5jfj-c9ac']

a=subprocess.run(" ".join(command),shell=True)
print(" ".join(command))