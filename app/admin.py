from app import app,mysql,save_images
from flask import render_template, redirect , url_for ,current_app, flash , request
import os
import secrets






@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == "POST":
        carmodel  = request.form.get('carmodel')
        fueltype  = request.form.get('fueltype')
        transmission  = request.form.get('transmission')
        cost = request.form.get('cost')
        carpic = save_images(request.files.get ('carpic'))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO car(carmodel,fueltype,transmission,cost,carpic) VALUES(%s,%s,%s,%s,%s)",(carmodel,fueltype,transmission,cost,carpic))
        mysql.connection.commit()
        cur.close()

    return render_template('base/add.html')

@app.route('/d',methods=['GET','POST'])
def display():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin")
    a = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    for i in a:
        filename = i[3]
    with open(filename,'wb') as f:
        x = f.write(filename)
    return render_template('base/display.html',pic = x)


@app.route('/login')
def login():
    bg_img = os.path.join (app.config['UPLOAD_FOLDER'],'bg.png')
    return render_template('base/login.html', img1 = bg_img)

@app.route('/')
def home():
    
    return render_template('base/home.html')


@app.route('/register')
def reg():
    bg_img = os.path.join (app.config['UPLOAD_FOLDER'],'bg.png')
    return render_template('base/register.html', img1 = bg_img)

@app.route('/admin')
def admin():
    bg_img = os.path.join (app.config['UPLOAD_FOLDER'],'bg.png')
    return render_template('base/admin.html', img1 = bg_img)

@app.route('/payment')
def payment():
    bg_img = os.path.join (app.config['UPLOAD_FOLDER'],'bg.png')
    return render_template('base/admin.html', img1 = bg_img)

@app.route('/explore')
def explore():
    first = os.path.join (app.config['UPLOAD_FOLDER'],'bg.png')
    sec = os.path.join (app.config['UPLOAD_FOLDER'],'cars/i20.jpg')
    tri = os.path.join (app.config['UPLOAD_FOLDER'],'cars/maruti.jpg')
    return render_template('base/explore.html',img1=first,img2=sec,img3=tri)

    
@app.route('/dash')
def dash():
    '''
        a[0] : carname
    a[1]: price
    a[2]: transmission
    a[3] : fule
    '''

    cur = mysql.connection.cursor()
    cur.execute('select * from car')
    cars = cur.fetchall() 
    mysql.connection.commit()
    cur.close()
    return render_template('base/customerdash.html',cars=cars)

@app.route('/modify')
def mod():
    
    cur = mysql.connection.cursor()
    cur.execute('select * from car')
    cars = cur.fetchall() 
    mysql.connection.commit()
    cur.close()
    return render_template("base/modify.html",cars=cars)