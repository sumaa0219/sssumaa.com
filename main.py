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






@app.before_request
def before_request():
    if not request.is_secure and app.env != 'development':
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@app.route('/.well-known/acme-challenge/<filename>')
def well_known(filename):
    return render_template('.well-known/acme-challenge/'+ filename)


@app.route("/")
def hell():
    return render_template("top.html")


@app.route("/GfN/<string:st>")
def GfN(st):
    s = "web/" + st + ".html"
    return render_template(s)

@app.route("/download")
def download():
    filename = os.listdir(path=app.config['UPLOAD_FOLDER'])
    filename.sort()
    filekey = list(range(len(filename)))
    return render_template("download.html", data=zip(filename, filekey))


@app.route("/upload")
def upload():
    return render_template("upload.html")


@app.route("/put", methods=["POST"])
def put():
    putFile = request.files["file"]
    putName = secure_filename(putFile.filename)
    putFile.save(os.path.join(app.config['UPLOAD_FOLDER'], putName))
    return jsonify()



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

    


    app.run(host="0.0.0.0",ssl_context=('/etc/letsencrypt/live/sssumaa.net/fullchain.pem', '/etc/letsencrypt/live/sssumaa.net/privkey.pem'),debug=True,threaded=True)


# sumaa@raspberrypi:~/Desktop/api $ sudo certbot certonly --webroot -w /home/sumaa/Desktop/api/templates/ -d sssumaa.net