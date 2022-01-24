from flask import Flask,render_template, request, flash, jsonify, session, redirect, url_for
from firebase import app


# client = pymongo.MongoClient('localhost', 27017)
# db = client.firstdb
# postdb = db["postdb"]

# app.secret_key = "mysecretkey"


if __name__ == '__main__':
    app.run(debug=True)
