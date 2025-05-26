from  typing import List

class medicineDBTools:
    def __init__(self, db):
        self.db = db
    def get_stock(self,query:str)-> List[str]:
        if query in self.db:
            return [f"available stock of {query} is {self.db[query]}"]
        return ["Not available in data  or Enter correct name"]

    def list_available(self,query:str)->List[str]:
        total_medicine = []
        for _ in self.db:
            total_medicine.append(f"{_} - {self.db[_]}")
            print()
        return total_medicine


