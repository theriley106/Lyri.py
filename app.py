from flask import Flask, render_template, request, url_for, redirect, Markup, send_from_directory, send_file
from datetime import datetime
import csv
from Music import *
import os
import time

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/ajax/index')
def ajax_index():
    time.sleep(5)
    return '<h1>Done!</h1>'

#<form action = "{{url_for('Add') }}" method = "post">

@app.route('/', methods=['POST'])
def Add():
	a = request.form.items()
	artist = a[0][1]
	song = a[1][1]
	file = SearchSong("{} {}".format(artist, song))
	print file
	return send_file(file, as_attachment=True)
	

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8888)
