import json
from flask import Flask, request,make_response,jsonify
# from flask_login import LoginManager,login_required,login_user
from db import *
import os
import multiprocessing
from functools import wraps
from main import main,mediaThread

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Authentication decorator
def token_required(f):
  @wraps(f)
  def decorator(*args, **kwargs):
    token = None
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']

    if not token: 
        return make_response(jsonify({"message": "A valid token is missing!"}), 401)
    if token==os.environ['accessToken']:
      return f( *args, **kwargs)
  return decorator



@app.route('/')
@token_required
def home():
    return "hello, this is the home page"

ytthread=True

@app.route('/server', methods=['PUT', 'DELETE'])
@token_required
def startyt():
  global ytthread
  if request.method == 'PUT':
    if ytthread==True:
      db.dadd('config',('running', True))
      ytthread=multiprocessing.Process(target = main)
      ytthread.start()
      return {"status": "started"}
    return {"status":"already running"}

  elif request.method == 'DELETE':
    if ytthread!=True:
      if  ytthread.is_alive():
        ytthread.terminate()
        dbset('running', False)
        if mediaThread.is_alive():
          mediaThread.join(600)
          print("stopping after media download complete")
        ytthread=True
        return {"status": "stopped"}
    return {"status":"not started"}


@app.route('/config', methods=['GET', 'POST'])
@token_required
def config():
  if request.method == 'POST':
    newconfig = request.json
    unchanged={"running":dbget("running"),"downloading":dbget("downloading"),"current":dbget("current")}
    upConfig={**newconfig,**unchanged}
    db.set('config', upConfig)
  return db.dgetall('config')

@app.route('/songs', methods=['GET', 'POST'])
@token_required
def setsong():
  if request.method == 'POST':
    newSong = request.json
    for key in newSong:
      db.ladd('songs',key)
  return json.dumps(db.lgetall('songs'))


@app.route('/song', methods=['GET'])
def song():
  iid = dbget('current')
  isong=db.lget('songs',iid-1)
  return isong["name"]
