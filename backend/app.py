# Imports taken from https://docs.ckan.org/en/2.9/api/, the documentation for the
# CKAN API, used by Boston 311

from api_interact import find_issues_wrapper, address_to_latlong
from flask import Flask, render_template, request, url_for, flash, redirect, session, jsonify
import sys
import pyrebase

config = {
        'apiKey': "AIzaSyCmH1QKp1t4y_gsNJ-63_NbsRHGlWuxGy0",
        'authDomain': "apartments-8578b.firebaseapp.com",
        'projectId': "apartments-8578b",
        'storageBucket': "apartments-8578b.appspot.com",
        'messagingSenderId': "412201567680",
        'appId': "1:412201567680:web:f53080566635a954187425",
        'measurementId': "G-VR2EDWMR3X",
        'databaseURL':'https://apartments-8578b-default-rtdb.firebaseio.com/'
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c5089374a4f1b370064f8f337e7e89650b9347932d13e004'

@app.route('/', methods = ['GET', 'POST'])
def index():
    if('user' in session):
        return redirect('/home')
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
    
        try: 
            user = auth.sign_in_with_email_and_password(email,password)
            session['user'] = username
            return redirect('/home')
        except:
            return "Failed to login"
    return render_template('Login.html')



@app.route('/signup', methods = ['GET' ,'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        username = request.form.get('username')

        # try: 
        user = auth.create_user_with_email_and_password(email,password)
        session['user'] = username
        # if user != None:
        #     for user in all_users.each():
        #         if user.key() == username:
        #             return "Username already taken. Try again."

        data = {'name': name, 'apts':[]}
        db.child("users").child(username).set(data)
        return redirect('/profile')
        # except:
        #     return "Sign up unsuccessful. Please try again."
    return render_template('Signup.html')



@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')



@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        address = request.form['address']
        if address_to_latlong(address) == -1:
            print('Failed!', file=sys.stderr)
            flash("Please enter a valid Boston address")
        else:
            return redirect(url_for('report', address=address))
    return render_template("Home.html")



@app.route("/report/<address>", methods=['GET', 'POST'])
def report(address):
    reports = find_issues_wrapper(address)
    rating = 0
  
    rating =( 5*reports['report2023']['rating'] + 4*reports['report2022']['rating'] + 3*reports['report2021']['rating'] +
             2*reports['report2020']['rating'] +reports['report2019']['rating']) / 15
    
    if rating < 0:
        rating = 0
    rating = round(rating,1)
    return render_template("SearchResult.html", address=address, reports=reports, rating=rating)



@app.route("/profile")
def profile():
    username = session['user']
    info =(db.child("users").child(username).child("name").get())
    name = info.val()


    apartments = [{'address': "2 Hillside St",
         'lon' : -71.0991603,
         'lat': 42.3290705,
         'rating': 4}]
    
    return render_template("Profile.html", name = name, apartments=apartments)