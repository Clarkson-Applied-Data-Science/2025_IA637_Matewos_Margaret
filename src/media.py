from baseObject import baseObject
from datetime import datetime
from experiments import experiments  # For validating foreign key

class media(baseObject):
    def __init__(self):
        self.setup()
        self.valid_types = ['car', 'truck', 'motorcycle']

    def verify_new(self, n=0):
        self.errors = []

        # Validate FilePath
        if not self.data[n].get('FilePath') or len(self.data[n]['FilePath'].strip()) == 0:
            self.errors.append('FilePath is required.')

        # Validate AutomobileType
        if self.data[n].get('AutomobileType') not in self.valid_types:
            self.errors.append(f"AutomobileType must be one of: {', '.join(self.valid_types)}")

        # Validate Duration as positive number (seconds)
        try:
            duration = float(self.data[n]['Duration'])
            if duration <= 0:
                self.errors.append('Duration must be a positive number (in seconds).')
        except Exception:
            self.errors.append('Duration must be a number (in seconds).')

        # Set CreatedTime to now
        self.data[n]['CreatedTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Validate ExperimentID exists
        if not self.data[n].get('ExperimentID'):
            self.errors.append('ExperimentID is required.')
        else:
            exp = experiments()
            exp.getById(self.data[n]['ExperimentID'])
            if len(exp.data) == 0:
                self.errors.append(f"ExperimentID {self.data[n]['ExperimentID']} does not exist.")

        return len(self.errors) == 0

    def verify_update(self, n=0):
        self.errors = []

        # FilePath optional on update
        if 'FilePath' in self.data[n] and not self.data[n]['FilePath'].strip():
            self.errors.append('FilePath cannot be empty.')

        # Validate AutomobileType
        if 'AutomobileType' in self.data[n]:
            if self.data[n]['AutomobileType'] not in self.valid_types:
                self.errors.append(f"AutomobileType must be one of: {', '.join(self.valid_types)}")

        # Validate Duration as positive number (seconds)
        if 'Duration' in self.data[n]:
            try:
                duration = float(self.data[n]['Duration'])
                if duration <= 0:
                    self.errors.append('Duration must be a positive number (in seconds).')
            except Exception:
                self.errors.append('Duration must be a number (in seconds).')

        # Validate CreatedTime format if provided
        if 'CreatedTime' in self.data[n]:
            try:
                datetime.strptime(self.data[n]['CreatedTime'], '%Y-%m-%d %H:%M:%S')
            except Exception:
                self.errors.append('CreatedTime must be in YYYY-MM-DD HH:MM:SS format.')

        # Validate ExperimentID if updated
        if 'ExperimentID' in self.data[n]:
            exp = experiments()
            exp.getById(self.data[n]['ExperimentID'])
            if len(exp.data) == 0:
                self.errors.append(f"ExperimentID {self.data[n]['ExperimentID']} does not exist.")

        return len(self.errors) == 0
