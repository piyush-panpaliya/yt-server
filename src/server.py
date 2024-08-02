from .main import main, mediaThread
from functools import wraps
import multiprocessing
import os
from .db import *
from flask import Flask, request, make_response, jsonify
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


def token_required(f):
  @wraps(f)
  def decorator(*args, **kwargs):
    token = None
    if 'x-access-token' in request.headers:
      token = request.headers['x-access-token']

    if not token:
      return make_response(jsonify({"message": "A valid token is missing!"}), 401)
    if token == os.environ['accessToken']:
      return f(*args, **kwargs)
  return decorator


@app.route('/')
@token_required
def home():
  return "hello, this is the home page"


ytthread = None


@app.route('/server', methods=['PUT', 'DELETE'])
@token_required
def startyt():
  global ytthread
  if request.method == 'PUT':
    if ytthread is None or not ytthread.is_alive():
      db.dadd('config', ('running', True))
      ytthread = multiprocessing.Process(target=main)
      ytthread.start()
      return {"status": "started"}
    return {"status": "already running"}

  elif request.method == 'DELETE':
    if ytthread is not None and ytthread.is_alive():
      ytthread.terminate()
      db.dadd('config', ('running', False))
      if mediaThread is not None and mediaThread.is_alive():
        print("waiting for media download to complete")
        mediaThread.join(600)
        print("stopping after media download complete")
      ytthread = None
      return {"status": "stopped"}
    return {"status": "not started"}


@app.route('/config', methods=['GET', 'POST'])
@token_required
def config():
  if request.method == 'POST':
    newconfig = request.json
    unchanged = {"running": db.dget('config', "running"), "downloading": db.dget(
      'config', "downloading"), "current": db.dget('config', "current")}
    upConfig = {**newconfig, **unchanged}
    db.set('config', upConfig)
  return db.dgetall('config')


@app.route('/songs', methods=['GET', 'POST'])
@token_required
def setsong():
  if request.method == 'POST':
    newSong = request.json
    for key in newSong:
      db.ladd('songs', key)
  return json.dumps(db.lgetall('songs'))


@app.route('/song', methods=['GET'])
def song():
  iid = db.dget('config', 'current')
  isong = db.lget('songs', iid - 1)
  return isong["name"]
