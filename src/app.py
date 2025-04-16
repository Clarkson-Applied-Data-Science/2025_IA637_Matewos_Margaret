from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from flask_session import Session
from datetime import timedelta, datetime
import os, time
from user import user
from experiments import experiments

app = Flask(__name__, static_url_path='', template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))
print("Template folder:", app.template_folder)


app.config['SECRET_KEY'] = '5sdghsgRTg'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)

sess = Session()
sess.init_app(app)

@app.route('/')
def home():
    return redirect('/login')

@app.context_processor
def inject_user():
    return dict(me=session.get('user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = user()
        if u.tryLogin(request.form.get('name'), request.form.get('password')):
            session['user'] = u.data[0]
            session['active'] = time.time()
            return redirect('/main')
        else:
            return render_template('login.html', title='Login', msg='Incorrect username or password.')
    else:
        m = session.pop('msg', 'Type your email and password to continue.')
        return render_template('login.html', title='Login', msg=m)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html', title='Login', msg='You have logged out.')

@app.route('/main')
def main():
    if not checkSession():
        return redirect('/login')
    return render_template('main.html', title='Main menu')

@app.route('/users/manage', methods=['GET', 'POST'])
def manage_user():
    if not checkSession() or session['user']['role'] != 'admin': 
        return redirect('/login')

    o = user()
    action = request.args.get('action')
    pkval = request.args.get('pkval')

    if action == 'delete' and pkval:
        o.deleteById(pkval)
        return render_template('ok_dialog.html', msg="Deleted.")

    if action == 'insert':
        d = {
            'Fname': request.form.get('Fname'),
            'Lname': request.form.get('Lname'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'password2': request.form.get('password2'),
            'CreatedTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        o.set(d)
        default_dt = datetime.now().strftime('%Y-%m-%dT%H:%M')
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html', msg="User added.")
        else:
            return render_template('users/add.html', obj=o, default_dt=default_dt)

    if action == 'update' and pkval:
        o.getById(pkval)
        o.data[0].update({
            'Fname': request.form.get('Fname'),
            'Lname': request.form.get('Lname'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'password2': request.form.get('password2'),
            'CreatedTime': request.form.get('CreatedTime')
        })
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html', msg="User updated.")
        else:
            return render_template('users/manage.html', obj=o)

    if pkval is None:
        o.getAll()
        return render_template('users/list.html', obj=o)
    elif pkval == 'new':
        o.createBlank()
        default_dt = datetime.now().strftime('%Y-%m-%dT%H:%M')
        return render_template('users/add.html', obj=o, default_dt=default_dt)
    else:
        o.getById(pkval)
        return render_template('users/manage.html', obj=o)

##############################################################################
###################              Experiments:
############################################################################

@app.route('/experiments/manage', methods=['GET', 'POST'])
def manage_experiments():
    if not checkSession() or session['user']['role'] != 'admin':
        return redirect('/login')

    e = experiments()
    action = request.args.get('action')
    pkval = request.args.get('pkval')

    if action == 'delete' and pkval:
        e.deleteById(pkval)
        return render_template('ok_dialog.html', msg="Experiment deleted.")

    if action == 'insert':
        d = {
            'StartDate': request.form.get('StartDate'),
            'EndDate': request.form.get('EndDate'),
            'Description': request.form.get('Description'),
            'Creator_UserID': session['user']['UserID'],
            'CreatedTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        e.set(d)
        if e.verify_new():
            e.insert()
            experiment_id = e.data[0][e.pk]
            e.data[0]['ExperimentCode'] = e.generate_experiment_code(experiment_id)
            e.update()
            return render_template('ok_dialog.html', msg="Experiment added.")
        else:
            return render_template('experiments/add.html', obj=e)

    if action == 'update' and pkval:
        e.getById(pkval)
        if e.data:
            e.data[0].update({
                'ExperimentID': request.form.get('ExperimentID'),
                'StartDate': request.form.get('StartDate'),
                'EndDate': request.form.get('EndDate'),
                'Description': request.form.get('Description'),
                'UpdatedDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            if e.verify_update():
                e.update()
                return render_template('ok_dialog.html', msg="Experiment updated.")
            else:
                return render_template('experiments/manage.html', obj=e)
        else:
            return render_template('error_dialog.html', msg=f"Experiment with ID {pkval} was not found.")

    if pkval is None:
        e.getAll()
        return render_template('experiments/list.html', obj=e)
    elif pkval == 'new':
        e.createBlank()
        return render_template('experiments/add.html', obj=e)
    else:
        e.getById(pkval)
        if e.data:
            return render_template('experiments/manage.html', obj=e)
        else:
            return render_template('error_dialog.html', msg=f"Experiment with ID {pkval} was not found.")

@app.route('/survey')
def survey():
    code = request.args.get('code')
    if not code:
        return "Invalid survey link."

    e = experiments()
    e.getByField('ExperimentCode', code)
    if len(e.data) == 0:
        return "Experiment not found."

    return render_template('survey.html', experiment=e.data[0])

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

def checkSession():
    if 'active' in session:
        if time.time() - session['active'] > 500:
            session['msg'] = 'Your session has timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    return False

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
