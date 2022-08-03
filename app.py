## Ponder
## Sarah Hernandez
## HCI 584
## Summer 2022
##CHECK DEV GUIDE FOR PACKAGES TO INSTALL##

from asyncio.base_futures import _format_callbacks
from operator import and_
from smtplib import SMTPRecipientsRefused
from statistics import median_high
from flask import Flask, render_template, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, RadioField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt #used to hash passwords
import datetime
from sqlalchemy import and_
from sqlalchemy import extract
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import insert
import pandas as pd

## SETS UP FLASK APPLICATION ##
app = Flask(__name__) #creates app
db = SQLAlchemy(app) #creates user database for app
bcrypt = Bcrypt(app) #creates encryption for app info
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
login_manager = LoginManager() #allows app and flask to handle things while logging in
login_manager.init_app(app)
login_manager.login_view = "login"


## CREATES LOGIN MANAGER ##
@login_manager.user_loader #reloads the user object from the user ID stored in session
def load_user(user_id):
    return User.query.get(int(user_id))
    
## CREATES USER CLASS FOR DB##
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #creates unique ID for each row in table
    email = db.Column(db.String(50), nullable = False, unique=True) #email can have max of 20 characters, field cannot be empty, cannot be 2 or more of the same email
    username = db.Column(db.String(20), nullable=False, unique=True) #username can only have 20 characters, field cannot be empty, cannot be 2 or more of the same username
    password = db.Column(db.String(80), nullable = False) #pass can only have 80 characters, field cannot be empty
    moods = db.relationship('Mood', backref='User', lazy = True) #creating link between user and mood table (I think)

##CREATES MOOD CLASS FOR DB ##
class Mood(db.Model): #creating mood table
    date = db.Column(db.Date, db.ForeignKey('user.id'), nullable = False, primary_key=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False, primary_key=True)
    happy = db.Column(db.Integer) #creates column for happy mood choice
    sad = db.Column(db.Integer) #creates column for sad mood choice
    angry = db.Column(db.Integer) #creates column for angry mood choice
    meh = db.Column(db.Integer) #creates column for meh mood choice
    romantic = db.Column(db.Integer) #creates column for romantic mood choice
    stressed = db.Column(db.Integer) #creates column for stressed mood choice
    journal = db.Column(db.String(1000)) #creates column for journal entries


## CREATES REGISTRATION FORM ##
class RegisterForm(FlaskForm): #creates register form to be added to html pages
    email = StringField(validators=[InputRequired(), Email(message='Invalid email, please try again.'), Length (min=3, max=30)], render_kw={"placeholder": "Email"})
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")


## VALIDATES USERNAME FOR REGISTRATION ##
def validate_username(self, username): #
    existing_user_username = User.query.filter_by(username=username.data).first() #queries database to check if there are duplicate usernames
    if existing_user_username: #if there's a duplicate username, gives validation error
        raise ValidationError("That username is taken. Please choose a different one.")


## VALIDATES EMAIL FOR REGISTRATION ##
def validate_email(self, email):
    existing_user_email = User.query.filter_by(email=email.data).first()
    if existing_user_email:
        raise ValidationError("That email has already been used, choose a different one.")


## CREATES LOGIN FORM ##
class LoginForm(FlaskForm): #creates login form to be added to html pages
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


## CREATES MOOD ENTRY FORM ##
class MoodEntry(FlaskForm): #creates form for mood entry, gives multiple choices
    happy = SubmitField("Happy")
    sad = SubmitField("Sad")
    angry = SubmitField("Angry")
    meh = SubmitField("Meh")
    romantic = SubmitField("Romantic")
    stressed = SubmitField("Stressed")
    journal = TextAreaField(validators = [InputRequired(), Length(min=4, max=1000)], render_kw={"placeholder": "Type your journal entry here..."})

## CREATES HOME PAGE ##
@app.route("/")
def home():
    return render_template('home.html')

## CREATES MOOD ENTRY PAGE, CREATES USER CSV DB ##
@app.route("/moodentry", methods = ['GET', 'POST']) #creates mood entry page
@login_required #must log in to access
def moodentry():
    form = MoodEntry()
    if form.validate_on_submit():
        if form.happy.data:
            mood = 1  
        elif form.sad.data:
            mood = 2
        elif form.angry.data:
            mood = 3
        elif form.meh.data:
            mood = 4
        elif form.romantic.data:
            mood = 5
        elif form.stressed.data: 
            mood = 6
        print("You have selected", mood)
        if form.validate_on_submit:
            if form.journal.data:
                journal = form.journal.data
            print("Here is your journal entry:", journal)

            #add new row to csv file
            csv_name = session["user"] + ".csv"
            try:
                df = pd.read_csv(csv_name)
            except Exception as e: 
                print("Error opening", csv_name, e)
            else:
                tstamp = pd.Timestamp.now().round(freq='T')
                max_index = len(df)
                df.loc[max_index+1] = [tstamp, mood, journal]
                df.to_csv(csv_name, index = False)
                return redirect(url_for('thankyou')) #redirects to dashboard (only 1 entry per day)

    return render_template('moodentry.html', form = form)


## CREATES LOGIN PAGE ##
@app.route("/login", methods = ['GET', 'POST']) #creates login page with loginform
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() #check if user is in db
        if user: #if user is registered
            if bcrypt.check_password_hash(user.password, form.password.data): #checks password, if everything matches up redirects to dashboard
                login_user(user)


                session["user"]= user.username
                return redirect(url_for('dashboard'))
            else:
                print("Wrong username or password!")
    return render_template('login.html', form = form)

##CREATES LOGOUT PAGE ##
@app.route('/logout', methods=['GET', 'POST']) #creates logout page
@login_required #have to be logged in to log out
def logout():
    logout_user()
    return(redirect(url_for('login'))) #redirects to login page

## CREATES USER DASHBOARD PAGE ##
@app.route('/dashboard', methods = ['GET', 'POST']) #creates User Dash
@login_required
def dashboard():
    return render_template('dashboard.html')

## CREATES REGISTRATION PAGE ##
@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit(): #encrypting passwords for registration
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, username=form.username.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit() #commit new user to database


        username=form.username.data

        df = pd.DataFrame({'Date': pd.Series(dtype='datetime64[ns]'), 
                           'Mood': pd.Series(dtype='int'),
                           'Journal': pd.Series(dtype='str')
                           })
       
        import csv
        df.to_csv(username + ".csv", index=False, quoting=csv.QUOTE_NONE)


        return redirect(url_for('login'))

    return render_template('register.html', form = form)

## CREATES THANK YOU PAGE AFTER MOOD ENTRY ##
@app.route('/thankyou', methods = ['GET', 'POST']) 
@login_required
def thankyou():
    return render_template('thankyou.html')

## CREATES PREVIOUS ENTRY PAGE ##
@app.route('/previousentries', methods = ['GET', 'POST']) 
@login_required
def previousentries():
    df = session["user"] + ".csv"
    rdf = pd.read_csv(df)
    print(rdf)
    with open(df) as file:
        return render_template('previousentries.html', csv=file)

if __name__ == '__main__':
    app.run(debug=True)