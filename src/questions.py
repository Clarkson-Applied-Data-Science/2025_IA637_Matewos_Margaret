from baseObject import baseObject
from datetime import datetime
from experiments import experiments
from media import media

class question(baseObject):
    def __init__(self):
        self.setup()
        self.valid_types = ['open-ended', 'multiple-choice', 'scale']

    def verify_new(self, n=0):
        self.errors = []

        # Validate QuestionText
        if not self.data[n].get('QuestionText') or len(self.data[n]['QuestionText'].strip()) < 5:
            self.errors.append('QuestionText must be at least 5 characters long.')

        # Validate QuestionType
        question_type = self.data[n].get('QuestionType')
        if question_type not in self.valid_types:
            self.errors.append(f"QuestionType must be one of: {', '.join(self.valid_types)}")

        # Validate ExperimentID
        experiment_id = self.data[n].get('ExperimentID')
        if not experiment_id:
            self.errors.append('ExperimentID is required.')
        else:
            exp = experiments()
            exp.getById(experiment_id)
            if len(exp.data) == 0:
                self.errors.append(f"ExperimentID {experiment_id} does not exist.")

        # Validate MediaID
        media_id = self.data[n].get('MediaID')
        if not media_id:
            self.errors.append('MediaID is required.')
        else:
            m = media()
            m.getById(media_id)
            if len(m.data) == 0:
                self.errors.append(f"MediaID {media_id} does not exist.")

        # Set CreatedTime
        self.data[n]['CreatedTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return len(self.errors) == 0

    def verify_update(self, n=0):
        self.errors = []

        # Validate QuestionText if provided
        if 'QuestionText' in self.data[n] and len(self.data[n]['QuestionText'].strip()) < 5:
            self.errors.append('QuestionText must be at least 5 characters long.')

        # Validate QuestionType if provided
        if 'QuestionType' in self.data[n]:
            if self.data[n]['QuestionType'] not in self.valid_types:
                self.errors.append(f"QuestionType must be one of: {', '.join(self.valid_types)}")

        # Validate CreatedTime format (optional)
        if 'CreatedTime' in self.data[n]:
            try:
                datetime.strptime(self.data[n]['CreatedTime'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                self.errors.append('CreatedTime must be in YYYY-MM-DD HH:MM:SS format.')

        # Validate ExperimentID if provided
        if 'ExperimentID' in self.data[n]:
            exp = experiments()
            exp.getById(self.data[n]['ExperimentID'])
            if len(exp.data) == 0:
                self.errors.append(f"ExperimentID {self.data[n]['ExperimentID']} does not exist.")

        # Validate MediaID if provided
        if 'MediaID' in self.data[n]:
            m = media()
            m.getById(self.data[n]['MediaID'])
            if len(m.data) == 0:
                self.errors.append(f"MediaID {self.data[n]['MediaID']} does not exist.")

        return len(self.errors) == 0
