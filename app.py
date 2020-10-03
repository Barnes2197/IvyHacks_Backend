from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import csv
from flask import json
import traceback
import os
from dotenv import load_dotenv



app = Flask(__name__)
app.config["DEBUG"] = False

schools = {}

#Loads schools in-memory so that calls to apis don't hit the database more than needed
@app.before_first_request
def load_data():

    #Tries to get entries from Firebase first and fallsback to csv if firebase errors out

    try:
        #Loads db credentials and tries to establish a connection
        load_dotenv(verbose=True)
        cred = credentials.Certificate(json.loads(os.getenv("SERVICE_ACCOUNT_JSON")))
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        docs = db.collection(u'tuition_cost').stream()

        for doc in docs:
            school = doc.to_dict()
            if school:
                schools[school['name']] = school

        print('Using Firebase to retrieve Entries')
        
    except:
        print(f'Exception occured using firebase:{ traceback.format_exc() }, Using CSV instead')

        with open('tuition_cost.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if '/' in row['name']:
                    row['name'] = row['name'].replace('/', ' ')
                schools[row['name']] = row


@app.route('/', methods=['GET'])
def home():
    response = {}
    response['message'] = 'Hello'
    return jsonify(response)

@app.route('/names', methods=['GET'])
def names():
    college_names = []
    for school in schools.items():
            college_names.append(school[0])
        
    return jsonify(college_names)

@app.route('/tuition', methods=['GET'])
def tuition():
    school_name = request.args['name']
    print(request.args['name'])
    tuition_cost = {}
    try:
        tuition_cost['in_state_tuition'] = schools[school_name]['in_state_tuition']
        tuition_cost['out_of_state_tuition'] = schools[school_name]['out_of_state_tuition']
        return jsonify(tuition_cost)
    except:
        return 'School name not in database'


if __name__ == '__main__':
    app.run(threaded=True, port=5000)