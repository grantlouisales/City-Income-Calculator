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


def description():
    """
    Purpose: This function will describe all of the details of 
    the project. It will go over what cost index, grocery cost,
    housing cost, misc cost, transportation cost, and utilities cost
    is.

    Return: Nothing. This function will only print out a paragraph explaining
    everything. 
    """
    pass


def get_state_info(state, db):
    """
    Purpose: This will grab the state given by the user and
    output all of the information.

    Return: This function returns the function string overide
    with all of th estate information.
    """
    given_state = db.collection("States").document(state).get()

    if given_state.exists:
        state1 = given_state.to_dict()
    else:
        print("State does not exist in the database")
        return 

    state = StateInfo(state1)
    print(state)


def state_cost_index_difference(state_1, state_2, db):
    """
    Purpose: The function is meant to receive the information for
    the given states and find the difference in cost index between the
    two.

    Return: This function returns nothing. It will only return print 
    statements.
    """
    state_1_result = db.collection("States").document(state_1).get()
    state_2_result = db.collection("States").document(state_2).get()

    if state_1_result.exists and state_2_result.exists:
            state1 = state_1_result.to_dict()
            state2 = state_2_result.to_dict()
    else: 
        print("One of the given states were not correct")
        return 

    state_1_cost_index = StateInfo(state1)._get_cost_index()
    state_2_cost_index = StateInfo(state2)._get_cost_index()
    
    float_cost_index1 = float(state_1_cost_index)
    float_cost_index2 = float(state_2_cost_index)

    if float_cost_index1 > float_cost_index2:
        result = float_cost_index1 - float_cost_index2
        print(f"There is a {result:.0f} cost index decrease between "
              f"{StateInfo(state1)._get_name()} and {StateInfo(state2)._get_name()}")

    elif float_cost_index1 < float_cost_index2:
        result = float_cost_index2 - float_cost_index1
        print(f"There is a {result:.0f} cost index increase between "
              f"{StateInfo(state1)._get_name()} and {StateInfo(state2)._get_name()}")
    
    else:
        print(f"There is no difference between {StateInfo(state1)._get_name()}" 
              f" and {StateInfo(state2)._get_name()}")


def add_person(name, state, monthly_income, db):
    """
    Purpose: This function will add a person to the cloud
    database. It will create a class that will extract information
    and send it into the cloud database.

    Return: Nothing. It will only add the give person to the database.
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

    Return: Nothing. It will either print out an error message or 
    delete the document specified.
    """
    result = db.collection("Persons").document(name)
    doc = result.get()
    if doc.exists:
        result.delete()
    else:
        print("This person does not exist in the system.")


def display_menu():
    """
    Purpose: Prints out a simple menu to the user.

    Return: Nothing. It will only print out statements in
    this function.
    """
    print("\n==========================================")
    print("1. Add Person")
    print("2. Remove Person")
    print("3. Check the state cost index difference")
    print("4. Print out a states information")
    print("5. Check income compared to other state")
    print("6. Quit")
    print("==========================================\n")


def main():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    # Stores client to firestore database.
    db = firestore.client()
    data = open_data("States.json")
    valid = True

    display_menu()

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
    # for state in data:
    #     db.collection("States").document(state).set(data[state])

    # result = db.collection("States").document("Idaho").get()
    # if result.exists:
    #     city = result.to_dict()
    #     print(city)

if __name__ == "__main__":
    main()
