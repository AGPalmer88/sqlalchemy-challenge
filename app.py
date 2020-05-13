import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        f"<br/>"
        f"Let's Plan a Trip! Here are the Available Routes:<br/>"
        f"<br/>"
        f"<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations Data: /api/v1.0/stations<br/>"
        f"The Dates & Temperature Observations: /api/v1.0/tobs<br/>"
        f"List of Min, Avg, & Max Temperature for a given start date: /api/v1.0/2016-05-05<br/>"
        f"List of Min, Avg, & Max Temperature for a given start and end date: /api/v1.0/2016-05-05/2016-05-11<br/>"
    )

#####################################################################



@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results to a dictionary using `date` as the key and `prcp` as the value"""
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    last_12_mnth_prcp = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= last_year_date).order_by(measurement.date).all()
    
    
    #Return the JSON representation of your dictionary.
    precipitation = {date: prcp for date, prcp in last_12_mnth_prcp}    
    return jsonify(precipitation)

    session.close()

#####################################################################
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    
    results = session.query(station.name, measurement.station).\
    filter(station.station == measurement.station).\
    group_by(station.station).all()
    
    
    all_stations = list(np.ravel(results))
    
    return jsonify(all_stations)
    
    session.close()
    
#####################################################################
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
        
    return jsonify(list_TempObs)
    
    session.close()

#####################################################################

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ Return `TMIN`, `TAVG`, and `TMAX` for start only, for all dates greater than and equal to the start date."""
    
    temp_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start).all()
    
    temps = list(np.ravel(temp_data))
    
    session.close()
    
    return jsonify(temps)

    return jsonify({"error": "Please try another date range."}), 404

#####################################################################    
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)
    
    temp_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start).filter(measurement.date <= end).all()
        
    temps = list(np.ravel(temp_data))
    
    session.close()
    
    return jsonify(temps)
    
    return jsonify({"error": "Please try another date range."}), 404

    
if __name__ == "__main__":
    app.run(debug=True)