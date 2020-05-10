###########################################
# imports dependencies
###########################################
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """ List all routes that are available. """
    return (
        f"Welcome to Hawaii Climate Climate Analysis!<br/>"
        f"Let's Plan a Trip! Here are the Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results to a dictionary using `date` as the key and `prcp` as the value"""
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    last_12_mnth_prcp = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= last_year_date).order_by(measurement.date.desc()).all()
    
    
    #Return the JSON representation of your dictionary.
    precipitation = {date: prcp for date, prcp in last_12_mnth_prcp}    
    return jsonify(precipitation)

    session.close()


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    
    results = session.query(station.station, station.name, station.latitude, station.latitude, station.longitude, station.elevation).\
    group_by(station.station).all()
    
    
    all_stations = list(np.ravel(results))
    
    return jsonify(all_stations)
    
    session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ Query the dates and temperature observations of the most active station for the last year of data."""
    results = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >= "2016=08-23").\
    filter(measurement.date <= "2017-08-23").\
    filter(measurement.station == "USC00519281").all()

  
  # Return a JSON list of temperature observations (TOBS) for the previous year.
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    tobs_list = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date>= last_year_date).all()
    
    list_TempObs = list(np.ravel(results)) 
    
    session.close()
    
    return jsonify(list_TempObs)

#@app.route("api/v1.0/<start>")
#@app.route("/api/v1.0/<start>/<end>`")

if __name__ == "__main__":
    app.run(debug=True)
