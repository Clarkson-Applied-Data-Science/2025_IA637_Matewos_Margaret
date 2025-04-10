from baseObject import baseObject
import random, string

class participant_codes(baseObject):
    def __init__(self):
        self.setup()

    def generate_access_code(self, length=8):
        
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def create_code(self, experiment_id):
        code = self.generate_access_code()
        while self.code_exists(code):
            code = self.generate_access_code()  # regenerate the code if it already exists

        # Store the access code and the associated experiment_id in the participant table
        self.createBlank()
        self.data[0]['AccessCode'] = code
        self.data[0]['experiment_id'] = experiment_id
        self.insert()
        return code

    def code_exists(self, code):
        self.getByField('AccessCode', code)
        return len(self.data) > 0

    def get_experiment_from_code(self, code):
        self.getByField('AccessCode', code)
        return self.data[0]['experiment_id'] if self.data else None
