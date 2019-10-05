# ----------------------------------------------------------------------
# Step 1: Import all necessary modules and create Flask app
# ---------------------------------------------------------------------- 
from flask import Flask, jsonify
import pandas as pd
import datetime as dt

# create app
app = Flask(__name__)

# ----------------------------------------------------------------------
# Step 2: Set up db connection and session
# ----------------------------------------------------------------------
# set up sqlalchemy engine
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///C:\\Users\\Drew's Surface\\Documents\\COLNYC20190716DATA\\02-Homeworks\\10-Advanced-Data-Storage-and-Retrieval\\Instructions\\hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# map classes
print (Base.classes.keys())
Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)

# ----------------------------------------------------------------------
# Step 3: Create all required routes
# ---------------------------------------------------------------------- 
@app.route("/")
def welcome():
    return (
        f"Welcome to the Weather App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>" 
        f"/api/v1.0/start and end<br/>"
        )


@app.route('/api/v1.0/precipitation')
def precipitation():
    last_year_start = (dt.date(2017,8,23) - dt.timedelta(days=365)).isoformat()
    query = (f'SELECT date, prcp FROM measurement \
                WHERE date > "{last_year_start}"')
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'))

@app.route('/api/v1.0/station')
def station():
    query = 'SELECT station, name FROM station'
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'))

@app.route('/api/v1.0/tobs')
def normal():
    sel = [Measurement.station, Measurement.id, Measurement.tobs]
    date = dt.datetime(2017, 8, 24)
    date2 = dt.datetime(2016, 8, 22)
    station4 = session.query(*sel).\
        filter(Measurement.station =="USC00519281").\
        filter(Measurement.date <= date).\
        filter(Measurement.date >= date2).\
        order_by(Measurement.date).all()
    station4
    return jsonify(station4)


@app.route('/api/v1.0/start/')
def temps_startOnly(start):
    query = (f'SELECT AVG(temp) AS "Average Temperature", MIN(temp) \
                AS "Minimum Temperature", MAX(temp) AS "Maximum Temperature" \
                FROM  WHERE date >= "{start}"')
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'))


@app.route('/api/v1.0/start and end/{start}{end}')
def temps_startAndEnd(start, end):
    query = (f'SELECT AVG(temp) AS "Average Temperature", MIN(temp) \
                AS "Minimum Temperature", MAX(temp) AS "Maximum Temperature" \
                FROM  WHERE date >= "{start}" AND date <= "{end}"')
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'))  

# ----------------------------------------------------------------------
# Step 4: Define main
# ---------------------------------------------------------------------- 
if __name__ == "__main__":
    app.run(debug=True)