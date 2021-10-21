import firebase_admin
import json
from StatesInfo import StateInfo
from firebase_admin import credentials
from firebase_admin import firestore
from StatesInfo import StateInfo
from User import User


def open_data(filename):
    """
    Purpose: Reads a json and loads it into a variable.
    Return: variable holding json information.
    """
    f = open(filename)
    data = json.load(f)

    return data

def main():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    # Stores client to firestore database.
    db = firestore.client()

    Grant = User("Grant Ales", "Rexburg", 5000)
    Jeremy = User("Jeremy Williams", "Lancing", 7000)
    Breanna = User("Breanna Ales", "Rexburg", 9000)

    Grant_data = {"name": Grant._get_name(), "City": Grant._get_city(), "income": Grant._get_monthly_income()}
    Jeremy_data = {"name": Jeremy._get_name(), "City": Jeremy._get_city(),"income": Jeremy._get_monthly_income()}
    Breanna_data = {"name": Breanna._get_name(), "City": Breanna._get_city(),"income": Breanna._get_monthly_income()}


    # # Set documents with known IDs and allow you to name the data.
    # db.collection("Persons").document("Grant Ales").set(Grant_data) # Document reference

    # # Set documents with auto generated IDs
    # db.collection("Persons").document("Jeremy Williams").set(Jeremy_data)  # Document reference

    # # Set documents with auto generated IDs
    # db.collection("Persons").document("Breanna Ales").set(Breanna_data)  # Document reference

    # Read Data
    # Getting a document with a known ID

    """
    x = input("Name: ")
    result = db.collection("Persons").document(x).get()

    # Make sure the collection document exists and make sure you convert it to dict.
    if result.exists:
        user_city = result.to_dict()
        print(user_city["City"])
    """
    data = open_data("States.json")

    # Loop through json file and add all the names to the firebase.
    for state in data:
        db.collection("States").document(state).set(data[state])

    result = db.collection("States").document("Idaho").get()
    if result.exists:
        city = result.to_dict()
        print(city)

    x = StateInfo(city)
    print(x._get_cost_index())

if __name__ == "__main__":
    main()
