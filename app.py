from flask import Flask, render_template, request, redirect, url_for
import csv
from operator import itemgetter

app = Flask(__name__)

#Global variables with yoga data
YOGA_PATH = app.root_path +'/classes.csv'
YOGA_KEYS = ['name','type','level','date','duration','trainer','description']

#reads data
def data_reader():
    with open(YOGA_PATH, 'r') as csvfile:
        data = csv.DictReader(csvfile)
        class_dict = {row['name']:{'name':row['name'], 'type':row['type'], 'level':row['level'], 'date':row['date'], 'duration':row['duration'], 'trainer':row['trainer'], 'description':row['description']} for row in data}
    
    sorted_dict = {}
    for entry in sorted(class_dict,key=itemgetter(4),reverse=True):
        sorted_dict[entry]=class_dict[entry]
    return sorted_dict


#Routes to different pages of the site

#index route
@app.route('/')
def index():
    return render_template("index.html")


#classes route
@app.route('/classes')
@app.route('/classes/<class_name>')
def classes(class_name=None):
    class_dict = data_reader()
    if class_name and class_name in class_dict.keys():
        varclass = class_dict[class_name]
        return render_template('class.html',varclass=varclass)
    else:
        return render_template("classes.html",class_dict=class_dict)


#gets dictionary from csv data
def get_classes():
    try:
        with open(YOGA_PATH, 'r') as csvfile:
            data = csv.DictReader(csvfile)
            classes = {}
            for entry in data:
                classes[entry['name']] = entry
    except Exception as e:
        print(e)
    return classes


# Saves dictionary to csv file
def set_classes(classes):
    try:
        with open(YOGA_PATH, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=YOGA_KEYS)
            writer.writeheader()
            for entry in classes.values():
                writer.writerow(entry)
    except Exception as err:
        print(err)

# Create a class route
@app.route('/classes/create', methods=['GET','POST'])
def class_form():
    if request.method == 'POST':
        # get csv data
        current_classes = get_classes()
    
        # create dict to hold new data
        new_classes = {}
        # add form data to new dict
        for key in YOGA_KEYS:
            new_classes[key]=request.form[key]
        # add new dict to csv data
        current_classes[request.form['name']]= new_classes
        # write csv data to csv file
        set_classes(current_classes)
        return redirect(url_for('classes'))
    else:
        return render_template("class_form.html",varclass=False)

# Edit a class route
@app.route('/classes/<class_name>/edit', methods=['GET','POST'])
def class_edit(class_name=None):
    if request.method == 'POST':
        # get csv data
        current_classes = get_classes()
    
        # create dict to hold new data
        new_classes = {}
        # add form data to new dict
        for key in YOGA_KEYS:
            new_classes[key]=request.form[key]
        # add new dict to csv data
        current_classes[class_name]= new_classes
        # write csv data to csv file
        set_classes(current_classes)
        return redirect(url_for('classes'))
    else:
        class_dict = data_reader()
        varclass = class_dict[class_name]
        return render_template('class_form.html',varclass=varclass)