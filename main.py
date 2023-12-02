import sqlite3
from datetime import datetime
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
from io import BytesIO


from DataBase import DataBase
from Model import define_corrosion
from Classification import image_classification
from DataBase import DataBase
from UserLogin import UserLogin
from Forms import LoginForm



# Main config
DATABASE = 'database.db'
DEBUG = True
SECRET_KEY = 'Test_user'
MAX_IMAGE_LENGTH = 1024 * 1024 

app = Flask(__name__)
app.config.from_object(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    print("load User")
    return UserLogin().fromDB(user_id, dbase)

# Connect to DB
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# Connect to DB (in request)
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        print('link_db=')
    return g.link_db

# Close connection to DB
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


# Connect to DB
dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = DataBase (db)




# URL actions
@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        return render_template('index.html', title = "Home", menu = dbase.getMenuForUser())
    else:
        return render_template('index.html', title = "Home", menu = dbase.getMenu())


@app.route("/login", methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('my_experiments'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.getUserByLogin(form.login.data)
        if user and check_password_hash(user['password'], form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(url_for('index'))
    return render_template('login.html', title="Sign in", menu=dbase.getMenu(), form=form)


@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        if len(request.form['username']) > 0 and len(request.form['userlogin']) > 0 \
        and len(request.form['psw1']) > 0 and request.form['psw1'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw1'])
            res = dbase.addUser(request.form['username'], request.form['userlogin'], hash)
            if res:
                flash('You have successfully signed up!')
                return redirect(url_for('login'))
            else:
                flash('There was an error during sign up. Please try again later.')
        else:
            flash ('The fields are filled in incorrectly. Please review and correct values in fields.')    
    return render_template('register.html', title = "Sign up", menu = dbase.getMenu())


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('index.html', title = "Номе", menu = dbase.getMenu())


@app.route("/profile")
@login_required
def profile():
    return f"""<p><a href="{url_for('logout')}">Logout</a>
                <p>user info {current_user.get_id()}"""


@app.route("/my_experiments")
def my_experiments():
    user={current_user.get_id()}
    formatted_experiments = []
    if isinstance(user, set) and len(user) == 1:
        user = next(iter(user))
    experiments = dbase.getUserExperiments(user)
    # Convert start_data to '%d-%m-%Y'
    for exp in experiments:
        exp_dict = dict(exp)
        exp_dict['start_date'] = datetime.fromtimestamp(exp_dict['start_date']).strftime('%d-%m-%Y')
        formatted_experiments.append(exp_dict)
    return render_template('my_experiments.html', title = "My experiments", menu = dbase.getMenuForUser(), experiments=formatted_experiments)


@app.route("/all_experiments")
def all_experiments():
    experiments = dbase.getAllExperiments()
    formatted_experiments = []
    
    # Convert start_data to '%d-%m-%Y'
    for exp in experiments:
        exp_dict = dict(exp)
        exp_dict['start_date'] = datetime.fromtimestamp(exp_dict['start_date']).strftime('%d-%m-%Y')
        formatted_experiments.append(exp_dict)
    return render_template('all_experiments.html', title = "All experiments", menu = dbase.getMenuForUser(), experiments = formatted_experiments)


@app.route("/add_experiment", methods=["POST","GET"])
@login_required
def addExperiment():
    if request.method == "POST":
        print(request.form['title'])
        if len(request.form['title']) > 1:
            if 'file' not in request.files:
                flash('No file part', 'error')
                return render_template('add_experiment.html', title="Add Experiment", menu=dbase.getMenuForUser())
            
            # read file 
            file = request.files['file']
            if file.filename == '':
                flash('No selected file', 'error')
                return render_template('add_experiment.html', title="Add Experiment", menu=dbase.getMenuForUser())

            img = file.read()
            try:
                img = Image.open(file)
                if img.width != img.height:
                    flash('The image must be square', 'error')
                    return render_template('add_experiment.html', title="Add Experiment", menu=dbase.getMenuForUser())

                img = img.resize((512, 512), Image.ANTIALIAS)
                
                # Conversion back to binary data
                img_byte_arr = BytesIO()
                img.save(img_byte_arr, format='PNG')
                img = img_byte_arr.getvalue()
            except IOError:
                flash('Can\'t resize image.', 'error')
                return render_template('add_experiment.html', title="Add Experiment", menu=dbase.getMenuForUser())

            # define user
            user = {current_user.get_id()}
            if isinstance(user, set) and len(user) == 1:
                user = next(iter(user))

            # convert time
            start_data = request.form['start_date']
            date_object = datetime.strptime(start_data, '%Y-%m-%d')
            unix_timestamp = int(date_object.timestamp())
            
            exp = dbase.addExreriment(request.form['title'], unix_timestamp, user, img, request.form['sample_size_h'], request.form['sample_size_w'], request.form['comment'])
            if not exp:
                flash('Save error', "error")
            else:
                flash('Experiment saved', "success")
        else:
            flash('Title is undefined', "error")
    return render_template('add_experiment.html', title = "Add Experiment", menu = dbase.getMenuForUser())


@app.route("/experiment/<int:id_exp>")
def showExperiment(id_exp):
    title, start_date_unix, sample_size_h, sample_size_w, comment = dbase.getExperiment(id_exp) 
    
    start_date = datetime.fromtimestamp(start_date_unix).strftime('%d-%m-%Y')
    image = dbase.loadImage(id_exp)
    image_response, corroded_area_meters , corroded_area_cm2 = define_corrosion(image, sample_size_h, sample_size_w)
    image_class = image_classification(image)
    return render_template('experiment.html', menu = dbase.getMenuForUser(), title = title, start_date = start_date, 
                           corroded_area_meters = round(corroded_area_meters, 4), corroded_area_cm2 = round(corroded_area_cm2, 2), 
                           image_response = image_response, image_class = image_class, sample_size_h = sample_size_h, 
                           sample_size_w = sample_size_w, comment = comment)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page_404.html', title = "Page not found", menu = dbase.getMenuForUser()), 404


# Starting app
if __name__ == "__main__":
    app.run(debug=True)