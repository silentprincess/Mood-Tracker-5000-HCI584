from asyncio.base_futures import _format_callbacks
from operator import and_
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, RadioField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt #used to hash passwords
import datetime
from sqlalchemy import and_
from sqlalchemy import extract
from sqlalchemy.ext.hybrid import hybrid_property

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

login_manager = LoginManager() #allows app and flask to handle things while logging in
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader #reloads the user object from the user ID stored in session
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #creates unique ID for each row in table
    username = db.Column(db.String(20), nullable=False, unique=True) #username can only have 20 characters, field cannot be empty, cannot be 2 or more of the same username
    password = db.Column(db.String(80), nullable = False) #pass can only have 80 characters, field cannot be empty
    #moodIcon = db.Column("mood", db.Integer)
    #moodJournal = db.Column("journal", db.String(300))

    #def AddMood(moodChoice):
        #today = datetime.datetime.now()
        #moodIconToday = db.Column(db.Integer, nullable = False)
        #moodJournalToday = db.Column(db.String(300), nullable = False)


class RegisterForm(FlaskForm): #creates register form to be added to html pages
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

def validate_username(self, username):
    existing_user_username = User.query.filter_by(username=username.data).first() #queries database to check if there are duplicate usernames
    if existing_user_username: #if there's a duplicate username, gives validation error
        raise ValidationError("That username is taken. Please choose a different one.")

class LoginForm(FlaskForm): #creates login form to be added to html pages
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class MoodEntry(FlaskForm): #creates form for mood entry, gives multiple choices
    happy = SubmitField("Happy")
    sad = SubmitField("Sad")
    angry = SubmitField("Angry")
    meh = SubmitField("Meh")
    romantic = SubmitField("Romantic")
    stressed = SubmitField("Stressed")
    journal = TextAreaField("Submit journal entry here...")

#def moodAssignment(mood):
    #mood = 0
    #if mood == happy:
    #    mood = 1
    #elif mood == sad:
    #    mood = 2
    #elif mood == angry:
    #    mood = 3
    #elif mood == meh:
    #    mood = 4
    #elif mood == romantic:
    #    mood = 5
    #else:
    #    mood = 6
    #    return MoodEntry.query.get(mood)


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/moodentry", methods = ['GET', 'POST'])
def moodentry():
    form = MoodEntry()
    return render_template('moodentry.html', form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() #check if user is in db
        if user: #if user is registered
            if bcrypt.check_password_hash(user.password, form.password.data): #checks password, if everything matches up redirects to dashboard
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form = form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required #have to be logged in to log out
def logout():
    logout_user()
    return(redirect(url_for('login'))) #redirects to login page

@app.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard():
        return render_template('dashboard.html')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit(): #encrypting passwords for registration
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit() #commit new user to database
        return redirect(url_for('login'))

    return render_template('register.html', form = form)

if __name__ == '__main__':
    app.run(debug=True)