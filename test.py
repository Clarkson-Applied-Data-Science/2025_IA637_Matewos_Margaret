from user import user
import datetime

u = user()
if not u.cur:
    print("Database connection failed in baseObject setup")
    exit()  # Stop execution if the database isn't connected

table = 'mm_user'
fields = ['Fname', 'Lname', 'email', 'role', 'UserName','PasswordHash', 'AccessCode', 'CreatedTime']

d = {}
d['Lname'] = 'Dorothy'
d['Fname'] = 'Ruta'
d['email'] = 'r.ruta@d.com'
d['role'] = 'admin'
d['UserName'] = 'dorothy.ruta'
d['password'] = 'pass123'
d['password2'] = 'pass123'   # raw password

d['AccessCode'] = 1130
d['CreatedTime'] = datetime.datetime.now()

u.set(d)


if u.verify_new():
    u.insert()
    print("User registered successfully!")
else:
    print("Errors:", u.errors)


