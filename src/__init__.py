from .server import app
from os import path, mkdir, system

if not path.exists('media'):
  mkdir('media')
  mkdir('media/ad')
  mkdir('media/music')
  mkdir('media/video')
  mkdir('media/zip')

if not path.exists("db/data.db"):
  system("mkdir -p db && touch db/data.db && echo '{}' > db/data.db")
