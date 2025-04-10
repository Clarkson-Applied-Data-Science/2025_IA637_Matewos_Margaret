from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, send_from_directory,make_response 
from flask_session import Session
from datetime import timedelta
import datetime
import os
from user import user
from experiments import experiments
from participants import participant_codes
import time

app = Flask(__name__,static_url_path='',
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

app.config['SECRET_KEY'] = '5sdghsgRTg'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)

@app.route('/')
def home():
    return redirect('/homepage')

@app.context_processor
def inject_user():
    return dict(me=session.get('user'))

def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    if value is None:
        return ''
    try:
        return value.strftime(format)
    except AttributeError:
        return 'NA'

app.jinja_env.filters['format_datetime'] = format_datetime

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    if 'user' in session:
        me = session['user']
    else:
        me = None

    # Fetch the experiment_id dynamically from the experiments table
    e = experiments()
    e.getAll() 
    experiment_id = e.data[0]['ExperimentID'] if e.data else None 

    if experiment_id is None:
        return render_template('error_dialog.html', msg="No active experiment found.")

    if request.method == 'POST':
        agree = request.form.get('agree')

        if agree == 'yes':
            # Create the access code and associate it with the experiment_id from the table
            access_code = participant_codes().create_code(experiment_id)
            
            # Store access code and experiment_id in session for later use
            session['experiment_id'] = experiment_id
            session['access_code'] = access_code

            # Redirect to the survey page
            return redirect(url_for('start_survey'))

        elif agree == 'no':
            return render_template('homepage.html', me=me)
    
    # Render the homepage template
    return render_template('homepage.html', me=me)


@app.route('/login',methods = ['GET','POST'])
def login():
    if request.form.get('name') is not None and request.form.get('password') is not None:
        u = user()
        if u.tryLogin(request.form.get('name'),request.form.get('password')):
            print("Login ok")
            session['user'] = u.data[0]
            session['active'] = time.time()
            return redirect('main')
        else:
            print("Login Failed")
            return render_template('login.html', title='Login', msg='Incorrect username or password.')
    else:   
        if 'msg' not in session.keys() or session['msg'] is None:
            m = 'Type your email and password to continue.'
        else:
            m = session['msg']
            session['msg'] = None
        return render_template('login.html', title='Login', msg=m)    
    
@app.route('/logout',methods = ['GET','POST'])
def logout():
    if session.get('user') is not None:
        del session['user']
        del session['active']
    return render_template('login.html', title='Login', msg='You have logged out.')

@app.route('/main')
def main():
    if checkSession() == False: 
        return redirect('/homepage')
    
    if session['user']['role'] == 'admin':
        return render_template('main.html', title='Main menu') 
    else:
        return render_template('homepage.html', title='Survey App') 

@app.route('/access/<code>')
def access_with_code(code):
    pc = participant_codes()
    experiment_id = pc.get_experiment_from_code(code)

    if experiment_id:
        e = experiments()
        e.getById(experiment_id)
        if not e.data:
            return render_template('error_dialog.html', msg="Experiment not found.")
        # You might want to store access in session for later use
        session['experiment_id'] = experiment_id
        session['access_code'] = code
        return redirect(url_for('start_survey'))  # Add this route too
    else:
        return render_template('error_dialog.html', msg="Invalid access code.")

@app.route('/users/manage',methods=['GET','POST'])
def manage_user():
    if checkSession() == False or session['user']['role'] != 'admin': 
        return redirect('/login')
    o = user()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action is not None and action == 'delete': #action=delete&pkval=123
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg= "Deleted.")
    if action is not None and action == 'insert':
        d = {}
        d['Fname'] = request.form.get('Fname')
        d['Lname'] = request.form.get('Lname')
        d['email'] = request.form.get('email')
        d['role'] = request.form.get('role')
        d['UserName'] = request.form.get('UserName')
        d['password'] = request.form.get('password')
        d['password2'] = request.form.get('password2')
        d['CreatedTime'] = datetime.datetime.now()
        o.set(d)
        
        if o.verify_new():
            #print(o.data)
            o.insert()
            return render_template('ok_dialog.html',msg= "User added.")
        else:
            return render_template('users/add.html',obj = o)
        

    if action is not None and action == 'update':
        o.getById(pkval)
        o.data[0]['Fname'] = request.form.get('Fname')
        o.data[0]['Lname'] = request.form.get('Lname')
        o.data[0]['email'] = request.form.get('email')
        o.data[0]['role'] = request.form.get('role')
        o.data[0]['UserName'] = request.form.get('UserName')
        o.data[0]['password'] = request.form.get('password')
        o.data[0]['password2'] = request.form.get('password2')
        
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html',msg= "User updated. ")
        else:
            return render_template('users/manage.html',obj = o)
    if pkval is None:
        o.getAll()
        return render_template('users/list.html',obj = o)
    if pkval == 'new':
        o.createBlank()
        
        return render_template('users/add.html',obj = o)
    else:
        print(pkval)
        o.getById(pkval)
        return render_template('users/manage.html',obj = o)
    
#####################################################################################################################
###################              Experiments:
#####################################################################################################################

@app.route('/experiments/manage', methods=['GET', 'POST'])
def manage_experiments():
    if checkSession() == False or session['user']['role'] != 'admin':
        return redirect('/login')
    
    e = experiments()  
    u = user()
    u.getAll()
    e.creators = u.data
    action = request.args.get('action')
    pkval = request.args.get('pkval')

    if action == 'delete' and pkval:
        e.deleteById(pkval)
        return render_template('ok_dialog.html', msg="Experiment deleted.")

    if action == 'insert':
        d = {}
        d['ExperimentName'] = request.form.get('ExperimentName')
        d['StartDate'] = request.form.get('StartDate')
        d['EndDate'] = request.form.get('EndDate')
        d['Description'] = request.form.get('Description')
        d['CreatedTime'] = datetime.datetime.now()
        d['UpdatedDate'] = request.form.get('UpdatedDate')
        d['Creator_UserID'] = request.form.get('Creator_UserID')
        
        e.set(d)

        if e.verify_new():
            e.insert()
            ExperimentID = e.data[0][e.pk] 
            pc = participant_codes()
            AccessCode = pc.create_code(ExperimentID)
            experiment_code = e.generate_experiment_code(ExperimentID) 
            e.data[0]['ExperimentCode'] = experiment_code 
            e.update() 
            return render_template('ok_dialog.html', msg="Experiment added.", code=AccessCode) 
        else:
            return render_template('experiments/add.html', obj=e)

    if action == 'update' and pkval:
        e.getById(pkval)
        if e.data:
            e.data[0]['ExperimentName'] = request.form.get('ExperimentName')
            e.data[0]['StartDate'] = request.form.get('StartDate')
            e.data[0]['EndDate'] = request.form.get('EndDate')
            e.data[0]['Description'] = request.form.get('Description')
            e.data[0]['UpdatedDate'] = datetime.datetime.now()
            e.data[0]['Creator_UserID'] = request.form.get('Creator_UserID')
            if e.verify_update():  
                e.update()
                return render_template('ok_dialog.html', msg="Experiment updated.")
            else:
                return render_template('experiments/manage.html', obj=e)
        else:
            return render_template('error_dialog.html', msg=f"Experiment with ID {pkval} was not found.")

    if pkval is None:
        e.getCreatedBy()
        return render_template('experiments/list.html', obj=e)

    if pkval == 'new':
        e.createBlank()
        return render_template('experiments/add.html', obj=e)

    else:
        e.getById(pkval)
        if e.data:
            return render_template('experiments/manage.html', obj=e)
        else:
            return render_template('error_dialog.html', msg=f"Experiment with ID {pkval} was not found.")
############################################################################################################################
######## Survey
############################################################################################################################

@app.route('/start_survey', methods=['GET', 'POST'])
def start_survey():
    if 'experiment_id' not in session or 'access_code' not in session:
        return redirect('/homepage')  
    experiment_id = session['experiment_id']
    access_code = session['access_code']

    if request.method == 'POST':
        pass

    return render_template('survey/start.html', experiment_id=experiment_id, access_code=access_code)


# endpoint route for static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

#standalone function to be called when we need to check if a user is logged in.
def checkSession():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']
        #print(timeSinceAct)
        if timeSinceAct > 500:
            session['msg'] = 'Your session has timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False   



if __name__ == '__main__':
   app.run(host='127.0.0.1',debug=True)   
