from baseObject import baseObject
import hashlib
import random
from datetime import datetime

class user(baseObject):
    def __init__(self):
        self.setup()

    def hashPassword(self, pw):
        """Hashes a password with a static salt."""
        pw = pw + 'xyz'  # Simple salting (can be improved)
        return hashlib.md5(pw.encode('utf-8')).hexdigest()


    def verify_new(self, n=0):
        self.errors = []

        # First and last name validation
        if len(self.data[n].get('Fname', '').strip()) < 2:
            self.errors.append("First Name must be at least 2 characters.")

        if len(self.data[n].get('Lname', '').strip()) < 2:
            self.errors.append("Last Name must be at least 2 characters.")

        # Email validation
        email = self.data[n].get('email', '').strip()
        if '@' not in email:
            self.errors.append("Email must contain @")

        # Password validation
        pw1 = self.data[n].get('password', '')
        pw2 = self.data[n].get('password2', '')
        if len(pw1) < 3:
            self.errors.append("Password must be at least 3 characters.")
        if pw1 != pw2:
            self.errors.append("Retyped password must match.")

        # Email and Username uniqueness
        temp = user()
        temp.getByField('email', email)
        if len(temp.data) > 0:
            self.errors.append(f"Email address is already in use. ({email})")

        # If no errors, prepare data for insertion
        if len(self.errors) == 0:
            self.data[n]['password'] = self.hashPassword(pw1)
            self.data[n]['CreatedTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.data[n]['role'] = 'admin'  # Hardcoded role
            return True

        return False

    def verify_update(self, n=0):
        self.errors = []

        # Email and username
        email = self.data[n].get('email', '').strip()
        uname = self.data[n].get('UserName', '').strip()

        if '@' not in email:
            self.errors.append("Email must contain @")

        # Uniqueness check
        temp = user()
        temp.getByField('email', email)
        if len(temp.data) > 0 and temp.data[0][temp.pk] != self.data[n][self.pk]:
            self.errors.append(f"Email address is already in use. ({email})")

        # Password update (if provided)
        if 'password' in self.data[n] and self.data[n]['password']:
            if len(self.data[n]['password']) < 3:
                self.errors.append("Password must be at least 3 characters.")
            else:
                self.data[n]['password'] = self.hashPassword(self.data[n]['password'])

        return len(self.errors) == 0

    def tryLogin(self, email, pw):
        pw_hashed = self.hashPassword(pw)
        sql = f'SELECT * FROM `{self.tn}` WHERE `email` = %s AND `password` = %s AND `role` = "admin";'
        self.cur.execute(sql, [email, pw_hashed])
        self.data = [row for row in self.cur]
        return len(self.data) == 1
