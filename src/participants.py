from baseObject import baseObject
import random, string

class participant_codes(baseObject):
    def __init__(self):
        self.setup()

    def generate_access_code(self, length=8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def create_code(self):
        code = self.generate_access_code()
        while self.code_exists(code):
            code = self.generate_access_code()
        self.createBlank()
        self.data[0]['AccessCode'] = code
        self.insert()
        return code

    def code_exists(self, code):
        self.getByField('AccessCode', code)
        return len(self.data) > 0

    def get_participant_id_from_code(self, code):
        self.getByField('AccessCode', code)
        if self.data:
            return self.data[0]['partitpant_code_id']
        else:
            return None