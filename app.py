from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import csv
from flask import json

from flask.signals import Namespace

# cred = credentials.Certificate("tuitionapisecrets.json")
# firebase_admin.initialize_app(cred)

# db = firestore.client()
# doc_ref = db.collection(u'tuition_cost')

app = Flask(__name__)
app.config["DEBUG"] = False
schools = {}
@app.before_first_request
def load_csv():
    with open('tuition_cost.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if '/' in row['name']:
                row['name'].replace('/', ' ')
            schools[row['name']] = row


@app.route('/', methods=['GET'])
def home():
    response = {}
    response['message'] = 'Hello'
    return jsonify(response)

@app.route('/names', methods=['GET'])
def names():

    # def school_has_name(school):
    #     try:
    #         name = school.get('name')
    #         return name
    #     except:
    #         print('school has no name')
    #         return ''
    #snapshots = doc_ref.get()
    #document.get('name') to retrieve all names

    college_names = []
    for school in schools.items():
            college_names.append(school[0])
        
    return jsonify(college_names)

@app.route('/tuition/', methods=['GET'])
def tuition():
    school_name = request.args['name']
    print(request.args['name'])
    tuition_cost = {}
    print(schools[school_name])
    try:
        tuition_cost['in_state_tuition'] = schools[school_name]['in_state_tuition']
        tuition_cost['out_of_state_tuition'] = schools[school_name]['out_of_state_tuition']
        return jsonify(tuition_cost)
    except:
        return 'School name not in database'



if __name__ == '__main__':
    app.run(threaded=True, port=5000)