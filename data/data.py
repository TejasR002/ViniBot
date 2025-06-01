from typing import Dict, List, Optional
from datetime import  date
# Dummy data for patients, appointments, and inventory
patients_db: Dict[str, Dict] = {
    "John Doe": {"Age": 30, "Gender": "Male","EmailAddress":"2x3osjs@gmail.com" ,"Address":"Simform","PhoneNumber":8564846546},
    "Jane Smith": {"Age": 25, "Gender": "Male","EmailAddress":"2x3osjs@gmail.com","Address":"Simform","PhoneNumber":6876416848},
    "Kanya waste":{"Age": 23, "Gender": "Female","EmailAddress":"2x3osjs@gmail.com","Address":"Simform","PhoneNumber":6852416848},
    "Janna Otega" :{"Age": 28, "Gender": "Female","EmailAddress":"2x3osjs@gmail.com","Address":"Simform","PhoneNumber":68522316848},
}

case_db:Dict[str,Dict] = {
    '1':{"Name":"John Doe ","prescription":"Aspirin","Disease":"flu","history": "No prior visits","next_visit":"after 5 days","current_date":date.today()},
    '3':{"Name":"Kanya waste","prescription":"Supatlotion","Disease":"skin disease","history": "one week ago visited","next_visit":"after 10 days","current_date":date.today()},
    '2':{"Name":"Jane Smith ","prescription":"Paracetamol","Disuses":"viral","history": "No prior visits","next_visit":"after 2 days","current_date":date.today()},
    '4':{"Name":"Janna Otega","prescription":"Move","Disuses":"neck pain","history": "one week ago","next_visit":"","current_date":date.today()}
}

appointments_schedule: Dict[str,list [ Dict[str,Dict]]] = {
    "2025-05-22":[ {'slot1':{"status":1}},
                  {'slot2':{"status":0}},
                  {'slot3':{"status":0}},
                  {'slot4':{"status":1}},
                  {'slot5':{"status":1}}],
    "2025-05-23": [{'slot1':{"status":1}},
                  {'slot2':{"status":1}},
                  {'slot3':{"status":0}},
                  {'slot4':{"status":1}},
                  {'slot5':{"status":0}}
    ]
}

medicine_inventory: Dict[str, int] = {
    "Paracetamol": 50,
    "Aspirin": 20,
    "Antibiotic": 10,
    "Supatlotion":20,
    "Move":60
}