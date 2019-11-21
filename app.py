# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 20:59:23 2019

@author: J. Carroll
"""

# Dependencies and Setup
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri = "mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database  
    mars_data = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars = mongo.db.mars

    # Run the scrape function
    mars_data = scrape_mars.scrape_all()
    
    # Update the Mongo database using update and upsert=True
    mars.update({}, mars_data, upsert=True)
    
    # Redirect back to home page
    return redirect('/', code=302)

# Define Main Behavior
if __name__ == "__main__":
    app.run(debug=True)