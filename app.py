#-*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII']=False

restaurants_data = json.load(open('restaurants.json'))

@app.route('/restaurants')
def top():
    searchword = request.args.get('key', '')
    lat = request.args.get('lat', None)
    lng = request.args.get('lng', None)

    return jsonify(restaurants_data)

if __name__ == '__main__':
    app.run()
