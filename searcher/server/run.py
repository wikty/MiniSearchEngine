import json
from flask import Flask, Response, jsonify, request
from flask import send_from_directory, render_template, redirect, url_for
from flask import g

from .db_proxy import DBProxy
from .query import process

app = Flask(__name__)

# Database
def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = DBProxy()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

# @app.route("/h5/js/<path:path>")
# def send_js(path):
# 	return send_from_directory('js', path)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/q")
def q(query=None):
	query = request.args.get('query')
	if query:
		results = process(get_db(), query)
		return render_template('results.html', results=results, query=query)
	return redirect(url_for('index'))

def start():
	app.run()