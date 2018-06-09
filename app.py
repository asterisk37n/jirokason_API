#-*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII']=False

data = json.load(open('restaurants.json'))

@app.route('/restaurants')
def restaurants():
    lat = request.args.get('lat', default=None, type=float)
    lng = request.args.get('lng', default=None, type=float)
    data['center'] = {'lat': lat, 'lng': lng}
    if lat is None or lng is None:
        return jsonify(data)
    data['restaurants'] = sorted(
            data['restaurants'],
            key = lambda row: (lat - row['coordinate']['lat']) ** 2 + (lng - row['coordinate']['lng']) ** 2
            )
    return jsonify(data)

if __name__ == '__main__':
    app.run()
