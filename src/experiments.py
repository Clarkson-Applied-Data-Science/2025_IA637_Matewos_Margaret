from baseObject import baseObject
from datetime import datetime

class experiments(baseObject):
   
    def __init__(self):
        self.setup()

    def verify_new(self, n=0):
        self.errors = []

        if len(self.data[n]['Description']) < 10:
            self.errors.append("Description must be at least 10 characters long.")

        start_date = datetime.strptime(self.data[n]['StartDate'], "%Y-%m-%d")
        end_date = datetime.strptime(self.data[n]['EndDate'], "%Y-%m-%d")
        if start_date >= end_date:
            self.errors.append("StartDate must be before EndDate.")

        self.data[n]['CreatedTime'] = datetime.now().strftime('%Y-%m-%d')

        return len(self.errors) == 0

    def verify_update(self, n=0):
        self.errors = []

        if len(self.data[n]['Description']) < 10:
            self.errors.append("Description must be at least 10 characters long.")

        start_date = datetime.strptime(self.data[n]['StartDate'], "%Y-%m-%d")
        end_date = datetime.strptime(self.data[n]['EndDate'], "%Y-%m-%d")
        if start_date >= end_date:
            self.errors.append("StartDate must be before EndDate.")

        self.data[n]['UpdatedDate'] = datetime.now().strftime('%Y-%m-%d')

        return len(self.errors) == 0
