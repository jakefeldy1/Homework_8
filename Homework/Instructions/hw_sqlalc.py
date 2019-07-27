import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)


@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start_end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of last 12 months of prcp data"""
    # Query last 12 months of prcp data
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()
    
    all_prcp = []
    for date, prcp in precipitation:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)
    
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all stations
    active = session.query(Station.name).filter(Measurement.station==Station.station).\
    group_by(Station.name).all()
    
    all_station = []
    for station in active:
        station_dict = {}
        station_dict["station"] = station
        all_station.append(station_dict)

    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperatures over past year"""
    # Query all temperatures over past year
    temp = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()
    temp
    
    all_tobs = []
    for date, tobs in temp:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        all_tobs.append(temp_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_date(start):
    """start"""
    # Query with start date
    calculations = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    all_calcs = []
    for date, min, max, avg in calculations:
        calc_dict = {}
        calc_dict["date"] = date
        calc_dict["min"] = min
        calc_dict["avg"] = avg
        calc_dict["max"] = max
        all_calcs.append(calc_dict)

    return jsonify(all_calcs)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """start and end"""
    # Query with start and end dates

    end = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    all_dates = []
    for date, min, max, avg in end:
        dates_dict = {}
        dates_dict["date"] = date
        dates_dict["min"] = min
        dates_dict["avg"] = avg
        dates_dict["max"] = max
        all_dates.append(dates_dict)

    return jsonify(all_dates)

if __name__ == "__main__":
    app.run(debug=True)
