from app import app
from flask import render_template

@app.route('/',methods=['GET','POST'])
def add():

    return render_template('base/register.html')

