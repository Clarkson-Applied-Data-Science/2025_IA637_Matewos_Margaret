
from baseObject import baseObject
from datetime import datetime
from questions import question  # to get QuestionType

class responses(baseObject):
    def __init__(self):
        self.setup()

    def verify_new(self, n=0):
        self.errors = []

        # UserID must be present
        if not self.data[n].get('UserID'):
            self.errors.append('UserID is required.')

        # QuestionID must be present
        if not self.data[n].get('QuestionID'):
            self.errors.append('QuestionID is required.')

        # Answer must not be empty
        answer = self.data[n].get('Answer')
        if answer is None or str(answer).strip() == '':
            self.errors.append('Answer cannot be empty.')

       
        if self.data[n].get('QuestionID'):
            q = question()
            q.getById(self.data[n]['QuestionID'])
            if len(q.data) > 0:
                q_type = q.data[0].get('QuestionType')

                # Extra validation only for scale questions
                if q_type == 'scale':
                    try:
                        val = int(answer)
                        if val < 1 or val > 5:
                            self.errors.append('Answer must be a number between 1 and 5 for scale questions.')
                    except ValueError:
                        self.errors.append('Answer must be a number between 1 and 5 for scale questions.')

                # For other types (open-ended, multiple-choice, rating) you could add more rules here if needed

            else:
                self.errors.append(f"QuestionID {self.data[n]['QuestionID']} does not exist.")

        # Set CreatedTime
        self.data[n]['CreatedTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return len(self.errors) == 0

    def verify_update(self, n=0):
        self.errors = []

        if 'Answer' in self.data[n]:
            answer = self.data[n]['Answer']
            if answer is None or str(answer).strip() == '':
                self.errors.append('Answer cannot be empty.')

        return len(self.errors) == 0
