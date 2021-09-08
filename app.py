import numpy as np
import pymongo

from flask import Flask, jsonify, render_template

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.MarsDB
db.info.drop()

app = Flask(__name__)

@app.route('/scrape')
def scrape():
    from scrape_mars import scrape
    data = scrape()
    
    return data

@app.route('/')
def home():
    from scrape_mars import scrape
    data = scrape()
    
    db.info.insert_one(data)
    out = list(db.info.find())
    print(out)

    # Return the template with the teams list passed in
    return render_template('index.html', out=out)


if __name__ == '__main__':
    app.run(debug=True)