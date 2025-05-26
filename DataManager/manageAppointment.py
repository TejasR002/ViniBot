
from typing import List


# 1 is for free
 # 0 is for booked



class appointmentDBTools:
    def __init__ (self,db):
        self.db = db
    def appointment_status(self,query)->bool:
        print("i am here")
        for _ in self.db:
            for idx in self.db[_] :
                for status in idx:
                    if idx[status]['status']:
                        return True
        return False

    def list_available(self,query:str) -> List[str]:
        available_slots = []
        for _ in self.db:
            for idx in self.db[_]:
                for status in idx:
                    if idx[status]['status']:
                        available_slots.append(list(idx.keys()))
        return available_slots


    def assign_slot(self,query:str):
        for _ in self.db:
            for idx in self.db[_]:
                for status in idx:
                    if idx[status]['status']:
                        idx[status]['status'] = 0
                        print(f"{idx} is assigned to you on date {_}")
                        return
        print("sorry no slot is available")




