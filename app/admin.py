from app import app,mysql
from flask import render_template, redirect , url_for ,current_app, flash , request
import os
import secrets
def save_images(photo):
    name = os.path.splitext(photo.filename)
    print(os.path.splitext(photo.filename))
    if name[1] in ".jpg,.png,.jpeg":
        photo_name = name[0] + name[1]
    file_path = os.path.join(current_app.root_path, 'static/image',photo_name)
    photo.save(file_path)

    return photo_name



@app.route('/',methods=['GET','POST'])
def add():
    if request.method == "POST":
        carmodel  = request.form.get('carmodel')
        fueltype  = request.form.get('fueltype')
        transmission  = request.form.get('transmission')
        cost = request.form.get('cost')
        carpic = save_images(request.files.get ('carpic'))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO admin(carmodel,fueltype,transmission,carpic) VALUES(%s,%s,%s,%s)",(carmodel,fueltype,transmission,carpic))
        mysql.connection.commit()
        cur.close()
    return render_template('base/add.html')

