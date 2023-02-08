import numpy as np

import datetime as dt
from dateutil.relativedelta import relativedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

station = Base.classes.station
measurement = Base.classes.measurement

app = Flask(__name__)

@app.route("/")
def home():

    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():

    session = Session(engine)

    query_date = dt.date(2017, 8, 23) - relativedelta(years=1)

    date_prcp = session.query(measurement.date, measurement.prcp).filter(measurement.date >= query_date).order_by(measurement.date).all()

    session.close()

    prcp_dict = {}
    for date, prcp in date_prcp:
        prcp_dict[date] = prcp

    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    results = session.query(station.name).all()

    session.close()

    station_names = list(np.ravel(results))

    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    query_date = dt.date(2017, 8, 23) - relativedelta(years=1)

    results = session.query(measurement.date, measurement.tobs).filter(measurement.date >= query_date)\
              .filter(measurement.station=='USC00519281').all()

    session.close()

    tobs_data = list(np.ravel(results))

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def start_date(start):

    session = Session(engine)

    tmin = session.query(func.min(measurement.tobs)).filter(measurement.date >= start).all()

    tavg = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start).all()

    tmax = session.query(func.max(measurement.tobs)).filter(measurement.date >= start).all()

    session.close()

    temps = list(np.ravel(tmin))
    temps.extend(np.ravel(tavg))
    temps.extend(np.ravel(tmax))

    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def start_date_end_date(start, end):

    session = Session(engine)

    tmin = session.query(func.min(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()

    tavg = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()

    tmax = session.query(func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()

    session.close()

    temps = list(np.ravel(tmin))
    temps.extend(np.ravel(tavg))
    temps.extend(np.ravel(tmax))

    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)