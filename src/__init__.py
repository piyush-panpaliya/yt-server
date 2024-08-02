from .server import app
from os import path, mkdir, system

if not path.exists('media'):
  mkdir('media')
  mkdir('media/ad')
  mkdir('media/music')
  mkdir('media/video')
  mkdir('media/zip')

if not path.exists("data.db"):
  system("touch data.db && echo '{}' > data.db")
