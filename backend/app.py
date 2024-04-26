# Imports taken from https://docs.ckan.org/en/2.9/api/, the documentation for the
# CKAN API, used by Boston 311

from api_interact import find_issues_wrapper, address_to_latlong
from flask import Flask, render_template, request, url_for, flash, redirect
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c5089374a4f1b370064f8f337e7e89650b9347932d13e004'

@app.route("/", methods=['GET', 'POST'])
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
  
    rating =( reports['report2023']['rating'] + reports['report2022']['rating'] + reports['report2021']['rating'] +
             reports['report2020']['rating'] +reports['report2019']['rating']) / 5
    
    rating = round(rating,1)
    return render_template("SearchResult.html", address=address, reports=reports, rating=rating)

@app.route("/profile")
def profile():
    name = "Oliver"
    apartments = [{'address': "2 Hillside St",
         'lon' : -71.0991603,
         'lat': 42.3290705,
         'rating': 4}]
    
    return render_template("Profile.html", name = name, apartments=apartments)