from baseObject import baseObject
from datetime import datetime
from participants import participant_codes

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


    def getActiveExperiments(self):
        
        sql = f'SELECT ExperimentID, Description FROM `{self.tn}` WHERE `StartDate` <= NOW() AND `EndDate` >= NOW();'
        
        self.cur.execute(sql)
        self.data = []
        for row in self.cur:
            self.data.append(row)

    def generate_access_code(self, experiment_id):
        pc = participant_codes()
        access_code = pc.create_code(experiment_id)
        return access_code
    
    def getCreatedBy(self):
        sql = f'SELECT * FROM `mm_experiment` LEFT JOIN `mm_user` ON `mm_user`.`UserID`  = `mm_experiment`.`Creator_UserID`;'
        print(sql)
        self.cur.execute(sql)
        self.data = []
        for row in self.cur:
            self.data.append(row)