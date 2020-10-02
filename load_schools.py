import csv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("tuitionapisecrets.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
doc_ref = db.collection(u'tuition_cost')
with open('tuition_cost.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        doc_ref.document(row['name']).set(row)
        print(row['name'])


