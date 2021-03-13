import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/Enter start date in YYYY-MM-DD<br/>"
        f"/api/v1.0/Enter start date in YYYY-MM-DD/Enter end date in YYYY-MM-DD</<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all prcp names"""
    # Query all prcp
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_precipitation = []

# Create a dictionary from the row data and append to a list of precipitation
    for date,prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations data"""
    # Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Convert list to normal list
    all_sessions = list(np.ravel(results))
    
    return jsonify(all_sessions)


@app.route("/api/v1.0/tobs")
def tobs():
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations data"""
    # Query all tobs
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >=year_ago).\
        filter(Measurement.station =="USC00519281").all()

    session.close()

    all_tobs = []

    for date,tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(all_tobs)
    
    return jsonify(all_tobs)

#  When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def search_date (start):

    session = Session(engine)

    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    start_date_results = []
    for min, max, avg in results:
        start_date_results_dict = {}
        start_date_results_dict["min_temp"] = min
        start_date_results_dict["max_temp"] = max
        start_date_results_dict["avg_temp"] = avg
        start_date_results.append(start_date_results_dict)

    return jsonify(start_date_results)


# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_end_dates (start,end):

    session = Session(engine)

    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    start_end_date_results = []
    for min, max, avg in results:
        start_end_date_dict = {}
        start_end_date_dict["min_temp"] = min
        start_end_date_dict["max_temp"] = max
        start_end_date_dict["avg_temp"] = avg
        start_end_date_results.append(start_end_date_dict)

    return jsonify(start_end_date_results)


if __name__ == '__main__':
    app.run(debug=True)
