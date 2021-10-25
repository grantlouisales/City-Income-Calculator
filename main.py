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
    print("\nThis program will allow you to add users, remove users, get state info, "
          "difference of cost index between two states, and check income compared to another "
          "states. Cost index is a way we can see the average cost of living in states. "
          "For example Idaho has a cost index of 92.300. For cost index we want to see this "
          "as a percentage so, 92.3%. We go off of a average cost of living price nationwide. To "
          "make this easier lets say that average is $10,000. This percentage will be compared "
          "to the average price of $10,000. Idaho average cost of living would be equal to "
          "$10,000 * 92.3% which will come out to $9,230 for the average cost of living for Idaho.")

def compare_income_to_other_state(person, state, db):
    """
    Purpose:
    Return:
    """
    person_result = db.collection("Persons").document(person).get()
    state_result = db.collection("States").document(state).get()

    if person_result.exists and state_result.exists:
        person_data = person_result.to_dict()
        state_data = state_result.to_dict()

        person = User(person, person_data["State"], person_data["Income"])
        person_state_data = db.collection("States").document(person._get_state()).get()

        if person_state_data.exists:
            state1_data = person_state_data.to_dict()

            state1 = StateInfo(state1_data)
            state2 = StateInfo(state_data)

            print(f"\nLets take {person._get_name()}'s income for an example. To put it into perspective let's "
                "make their income the nationwide median price. If the income is 5000 then "
                "a state with 50 cost index would come out to 2500 overall cost of living. We are going to use "
                f"{person._get_name()}'s current living state and their index.\n")

            income = float(person._get_monthly_income())
            cost_index1 = float(state1._get_cost_index())
            cost_index2 = float(state2._get_cost_index())
            
            state_1_total = income * (cost_index1 / 100)
            state_2_total = income * (cost_index2 / 100)

            print(f"Going off of {person._get_name()}'s income as the nationwide medium, In their "
                  f"state of {state1._get_name()} they would only need ${state_1_total} to live comfortably. "
                  f"For them to live comfortably in {state2._get_name()} they would need ${state_2_total}.")

        else:
            print("One of these does not exists")

        
    else:
        print("One of these does not exists")



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

    print(f"\n{state_1} - {state_1_cost_index} || {state_2} - {state_2_cost_index}")

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
    valid = True

    description()
    while valid:
        display_menu()
        choice = input("Please choose a number> ")

        if choice == "1":
            name = input("Please enter the name of the person to be added> ")
            state = input("Please enter the state of the person to be added> ")
            monthly_income = input("Please enter the monthly income of the person to be added> ")
            add_person(name, state, monthly_income, db)

        elif choice == "2":
            name = input("Please enter the name of the person to be removed> ")
            remove_person(name, db)

        elif choice == "3":
            state1 = input("Please enter the name of the state you want to check> ")
            state2 = input("Please enter the name of the second state you want to check> ")
            state_cost_index_difference(state1, state2, db)

        elif choice == "4":
            state_info = input("Please enter the name of the state you want to get info on> ")
            get_state_info(state_info, db)

        elif choice == "5":
            name = input("Please enter the name of the person to be looked at> ")
            state = input("Please enter the state you want to look at> ")
            compare_income_to_other_state(name, state, db)

        elif choice == "6":
            valid = False


if __name__ == "__main__":
    main()
