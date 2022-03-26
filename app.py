from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

#Global variables with yoga data
YOGA_PATH = app.root_path +'/classes.csv'
YOGA_KEYS = ['name','type','level','date','duration','trainer','description']

#reads data
with open(YOGA_PATH, 'r') as csvfile:
   data = csv.DictReader(csvfile)
   class_dict = {row['name']:{'name':row['name'], 'type':row['type'], 'level':row['level'], 'date':row['date'], 'duration':row['duration'], 'trainer':row['trainer'], 'description':row['description']} for row in data}

#Routes to different pages of the site
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/classes')
def classes():
    return render_template("classes.html")