from app import app,mysql,save_images
from flask import render_template, redirect , url_for ,current_app, flash , request,session
import os
import secrets
import random






@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    if request.method == "POST":
            name = request.form.get('username')
            print(name)
            password = request.form.get('password')
            if len(name) > 0 and len(password) > 0:
                if name in "admin" and password in "admin123":
                    session["userid"] = 1
                    print(session.get("userid"))
                    return redirect('modify')
                else:
                    return redirect(url_for('/login'))
    return render_template ('admin/login.html') 

@app.route('/custmorebookings',methods=['GET','POST'])
def bookings():
    cur = mysql.connection.cursor()
    cur.execute("select * from bookings")
    all_data = cur.fetchall()
    print(all_data)
    mysql.connection.commit()
    cur.close()
    return render_template("admin/bookings.html",data=all_data)

@app.route('/modify')
def index():
    cur = mysql.connection.cursor()
    cur.execute("select * from cars")
    all_data = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template("admin/modify.html",dat=all_data)

@app.route('/insert',methods=['POST'])
def insert():
    if request.method == "POST":
        carname = request.form.get('carname')
        fuel = request.form.get('fuel')
        transmission = request.form.get('transmission')
        price = request.form.get('price')
        image = save_images(request.files.get('image'))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO cars(carmodel,fueltype,transmission,cost,carpic) VALUES(%s,%s,%s,%s,%s)", (carname,fuel,transmission,price,image))
        mysql.connection.commit()
        cur.close()
        return redirect (url_for("index"))

@app.route("/update",methods = ['GET','POST'])
def update():
    if request.method == 'POST':
        carid = request.form.get('carid')
        print("===========",carid)
        cur = mysql.connection.cursor()
        cur.execute("select carmodel,fueltype,transmission,cost,carpic from cars where carid = {} ".format(carid))
        car = cur.fetchone()
        p = list(car)
        p[0] = request.form.get('carname')
        p[1] = request.form.get('fuel')
        p[2] = request.form.get('transmission')
        p[3] = request.form.get('price')
        p[4] = save_images(request.files.get('image'))
        cur.execute("UPDATE cars SET carmodel = '{1}' , fueltype = '{2}' , transmission = '{3}' , cost = '{4}' , carpic = '{5}'  WHERE carid = '{0}'".format(carid,p[0],p[1],p[2],p[3],p[4]))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/delete/<id>/', methods=['GET','POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cars WHERE carid = '{0}'".format(id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))


@app.route('/viewcust',methods=['GET','POST'])
def viewcust():
    cur = mysql.connection.cursor()
    cur.execute("select * from customer")
    all_data = cur.fetchall()
    print(all_data)
    mysql.connection.commit()
    cur.close()
    return render_template("admin/viewcust.html",data=all_data)
