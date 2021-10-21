from os import remove
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


def compare_income_to_state_cost_index(name, income, state_1, state_2, db):
    state_1_result = db.collection("States").document(state_1).get()
    state_2_result = db.collection("States").document(state_2).get()

    if state_1_result.exists and state_2_result:
            state1 = state_1_result.to_dict()
            state2 = state_2_result.to_dict()


    state_1 = StateInfo(state1)
    state_2 = StateInfo(state2)



def add_person(name, state, monthly_income, db):
    """
    Purpose: This function will add a person to the cloud
    database. It will create a class that will extract information
    and send it into the cloud database.

    Returns: Nothing. It will only add the give person to the database.
    """
    person = User(name, state, monthly_income)
    person_data = {"Name": person._get_name(), "State": person._get_state(), 
                   "Income": person._get_monthly_income()}

    db.collection("Persons").document(name).set(person_data)

def remove_person(name, db):
    """
    Purpose: This function will grab the document of the name given,
    then it will check to see if the document exists and if it 
    does, delete the document in the cloud database. If it does not exist,
    it will send an error message to the user.

    Returns: Nothing. It will either print out an error message or 
    delete the document specified.
    """
    result = db.collection("Persons").document(name)
    doc = result.get()
    if doc.exists:
        result.delete()
    else:
        print("This person does not exist in the system.")


def main():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    # Stores client to firestore database.
    db = firestore.client()

    data = open_data("States.json")
    add_person("Grant Ales", "Idaho", 5000, db)
    add_person("Breanna Ales", "Idaho", 8000, db)


    # compare_income_to_state_cost_index("Grant Ales", 5000, "Nevada", "Idaho", db)

    # # Set documents with known IDs and allow you to name the data.
    # db.collection("Persons").document("Grant Ales").set(Grant_data) # Document reference

    # # # Set documents with auto generated IDs
    # db.collection("Persons").document("Jeremy Williams").set(Jeremy_data)  # Document reference

    # # # Set documents with auto generated IDs
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
    
    # Loop through json file and add all the names to the firebase.
    for state in data:
        db.collection("States").document(state).set(data[state])

    # result = db.collection("States").document("Idaho").get()
    # if result.exists:
    #     city = result.to_dict()
    #     print(city)

if __name__ == "__main__":
    main()
