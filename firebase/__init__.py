import os
from flask import Flask
import pyrebase

app = Flask(__name__)
app.secret_key = "mysecretkey"


firebaseconfig = {
    'apiKey': "AIzaSyDhLCXmpKUKgRizqz1C8zm569Z48vF4zzo",
    'authDomain': "mydb-21ab8.firebaseapp.com",
    'projectId': "mydb-21ab8",
    'storageBucket': "mydb-21ab8.appspot.com",
    'messagingSenderId': "850639472145",
    'appId': "1:850639472145:web:b1c7e6b88b9d1a052bd3b0",
    'measurementId': "G-L7VXZWECQE",
    'databaseURL': "https://mydb-21ab8-default-rtdb.firebaseio.com/"
  }

firebase = pyrebase.initialize_app(firebaseconfig)
auth = firebase.auth()
storage = firebase.storage()
db = firebase.database()

from firebase.users.views import users
# from firebase.core.views import core
# from firebase.error_pages.handlers import error_pages

app.register_blueprint(users)
# app.register_blueprint(error_pages)
# app.register_blueprint(core)



# <div class="blog">
#                     <p><span style="font-size: 1.7rem; font-weight: 600;">TITLE : {{post['title']}}</span></p>
#                     <h2>Written By : <a href="/profile/{{user['username']}}">{{post['author']}}</a></h2>
#                     <p>Published on : {{post['date']}}</p>
#                     <p><span style="font-size: 1.7rem; font-weight: 600;">Post : </span>{{post['text']}}</p>
#                 </div>