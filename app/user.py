from app import app,mysql,save_images,time,total
from flask import render_template, redirect , url_for ,current_app, flash , request,session
import os
from app import admin


@app.route('/dash',methods=["GET","POST"])
def dash():
    '''
    a[0] : carname
    a[1] : price
    a[2] : transmission
    a[3] : fule
    '''
    if session:
        userid = session['userid']
        cur = mysql.connection.cursor()
        cur.execute('select * from cars')
        cars = cur.fetchall() 
        mysql.connection.commit()
        cur.close()
    else:
        return redirect("login")
    return render_template('user/customerdash.html',cars = cars,id=userid)

@app.route('/logout')
def logout():
    session.pop('userid',None)
    return redirect("login")

@app.route('/booking',methods=['GET','POST'])
def booking():
    if request.method == "POST":
        carid = request.form.get('carid')
        cur = mysql.connection.cursor()
        cur.execute("select * from cars where id = '{0}'".format(carid))
        cardetails = cur.fetchone()
        mysql.connection.commit()
        cur.close()
    return render_template('user/booking.html',cardetails=cardetails)


@app.route('/book',methods=['GET','POST'])
def book():
    if session:
        userid = session['userid']
        if request.method =="POST":
            carid = request.form.get("carid")
            cur = mysql.connection.cursor()
            cur.execute("SELECT carmodel,fueltype,transmission,cost,carpic from cars")
            cardetails = cur.fetchone()
            mysql.connection.commit()
            cur.close()
    else:
        return redirect("login")
    return render_template("user/book.html" ,userid = userid,carid=carid,cardetails=cardetails)


@app.route("/booked",methods=["POST","GET"])
def insertingBookings():
    if request.method == "POST":
        userid = session["userid"]
        carid = request.form.get('carid')
        print(carid)
        #userid = request.form.get('userid')
        pickuploc = request.form.get('pickuploc')
        print(pickuploc)
        droploc = request.form.get('droploc')
        print(droploc)
        pickupdate = request.form.get("pickupdate")
        dropdate = request.form.get("dropdate")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO bookings(customerid,carid,pickuploc,droploc,pickupdate,dropdate) VALUES(%s,%s,%s,%s,%s,%s)"
                    ,(userid,carid,pickuploc,droploc,pickupdate,dropdate))
        mysql.connection.commit()
        cur.close()
    return render_template("user/payment.html",carid = carid)


@app.route('/')
def explore():
    first = os.path.join (app.config['UPLOAD_FOLDER'],'cars/i20.png')
    sec = os.path.join (app.config['UPLOAD_FOLDER'],'cars/maruthi.jpg')
    tri = os.path.join (app.config['UPLOAD_FOLDER'],'cars/maruti.jpg')
    return render_template('user/explore.html',img1=first,img2=sec,img3=tri)




@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
            name = request.form.get('username')
            print(name)
            password = request.form.get('password')
            cur = mysql.connection.cursor()
            cur.execute("SELECT customerid,username FROM customer WHERE username = '{0}'".format(name))
            userdb = cur.fetchone()
            cur.execute("SELECT password FROM customer WHERE username = '{0}'".format(name))
            passdb = cur.fetchone()
            mysql.connection.commit()
            cur.close()
            if len(name) > 0 and len(password) > 0:
                if name in userdb[1] and password in passdb:
                    session["userid"] = userdb[0]
                    # session={"userid":"user_id"}
                    #print(session.get("userid"))
                    return redirect(url_for('dash'))
                else:
                    return redirect(url_for('login'))
    return render_template ('user/login.html')  


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get("username")
        phone = request.form.get("phone")
        email = request.form.get("email")
        dlno = request.form.get("drivers-licence")
        password = request.form.get("password")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customer(username,phonenumber,emailid,dlno,password) VALUES(%s,%s,%s,%s,%s)",(name,phone,email,dlno,password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template ('user/register.html')  

@app.route("/thankyou",methods=['GET','POST'])
def thank():
    if request.method =="POST":
        userid = session["userid"]
        cur = mysql.connection.cursor()
        cur.execute("select bookingid,carid from bookings order by bookingid desc limit 1")
        recent = cur.fetchone()
        print(recent)
        cur.execute("""select bookings.pickupdate,bookings.dropdate,cars.cost from bookings,cars 
                            where bookings.bookingid = '{0}' and cars.carid='{1}'""".format(recent[0],recent[1]))
        calc = cur.fetchone()
        print(calc)
        mysql.connection.commit()
        cur.close()
        datentime = time()
        print(datentime)
        total_amount = total(calc[0],calc[1],calc[2])
        print(userid,recent,datentime,total)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO billing(customerid,bookingid,billingtime,billingdate,totalamount) VALUES(%s,%s,%s,%s,%s)"
            ,(userid,recent[0],datentime["time"],datentime["date"],total_amount))
        mysql.connection.commit()
        cur.close()
    return render_template("user/thankyou.html")



@app.route('/reviews',methods=['GET','POST'])
def reviews():
    if request.method == 'POST':
        userid = session["userid"]
        review = request.form.get('review')
        brief = request.form.get('brief')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO reviews(customerid,review,brief) VALUES(%s,%s,%s)",(userid,review,brief))
        mysql.connection.commit()
        cur.close()
    return render_template("user/reviews.html")
    

@app.route('/prebookings',methods=['GET','POST'])
def prebookings():
    userid = session["userid"]
    cur = mysql.connection.cursor()
    cur.execute("select * from bookings where customerid = {}".format(userid))
    all_data = cur.fetchall()
    print(all_data)
    mysql.connection.commit()
    cur.close()
    return render_template("user/prebookings.html",data=all_data)


