from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_mission_app")
mars_mission_db = mongo.db.mars_mission

@app.route("/")
def index():
    m_data = mars_mission_db.find_one()
    return render_template("index.html", mars=m_data)

@app.route("/scrape")
def scrape():
    print("starting the scrape")
    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update_one({}, {"$set": mars_data}, upsert=True)
    print("finished, redirecting user")
    # Redirect back to home page
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)