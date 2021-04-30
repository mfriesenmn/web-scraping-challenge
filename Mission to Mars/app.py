from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html",
		title="Mars Scrape",
		newstitle = mars["NewsTitle1"],
		newsdesc = mars["NewsDesc"],
		hspage = mars["FeaturedURL"],
		hem1 = mars["Hemispheres"][0]["Image URL"],
		hem2 = mars["Hemispheres"][1]["Image URL"],
		hem3 = mars["Hemispheres"][2]["Image URL"],
		hem4 = mars["Hemispheres"][3]["Image URL"],
		hem1name = mars["Hemispheres"][0]["Title"],
		hem2name = mars["Hemispheres"][1]["Title"],
		hem3name = mars["Hemispheres"][2]["Title"],
		hem4name = mars["Hemispheres"][3]["Title"],
		)

@app.route("/scrape")
def nameless():
	mars = mongo.db.mars
	mars_data = scrape_mars.scrape()
	mars.update({}, mars_data, upsert=True)
	return redirect('/', code=302)


if __name__ == "__main__":
    app.run()