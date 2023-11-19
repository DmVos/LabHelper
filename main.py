import sqlite3
import os
import base64
from io import BytesIO
from datetime import datetime

from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

#from db_sqlite import connect_db

from DataBase import DataBase
from Model import define_corrosion
from DataBase import DataBase
from UserLogin import UserLogin
from Forms import LoginForm



#конфигурация
DATABASE = 'database.db'
DEBUG = True
SECRET_KEY = 'Test_user'
MAX_IMAGE_LENGTH = 1024 * 1024 

app = Flask(__name__)
app.config.from_object(__name__)
#app.config.update(dict(DATABASE=os.path.join(app.root_path, 'database.db')))
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    print("load User")
    return UserLogin().fromDB(user_id, dbase)

#Подключение к БД
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

#Подключение к БД внутри запроса
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        print('link_db=')
    return g.link_db

#Закрытие соединения с БД
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


#Создание соединения с БД
dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = DataBase (db)





#Обработка URL

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
        return redirect(url_for('profile'))
    
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
    return f"""<p><a href="{url_for('logout')}">Выйти из профиля</a>
                <p>user info {current_user.get_id()}"""


@app.route("/my_experiments/<username>")
def my_experiments(username):
    return render_template('my_experiments.html', title = "My experiments", menu = dbase.getMenuForUser())


@app.route("/all_experiments")
def all_experiments():
    return render_template('all_experiments.html', title = "All experiments", menu = dbase.getMenuForUser(), experiments = dbase.getAllExperiments())

@app.route("/add_experiment", methods=["POST","GET"])
@login_required
def addExperiment():
    if request.method == "POST":
        print(request.form['title'])
        if len(request.form['title']) > 1:
            file = request.files['file']
            img = file.read()
            exp = dbase.addExreriment(request.form['title'], request.form['start_date'], img)
            if not exp:
                flash('Ошибка сохранения')
            else:
                flash('Сохранение выполнено')
        else:
            flash('Не задан Title для эксперимента')
    return render_template('add_experiment.html', title = "Add Experiment", menu = dbase.getMenuForUser())

@app.route("/experiment/<int:id_exp>")
def showExperiment(id_exp):
    title, start_date_unix = dbase.getExperiment(id_exp)
    
    start_date = datetime.fromtimestamp(start_date_unix).strftime('%d-%m-%Y')
    image = dbase.loadImage(id_exp)
    image_response, corroded_area_meters , corroded_area_cm2 = define_corrosion(image)
 
    return render_template('experiment.html', menu = dbase.getMenuForUser(), title = title, start_date = start_date, corroded_area_meters = round(corroded_area_meters, 4), corroded_area_cm2 = round(corroded_area_cm2, 2), image_response = image_response)


#@app.route('/experiment_image/<int:id_exp>')
#@login_required
#def experiment_image(id_exp):
#    img = dbase.loadImage(id_exp)
#    if not img:
#        return ""
#    h = make_response(img)
#    h.headers['Content-Type'] = 'image/png'
#    return h


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page_404.html', title = "Page not found", menu = dbase.getMenuForUser()), 404







if __name__ == "__main__":
    app.run(debug=True)