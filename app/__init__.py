from flask import Flask,current_app
from flask_assets import Bundle,Environment
import os
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

app = Flask (__name__)

imgfolder = os.path.join('static','image')
app.config['UPLOAD_FOLDER'] = imgfolder

css = Bundle ('css/admin.css','css/home.css','css/login.css','css/payment.css','css/explore.css','css/cars.css',output='gen/main.css')
assets = Environment(app)
assets.register('main_css',css)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root123'
app.config['MYSQL_DB'] = 'cars'
mysql = MySQL(app)



def save_images(photo):
    name = os.path.splitext(photo.filename)
    print(os.path.splitext(photo.filename))
    if name[1] in ".jpg,.png,.jpeg":
        photo_name = name[0] + name[1]
    file_path = os.path.join(current_app.root_path, 'static/image/cars',photo_name)
    photo.save(file_path)

    return photo_name

from app import admin,sign