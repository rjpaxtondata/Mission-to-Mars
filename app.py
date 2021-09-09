from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/MarsDB"
mongo = PyMongo(app)



#route to render index.html template using data from Mongo
@app.route('/')
def home():
    
    #find one record of data from the mongo database
    out = mongo.db.mars.find_one()
    # Return the template with the teams list passed in
    #mars goes into the HTML code
    return render_template('index.html', mars=out)

#Route that will trigger the scrape function
@app.route('/scrape')
def scrape():
    #run the scrape function
    mars = mongo.db.mars
    mars_df = scrape_mars.scrape()
    
    #update the mongo database useing the updte and upsert=True
    mars.update({}, mars_df, upsert=True)
    
    return redirect('/', code=302)
        

if __name__ == '__main__':
    app.run(debug=True)




