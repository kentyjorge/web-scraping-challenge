from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_mission_app"
mongo = PyMongo(app)
db = mongo.db

@app.route("/")
def index():
    db_data = db.mars_mission.find_one()
    #m_data = mars_mission.find()
    return render_template('index.html', m_data=db_data)

@app.route("/scrape")
def scrape():
    print("starting the scrape")
    # Run the scrape function
    mars_mission = db.mars_mission
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_mission.update({}, mars_data, upsert=True)
    print("finished, redirecting user")
    # Redirect back to home page
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)