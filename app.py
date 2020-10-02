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
    with open('tuition_cost.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            college_names.append(row['name'])
    print(list(college_names))
    return jsonify(college_names)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)