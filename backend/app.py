# Imports taken from https://docs.ckan.org/en/2.9/api/, the documentation for the
# CKAN API, used by Boston 311

from api_interact import find_issues
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/apt_report")
def report():
    address = "2 Hillside St Mission Hill MA 02120"
    reports = {
        'report2023': find_issues(address),
    }  
    rating = 4
    return render_template("SearchResult.html", address=address, reports=reports, rating=rating)