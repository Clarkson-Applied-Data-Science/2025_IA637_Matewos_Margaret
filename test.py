# # from user import user
# # import datetime

# # u = user()
# # if not u.cur:
# #     print("Database connection failed in baseObject setup")
# #     exit()  # Stop execution if the database isn't connected

# # table = 'mm_user'
# # fields = ['Fname', 'Lname', 'email', 'role', 'UserName','PasswordHash', 'AccessCode', 'CreatedTime']

# # d = {}
# # d['Lname'] = 'Dorothy'
# # d['Fname'] = 'Ruta'
# # d['email'] = 'r.ruta@d.com'
# # d['role'] = 'admin'
# # d['UserName'] = 'dorothy.ruta'
# # d['password'] = 'pass123'
# # d['password2'] = 'pass123'   # raw password

# # d['AccessCode'] = 1130
# # d['CreatedTime'] = datetime.datetime.now()

# # u.set(d)


# # if u.verify_new():
# #     u.insert()
# #     print("User registered successfully!")
# # else:
# #     print("Errors:", u.errors)


# import sys
# import os

# # # Add "src" to path
# sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# # from media import media

# # m = media()

# # # Test data
# # m.set({
# #     'FilePath': 'test_file.mp3',
# #     'AutomobileType': 'car',
# #     'Duration': '15',
# #     'ExperimentID': '3'
# # })

# # # Validate and insert
# # if m.verify_new(0):
# #     m.insert(0)  # <--- INSERTS INTO DB!
# #     print("Inserted into database!")
# # else:
# #     print("Validation failed.")
# #     print("Errors:", m.errors)
# # from questions import question

# # # Create a question object
# # q = question()

# # # Set the question data
# # q.set({
# #     'QuestionText': 'How annoying was the sound?',
# #     'QuestionType': 'scale',
# #     'ExperimentID': '1',
# #     'MediaID': '1'
# # })

# # # Validate and insert
# # if q.verify_new():
# #     q.insert()
# #     print("Question inserted successfully.")
# # else:
# #     print("Errors:", q.errors)

# from user import user

# u = user()

# u.set({
#     'Fname': 'Test',
#     'Lname': 'Admin',
#     'email': 'admin@test.com',
#     'UserName': 'admin',
#     'password': 'admin123',
#     'password2': 'admin123'
# })

# if u.verify_new():
#     u.insert()
#     print("User inserted successfully.")
# else:
#     print("Errors:", u.errors)


# from experiments import experiments
# from datetime import datetime

# e = experiments()
# e.set({
#     'ExperimentID': '1',
#     'StartDate': '2025-04-14',
#     'EndDate': '2025-04-20',
#     'Description': 'Test experiment from script',
#     'Creator_UserID': '1',
#     'CreatedTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# })

# if e.verify_new():
#     e.insert()
#     print("xperiment inserted successfully.")
# else:
#     print("Experiment failed. Errors:", e.errors)


# from experiments import experiments


# # Step 1: Load experiment by ID
# experiment_id = 8  # Change this ID if needed

# e = experiments()
# e.getById(experiment_id)

# if not e.data:
#     print(f"Experiment with ID {experiment_id} not found.")
# else:
#     # Step 2: Update the description
#     e.data[0]['Description'] += " (updated)"

#     # Step 3: Run verify_update and update
#     if e.verify_update():
#         e.update()
#         print(f"Experiment {experiment_id} updated successfully.")
#     else:
#         print("Update failed. Errors:", e.errors)
        
        
# from media import media


# m = media()

# m.set({
#     'FilePath': 'audio/car_sound_1.wav',
#     'AutomobileType': 'car',
#     'Duration': 3.45,
#     'CreatedTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#     'ExperimentID': 6  
# })

# if m.verify_new():
#     m.insert()
#     print("Media inserted successfully.")
# else:
#     print(" Media insert failed. Errors:", m.errors)
      
      
      
# from questions import question
# import datetime

# # Create question object
# q = question()

# # Check DB connection
# if not q.cur:
#     print("Database connection failed in baseObject setup")
#     exit()



# d = {}
# d['QuestionText'] = 'What vehicle do you hear in this sound?'
# d['QuestionType'] = 'multiple-choice'  # could also be 'open-ended' or 'scale'
# d['ExperimentID'] = 6  #  Replace with a valid experiment ID from your DB
# d['MediaID'] = 1        #  Replace with a valid media ID from your DB
# d['CreatedTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# q.set(d)

# if q.verify_new():
#     q.insert()
#     print("✅ Question inserted successfully!")
# else:
#     print("Errors:", q.errors)





# from responses import responses
# import datetime

# # Step 1: Create response object
# r = responses()

# # Step 2: Check if database connection is alive
# if not r.cur:
#     print("Database connection failed.")
#     exit()

# # Step 3: Set test data (change these IDs to match your DB)
# d = {}
# d['UserID'] = '2'     # Optional: can leave as '' or None for anonymous
# d['QuestionID'] = 2        # ✅ Replace with a valid question ID in your DB
# d['ExperimentID'] = 5 # ✅ Replace with a valid experiment ID in your DB
# d['Duration'] = 5

# # Pick an answer depending on the question type:
# # For 'multiple-choice' → e.g. "Truck"
# # For 'scale'           → e.g. "3"
# # For 'open-ended'      → e.g. "It sounds like a motorcycle"

# d['Answer'] = 'very annoying'  # Example for a scale question (1 to 5)

# # Timestamp
# d['CreatedTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# # Step 4: Set and validate
# r.set(d)

# if r.verify_new():
#     r.insert()
#     print("esponse inserted successfully!")
# else:
#     print("Response insert failed. Errors:", r.errors)



import sys
import os

# # # Add "src" to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from experiments import experiments
import datetime

# Step 1: Load experiment by ID
experiment_id = 6  # Change this ID if needed

e = experiments()
e.getById(experiment_id)

if not e.data:
    print(f"Experiment with ID {experiment_id} not found.")
else:
    # Step 2: Update the description
    e.data[0]['Description'] += " (updated)"

    # Step 3: Run verify_update and update
    if e.verify_update():
        e.update()
        print(f"Experiment {experiment_id} updated successfully.")
    else:
        print("Update failed. Errors:", e.errors)