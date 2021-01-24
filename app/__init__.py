from flask import Flask,current_app
from flask_assets import Bundle,Environment
import os,datetime
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

app = Flask (__name__)
app.secret_key = "hack123"
imgfolder = os.path.join('static','image')
app.config['UPLOAD_FOLDER'] = imgfolder

css = Bundle ('css/admin.css','css/login.css','css/modify.css','css/payment.css','css/explore.css','css/cars.css','css/book.css',output='gen/main.css')
assets = Environment(app)
assets.register('main_css',css)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root123'
app.config['MYSQL_DB'] = 'rnr'
mysql = MySQL(app)

def time():
    Now = datetime.datetime.now()
    datentime = {"date":Now.strftime("%y-%m-%d"),"time":Now.strftime("%y-%m-%d")}
    return datentime

def total(d1,d2,t):
   tdate1 = d1.split("-")
   tdate2 = d2.split("-")
   date1 = datetime.date(int(tdate1[0]),int(tdate1[1]),int(tdate1[2]))
   date2 = datetime.date(int(tdate2[0]),int(tdate2[1]),int(tdate2[2])) 

   no_of_days = (date1-date2).days
   amount = no_of_days*int(t)
   return amount

def save_images(photo):
    name = os.path.splitext(photo.filename)
    print(os.path.splitext(photo.filename))
    if name[1] in ".jpg,.png,.jpeg ,.JPG, .PNG, .JPEG":
        photo_name = name[0] + name[1]
    file_path = os.path.join(current_app.root_path, 'static/image/cars',photo_name)
    photo.save(file_path)
    return photo_name

from app import admin,user