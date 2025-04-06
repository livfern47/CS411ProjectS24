# Imports taken from https://docs.ckan.org/en/2.9/api/, the documentation for the
# CKAN API, used by Boston 311

from api_interact import find_issues_wrapper, address_to_latlong
from flask import Flask, render_template, request, url_for, flash, redirect, session, jsonify
import sys
import pyrebase

# Read secret information from ignored file
keys = open("key.txt")

# FIREBASE SETUP
config = {
        'apiKey': keys.readline(),
        'authDomain': keys.readline(),
        'projectId': keys.readline(),
        'storageBucket':  keys.readline(),
        'messagingSenderId':  keys.readline(),
        'appId':  keys.readline(),
        'measurementId':  keys.readline(),
        'databaseURL': keys.readline(),
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# APP SETUP 
app = Flask(__name__)
app.config['SECRET_KEY'] = keys.readline()
keys.close()

# SIGN IN
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



# SIGN UP
@app.route('/signup', methods = ['GET' ,'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        username = request.form.get('username')


        user = auth.create_user_with_email_and_password(email,password)
        session['user'] = username


        data = {'name': name, 'apts':[(0,0)]}
        db.child("users").child(username).set(data)
        return redirect('/profile')

    return render_template('Signup.html')


# LOG OUT
@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')


# ADDRESS INPUT
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


# GENERATE REPORT FOR ADDRESS
@app.route("/report/<address>", methods=['GET', 'POST'])
def report(address):
    reports = find_issues_wrapper(address)
    rating = 0
  
    rating =( 5*reports['report2023']['rating'] + 4*reports['report2022']['rating'] + 3*reports['report2021']['rating'] +
             2*reports['report2020']['rating'] +reports['report2019']['rating']) / 15
    
    if rating < 0:
        rating = 0
    rating = round(rating,1)


    latlon = address_to_latlong(address)
    apt_info = {'address': address,
         'lon' :latlon['long'],
         'lat': latlon['lat'],
         'rating': rating}
    username=session['user']
    apts = db.child("users").child(username).child("apts").get()
    apts_lst = apts.val()
    apts_lst = apts_lst= apts_lst + [apt_info]
    db.child("users").child(username).update({'apts' : apts_lst})

    return render_template("SearchResult.html", address=address, reports=reports, rating=rating)


# SHOW PROFILE
@app.route("/profile")
def profile():
    username = session['user']
    info =(db.child("users").child(username).child("name").get())
    name = info.val()


    apartments = db.child("users").child(username).child("apts").get()
    apartments = apartments.val() 

    return render_template("Profile.html", name = name, apartments=apartments)