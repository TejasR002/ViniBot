from data.data import patients_db
from langchain_core.tools import  tool




@tool("request_user_input", return_direct=True)
def request_user_input(message: str) -> str:
    """Ask the user for input with a custom message."""
    return input(f"{message}\n> ")

@tool("get_patient_data", return_direct=True)
def get_patient_data(patient_name: str) -> dict:
    """Asks Patient for getting the data and added them to patients_db"""
    patient_data = {}
    data = ['Address', 'Age', 'Marital_status', 'sex', 'phone_no', 'mail']
    for d in data:
        if d != 'Age' or 'phone_name':
            patient_data[d] = input(f"Enter your {d}")
        else:
            patient_data[d] = int(input(f"Enter your {d}"))
    patients_db[patient_name] = patient_data
    return patient_data

@tool("show_details", return_direct=True)
def show_details(patient_name: str) -> dict:
    """Gives the  data of the patient from patient's name"""
    patient_data = patients_db[patient_name]
    return patient_data


@tool("find_patient_in_data", return_direct=False)
def find_patient_in_data(query: str) -> list:
    """Finds the patient(s) in the database based on the query"""
    available_patients = []
    for name, data in patients_db.items():
        if query.strip().lower() in name.lower():
            available_patients.append({name: patients_db[name]})
    return available_patients
