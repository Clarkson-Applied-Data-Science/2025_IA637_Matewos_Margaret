from baseObject import baseObject
from datetime import datetime

class responses(baseObject):
    def __init__(self):
        self.setup()
    
    def verify_new(self, n=0):
        self.errors = []

        if not self.data[n].get('UserID'):
            self.errors.append('UserID is required.')

        if not self.data[n].get('QuestionID'):
            self.errors.append('QuestionID is required.')

        if not self.data[n].get('Answer') or len(self.data[n]['Answer'].strip()) < 1:
            self.errors.append('Answer cannot be empty.')

        # Set timestamp
        self.data[n]['CreatedTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return len(self.errors) == 0

    def verify_update(self, n=0):
        self.errors = []

        if 'Answer' in self.data[n] and len(self.data[n]['Answer'].strip()) < 1:
            self.errors.append('Answer cannot be empty.')

        return len(self.errors) == 0
