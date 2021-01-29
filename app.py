from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import pandas as pd
import datetime as dt


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
base = automap_base()
base.prepare(engine, reflect=True)
base.classes.keys()
measurement = base.classes.measurement
station = base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return (f"Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/station<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/(start)<br/>"
            f"/api/v1.0/(start)-(end)<br/>")

@app.route("/api/v1.0/precipitation")
def rain():
    session = Session(engine)

    lastDate = session.query(measurement.date).order_by(measurement.date.desc()).first()
    lastDateFormat = dt.datetime.strptime(lastDate[0], "%Y-%m-%d")
    lastYearDate = lastDateFormat - dt.timedelta(days=365)
    lastYearDateFormat = lastYearDate.strftime("%Y-%m-%d")
    rainData = session.query(measurement.date, measurement.prcp).filter(measurement.date > lastYearDateFormat).all()

    session.close()

    rainList = []
    for date, prcp in rainData:
        rainDict = {}
        rainDict['date'] = date
        rainDict['prcp'] = prcp
        rainList.append(rainDict)

    return jsonify(rainList)

if __name__ == "__main__":
    app.run(debug=True)