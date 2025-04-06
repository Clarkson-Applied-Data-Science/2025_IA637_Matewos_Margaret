from baseObject import baseObject
import pymysql
import hashlib
import random
from datetime import datetime

class user(baseObject):
    def __init__(self):
        self.setup()
        
        self.roles = [{'value':'admin','text':'admin'},{'value':'user','text':'user'}]
    def hashPassword(self,pw):
        pw = pw+'xyz'
        return hashlib.md5(pw.encode('utf-8')).hexdigest()
    def role_list(self):
        rl = []
        for item in self.roles:
            rl.append(item['value'])
        return rl
    
    def generate_accesscode(self):
        """Generate a random 6-digit AccessCode and ensure it is unique."""
        while True:
            accesscode = random.randint(100000, 999999) 
            u = user()
            u.getByField('AccessCode', str(accesscode)) 
            if len(u.data) == 0: 
                return accesscode
    def verify_new(self, n=0):
        self.errors = []

        if len(self.data[n]['Fname']) < 2:
            self.errors.append('First Name must be at least 2 characters.')

        if len(self.data[n]['Lname']) < 2:
            self.errors.append('Last Name must be at least 2 characters.')

        if '@' not in self.data[n]['email']:
            self.errors.append('Email must contain @')

        if self.data[n]['role'] not in self.role_list():
            self.errors.append(f'Role must be one of {self.role_list()}')

        u = user()
        u.getByField('email', self.data[n]['email'])
        if len(u.data) > 0:
            self.errors.append(f"Email address is already in use. ({self.data[n]['email']})")
        u.getByField('UserName', self.data[n]['UserName'])
        if len(u.data) > 0:
            self.errors.append(f"Username is already taken. ({self.data[n]['UserName']})")
        if len(self.data[n]['UserName']) < 3:
            self.errors.append('Username must be at least 3 characters.')
        if len(self.data[n]['password']) < 3:
            self.errors.append('Password should be greater than 3 chars.')
        if self.data[n]['password'] != self.data[n]['password2']:
            self.errors.append('Retyped password must match.')

        self.data[n]['password'] = self.hashPassword(self.data[n]['password'])

        self.data[n]['AccessCode'] = self.generate_accesscode()

        self.data[n]['CreatedTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return len(self.errors) == 0

    def verify_update(self, n=0):
        self.errors = []

        if '@' not in self.data[n]['email']:
            self.errors.append('Email must contain @')

        if self.data[n]['role'] not in self.role_list():
            self.errors.append(f'Role must be one of {self.role_list()}')

        u = user()
        u.getByField('email', self.data[n]['email'])
        if len(u.data) > 0 and u.data[0][u.pk] != self.data[n][self.pk]:
            self.errors.append(f"Email address is already in use. ({self.data[n]['email']})")

        u.getByField('UserName', self.data[n]['UserName'])
        if len(u.data) > 0 and u.data[0][u.pk] != self.data[n][self.pk]:
            self.errors.append(f"Username is already taken. ({self.data[n]['UserName']})")
        if len(self.data[n]['UserName']) < 3:
            self.errors.append('Username must be at least 3 characters.')

        if 'password' in self.data[n] and self.data[n]['password']:
            if len(self.data[n]['password']) < 3:
                self.errors.append('Password needs to be more than 3 chars.')
            else:
                self.data[n]['password'] = self.hashPassword(self.data[n]['password'])

        if 'AccessCode' in self.data[n]:
            new_accesscode = self.data[n]['AccessCode']
            if new_accesscode:
                u.getByField('AccessCode', str(new_accesscode))
                if len(u.data) > 0 and u.data[0][u.pk] != self.data[n][self.pk]:
                    self.errors.append(f"AccessCode {new_accesscode} has already been used.")

        if len(self.errors) == 0:
            return True
        else:
            return False
    
    def tryLogin(self,email,pw):
        pw = self.hashPassword(pw)
        sql = f'SELECT * FROM `{self.tn}` WHERE `email` = %s AND `password` = %s;'
        tokens = [email,pw]
        print(sql,tokens)
        self.cur.execute(sql,tokens)
        self.data = []
        for row in self.cur:
            self.data.append(row)
        if len(self.data) == 1: 
            return True
        else:
            return False
