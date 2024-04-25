# Imports taken from https://docs.ckan.org/en/2.9/api/, the documentation for the
# CKAN API, used by Boston 311

from api_interact import find_issues
from flask import Flask, render_template, request, redirect, url_for, flash
import pyrebase

firebaseConfig = {
        'apiKey': "AIzaSyCmH1QKp1t4ygsNJ-63NbsRHGlWuxGy0",
        'authDomain': "apartments-8578b.firebaseapp.com",
        'projectId': "apartments-8578b",
        'storageBucket': "apartments-8578b.appspot.com",
        'messagingSenderId': "412201567680",
        'appId': "1:412201567680:web:f53080566635a954187425",
        'measurementId': "G-VR2EDWMR3X"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
app = Flask(__name__)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            flash("Successfully signed in", 'success')
            return redirect(url_for('Profile'))
        except:
            flash("Invalid email or password", 'error')
            return redirect(url_for('Profile'))
    return render_template("Profile.html")    

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            flash("Successfully signed up", 'success')
            return redirect(url_for('Profile'))
        except:
            flash("Email already exists", 'error')
            return redirect(url_for('Profile'))
    return render_template("Profile.html")

'''
ans = input("Do you have an account? (y/n): ")
if ans == 'y':
    login()
else:
    signup()
'''

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("Home.html")

@app.route("/apt_report")
def report():
    address = "2 Hillside St Mission Hill MA 02120"
    reports = {
        'report2023': find_issues(address),
    }  
    rating = reports['report2023']['rating']
    return render_template("SearchResult.html", address=address, reports=reports, rating=rating)

@app.route("/profile", methods=['GET'])
def profile():
    name = "Oliver"
    apartments = [{'address': "2 Hillside St",
         'lon' : -71.0991603,
         'lat': 42.3290705,
         'rating': 4}]
    
    return render_template("Profile.html", name = name, apartments=apartments)