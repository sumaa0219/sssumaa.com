from email.mime.text import MIMEText
from flask.helpers import url_for
import os
from flask import Flask,render_template,request,redirect,Blueprint,jsonify
from werkzeug.utils import secure_filename
import requests
import json
from datetime import datetime, timezone, timedelta
import locale
# from flask_httpauth import HTTPBasicAuth
app = Flask(__name__, static_folder='static',static_url_path="")
# auth = HTTPBasicAuth()



wetherapikey = "80efcb09546b956c8fa14024be0cd5fa"

lat = "35.68944"
lon = "139.69167"





@app.route("/")
def hell():
    return render_template("top.html")




@app.route("/wheather")
def wheather():
    params = {'zipcode':'2330008'}
    reswea = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + lat + "&lon="+lon +"&exclude=dairy&appid="+wetherapikey+"&lang=ja&units=metric", params=params)
    return json.dumps(reswea.json())
    
@app.route("/unixJST/<int:unixtime>")
def convtime(unixtime):
    JST = timezone(timedelta(hours=+9), 'JST')
    dt = datetime.fromtimestamp(unixtime).replace(tzinfo=timezone.utc).astimezone(tz=JST)
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    date = dt.strftime('%a')
    return  str(date)


if __name__ == '__main__':

    


    app.run(host="0.0.0.0",debug=True,threaded=True)
