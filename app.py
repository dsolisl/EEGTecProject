import numpy as np
import datetime as dt
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float 
from flask import Flask, jsonify, render_template
from config import mysql_pass

from numpy import *
from scipy.signal import *
from numpy.fft import *
from matplotlib import *
from scipy import *
from pylab import *
import json

# Allow us to declare column types
# PyMySQL 
import pymysql
pymysql.install_as_MySQLdb()

#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///hawaii.sqlite")
Base = declarative_base()
engine = create_engine("mysql://root:"+mysql_pass+"@localhost/SignalData")
Base.metadata.create_all(engine)

session = Session(bind=engine)
#conn = engine.connect()

# Create the Garbage class
class SignalData(Base):
    __tablename__ = 'Data'
    id = Column(Integer, primary_key=True)
    channel_1 = Column(Float)
    channel_2 = Column(Float)
    channel_3 = Column(Float)
    channel_4 = Column(Float)
    Time = Column(String)
    TimeStamp = Column(String)


# reflect an existing database into a new model
#Base = automap_base()
# reflect the tables
#Base.prepare(engine, reflect=True)

# Save reference to the tables
#
#av = Base.classes.Data


# Create our session (link) from Python to the DB
#session = Session(engine)

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
        f"/api/v1.0/data<br/>"
        f"/api/v1.0/channel_<i>n</i><br/>"
    )


@app.route("/eeg")
def eeg():
    """List all available api routes."""
    return render_template("eeg.html")    

@app.route("/fourier")
def fourier():
    """List all available api routes."""
    return render_template("fourier.html")    


@app.route("/api/v1.0/data")
def data():
    """Return a list of all measurements"""
    # Query all dates
    #session.merge()
    #session = Session(engine)
    #session.query(Garbage).filter(Garbage.id == 3).delete()
    results = session.query(SignalData.channel_1, SignalData.channel_2, SignalData.channel_3, SignalData.channel_4, SignalData.Time, SignalData.TimeStamp).all()
    all_results = []

    for result in results:
        result_dict = {}
        result_dict['Channel_1'] = result[0]
        result_dict['Channel_2'] = result[1]        
        result_dict['Channel_3'] = result[2]
        result_dict['Channel_4'] = result[3]
        result_dict['Time'] = result[4]
        result_dict['TimeStamp'] = result[5]
        all_results.append(result_dict)

    session.close()
    return jsonify(all_results)

@app.route("/api/v1.0/<channel>")
def channel(channel):
    """Return a list of all measurements"""
    # Query all dates
    #session.merge()
    #session = Session(engine)
    #session.query(Garbage).filter(Garbage.id == 3).delete()
    #str_channel = channel
    #ab = engine.execute("SELECT"+channel+", Time, TimeStamp FROM data").fetchall()

    results = engine.execute("SELECT "+channel+" FROM data").fetchall()
    all_results = []

    for result in results:
        #result_dict = {}
        #result_dict['measure'] =result[0]
        all_results.append(result[0])

    output_to_js = []
    freq_element = {}
    list_names = ['original','delta band, 0-4 Hz','theta band, 4-7 Hz','alpha band, 7-12 Hz','beta band, 12-30 Hz', 'Filtro 1','Filtro 2','Filtro 3','Filtro 4']
    number_of_signal = 0

    chno = 4   # total number of channels
    eeg = []

    y = all_results#eeg[:,ch]         # the signal, study channel 'ch'
    L = len(y)            # signal length
    fs = 200.0              # sampling rate
    T = 1/fs                # sample time
    t= linspace(1,L,L)*T   # time vector

    f = fs*linspace(0,L/10,L/10)/L  # single side frequency vector, real frequency up to fs/2
    Y = fft(y)

    filtered = []
    b= [] # store filter coefficient
    cutoff = [0.5,4.0,7.0,12.0,30.0]


    for band in range(0, len(cutoff)-1):
        wl = 2*cutoff[band]/fs*pi
        wh = 2*cutoff[band+1]/fs*pi
        M = 512      # Set number of weights as 128
        bn = zeros(M)

        for i in range(0,M):     # Generate bandpass weighting function
            n = i-  M/2       # Make symmetrical
            if n == 0:
                bn[i] = wh/pi - wl/pi;
            else:
                bn[i] = (sin(wh*n))/(pi*n) - (sin(wl*n))/(pi*n)   # Filter impulse response

        bn = bn*kaiser(M,5.2)  # apply Kaiser window, alpha= 5.2
        b.append(bn)

        [w,h]=freqz(bn,1)
        filtered.append(convolve(bn, y)) # filter the signal by convolving the signal with filter coefficients

    for i in range(0, len(filtered)):
        y_p = filtered[i]

    for i in range(0, len(filtered)):
        Y = filtered[i]
        Y = fft(Y [ int(M/2):int(L+M/2)])

        number_of_signal = i
        for j in range(0,len(f)):
            freq_element["channelId"] = str(i)
            freq_element["channelName"] = list_names[i]
            freq_element["date"] = f[j]
            freq_element["measure"] = abs(Y[j])
            output_to_js.append(freq_element.copy())

    for i in range(0, len(filtered)):   # plot filter's frequency response
        H = abs(fft(b[i], L))
        H = H*1.2*(max(Y)/max(H))
        number_of_signal = number_of_signal + 1
        for j in range(0,len(f)):
            freq_element["channelId"] = str(number_of_signal)
            freq_element["channelName"] = list_names[number_of_signal]
            freq_element["date"] = f[j]
            freq_element["measure"] = abs(3*H[j])
            output_to_js.append(freq_element.copy())

    session.close()
    return jsonify(output_to_js) 

@app.route("/api/v1.0/eeg/all")
def channel_all():
    """Return a list of all measurements"""
    # Query all dates
    #session.merge()
    #session = Session(engine)
    #session.query(Garbage).filter(Garbage.id == 3).delete()
    #str_channel = channel
    #ab = engine.execute("SELECT"+channel+", Time, TimeStamp FROM data").fetchall()

    #channel_nbr = int(channel[8])

    #results = session.query(SignalData.channel_1, SignalData.Time, SignalData.TimeStamp).all()
    results_1 = engine.execute("SELECT channel_1, TimeStamp FROM data").fetchall()
    results_2 = engine.execute("SELECT channel_2, TimeStamp FROM data").fetchall()
    results_3 = engine.execute("SELECT channel_3, TimeStamp FROM data").fetchall()
    results_4 = engine.execute("SELECT channel_4, TimeStamp FROM data").fetchall()
    results = results_1 + results_2 + results_3 + results_4
    all_results = []

    for result in results_1:
        result_dict = {}
        result_dict['channelId'] = 1 
        result_dict['channelName'] = 'channel_1' 
        result_dict['measure'] =result[0]
        result_dict['date'] = result[1]
        #result_dict['Total'] = rt
        all_results.append(result_dict)

    for result in results_2:
        result_dict = {}
        result_dict['channelId'] = 2 
        result_dict['channelName'] = 'channel_2' 
        result_dict['measure'] =result[0]
        result_dict['date'] = result[1]
        #result_dict['Total'] = rt
        all_results.append(result_dict)

    for result in results_3:
        result_dict = {}
        result_dict['channelId'] = 3 
        result_dict['channelName'] = 'channel_3' 
        result_dict['measure'] =result[0]
        result_dict['date'] = result[1]
        #result_dict['Total'] = rt
        all_results.append(result_dict)

    for result in results_4:
        result_dict = {}
        result_dict['channelId'] = 4 
        result_dict['channelName'] = 'channel_4' 
        result_dict['measure'] =result[0]
        result_dict['date'] = result[1]
        #result_dict['Total'] = rt
        all_results.append(result_dict)                

    session.close()
    return jsonify(all_results) 

@app.route("/api/v1.0/meassure")
def channel_m(meassure):
    """Return a list of all measurements"""
    # Query all dates
    #session.merge()
    #session = Session(engine)
    #session.query(Garbage).filter(Garbage.id == 3).delete()
    #str_channel = channel
    #ab = engine.execute("SELECT"+channel+", Time, TimeStamp FROM data").fetchall()

    channel_nbr = int(meassure[8])

    #results = session.query(SignalData.channel_1, SignalData.Time, SignalData.TimeStamp).all()
    results_1 = engine.execute("SELECT channel_1, TimeStamp FROM data limit 1000").fetchall()
    results_2 = engine.execute("SELECT channel_2, TimeStamp FROM data limit 1000").fetchall()
    results_3 = engine.execute("SELECT channel_3, TimeStamp FROM data limit 1000").fetchall()
    results_4 = engine.execute("SELECT channel_4, TimeStamp FROM data limit 1000").fetchall()
    results = results_1 + results_2 + results_3 + results_4
    all_results = []

    for result in results_1:
        result_dict = {}
        result_dict['channelId'] = 1 
        result_dict['channelName'] = 'channel_1' 
        result_dict['measure'] =result[0]
        result_dict['date'] = result[1]
        #result_dict['Total'] = rt
        all_results.append(result_dict)

    for result in results_2:
        result_dict = {}
        result_dict['channelId'] = 2 
        result_dict['channelName'] = 'channel_2' 
        result_dict['measure'] =result[0]
        result_dict['date'] = result[1]
        #result_dict['Total'] = rt
        all_results.append(result_dict)

    for result in results_3:
        result_dict = {}
        result_dict['channelId'] = 3 
        result_dict['channelName'] = 'channel_3' 
        result_dict['measure'] =result[0]
        result_dict['date'] = result[1]
        #result_dict['Total'] = rt
        all_results.append(result_dict)

    for result in results_4:
        result_dict = {}
        result_dict['channelId'] = 4 
        result_dict['channelName'] = 'channel_4' 
        result_dict['measure'] =result[0]
        result_dict['date'] = result[1]
        #result_dict['Total'] = rt
        all_results.append(result_dict)                

    session.close()
    return jsonify(all_results)    


if __name__ == '__main__':
    app.run(debug=True)
