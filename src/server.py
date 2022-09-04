from flask import Flask, request,make_response,jsonify
# from flask_login import LoginManager,login_required,login_user
import pickledb
import os
import multiprocessing
from functools import wraps
from src.main import main,mediaThread
from src.variable import *

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


db = pickledb.load('data.db', True)
if not db.get('users'):
    db.dcreate('users')

if not db.get('songs'):
    db.dcreate('songs')

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

ytthread =multiprocessing.Process(target = main)

@app.route('/server', methods=['PUT', 'DELETE'])
@token_required
def startyt():
  global ytthread
  if request.method == 'PUT':
    if not ytthread.is_alive():
      ytthread.start()
      return {"status": "started"}
    return "already running"

  elif request.method == 'DELETE':
    if  ytthread.is_alive():
      ytthread.terminate()
      if mediaThread.is_alive():
        mediaThread.join(600)
        print("stopping after media download complete")
      ytthread=multiprocessing.Process(target=main, args=())
      return {"status": "stoped"}
    return {"status":"not started"}


@app.route('/config', methods=['GET', 'POST'])
@token_required
def config():
    if request.method == 'POST':
        newconfig = request.json
        # schema validation of newconfig
        db.set('config', newconfig)
    return db.get('config')



