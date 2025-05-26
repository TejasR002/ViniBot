# Class that manages the patient database
from tools.tools import request_user_input
from langchain_core.tools import  tool
class PatientDBTools:
    def __init__(self, db):
        self.db = db
    def query_patient(self, query: str) -> str:
        """Query patient record by name."""
        for name in self.db:
            if name.lower() in query.lower():
                return f"{name}'s record: {self.db[name]}"
        return "Patient not found."

    def insert_patient(self, query: str) -> str:
        # Expect format: "Insert John, 32, flu"
        try:
            _, data = query.split("Insert", 1)
            name, age, condition = map(str.strip, data.split(","))
            self.db[name] = {"age": int(age), "condition": condition}
            return f"Inserted patient: {name}"
        except Exception as e:
            return f"Error parsing insert query: {e}"

    def update_patient(self, query: str) -> str:
        # Expect format: "Update John, age=35, condition=cold"
        try:
            _, data = query.split("Update", 1)
            parts = [p.strip() for p in data.split(",")]
            name = parts[0]
            updates = {k.strip(): v.strip() for k, v in (p.split("=") for p in parts[1:])}
            if name in self.db:
                self.db[name].update(updates)
                return f"Updated {name}'s record."
            else:
                return "Patient not found."
        except Exception as e:
            return f"Error parsing update query: {e}"

    def delete_patient(self, query: str) -> str:
        # Expect format: "Delete John"
        try:
            _, name = query.split("Delete", 1)
            name = name.strip()
            if name in self.db:
                del self.db[name]
                return f"Deleted patient: {name}"
            else:
                return "Patient not found."
        except Exception as e:
            return f"Error parsing delete query: {e}"