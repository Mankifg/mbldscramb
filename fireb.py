import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("rem.json")
firebase_admin.initialize_app(cred)

# Get a reference to the Firestore database
db = firestore.client()

data = db.collection('scrambles')

import json

def array_to_json(array):
    # Create a dictionary where each row of the array is keyed by its index
    json_obj = {str(i): row for i, row in enumerate(array)}
    # Convert dictionary to JSON string
    print(array)
    return json.dumps(json_obj)  
    
def json_to_array(json_string):
    if json_string is None:
        return None
    # Parse JSON string back into a dictionary
    json_obj = json.loads(json_string)
    # Convert the dictionary back to a 2D array, sorting by the keys to maintain order
    array = [json_obj[str(i)] for i in range(len(json_obj))]
    return array

def save(id,data):
    
    print(id,data)
    
    d2 = array_to_json(data)
    
    print(d2)
    
    db = firestore.Client()
    # [START firestore_data_set_from_map]
    # Add a new doc in collection 'cities' with ID 'LA'
    db.collection("scrambles").document(id).set({"scr":d2})


def read(id):
    data = db.collection('scrambles').document(id).get().to_dict()
    print(data)
    if data is None:
        return None
    return json_to_array(data.get("scr",None))

from datetime import datetime as dt

def id():
    return str(int(dt.now().timestamp()*10))
