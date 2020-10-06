from flask import Flask
from flask_restful import Resource, Api

from flight_finder import FlightFinder

app = Flask(__name__)
api = Api(app)

@app.route('/flights/<from_>/<to_>/<start_>/<end_>')
def find_flights(from_, to_, start_, end_):
    ff = FlightFinder(from_, to_, start_, end_)
    
    return ff.find_flights()

if __name__ == '__main__':
    app.run(debug=True)