from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
import mysql.connector as MC
import sys
from passlib.hash import sha256_crypt
from datetime import time
from datetime import datetime #datetime is type of -> class <- datetime
import json

app = Flask(__name__, static_url_path='')
# Connect to DB and set cursor
db = MC.connect(host='localhost', database='users', user='admin', password='admin')

@app.route('/', methods=['GET','POST'])
def root():   
    #Renders a template from the template folder with the given context
    return render_template("index.html", title = 'Book Your Favourite Books')


#register form

@app.route("/login", methods=['GET','POST'])
def login():
    
    cursor = db.cursor(buffered=True) #fixes error mysql.connector Unread result found
    if request.method == "POST":
        email = request.form.get("email")
        passw =  request.form.get("password")
        
        cursor.execute("SELECT email FROM registered_users WHERE email = %s ",(email,))
        cursor.execute("SELECT password FROM registered_users WHERE email = %s ",(email,))
        email_data = cursor.fetchone()
        password_data = cursor.fetchone()        

        '''if email_data is None:
            flash("email is not registered - Sign Up", "danger")
            return redirect(url_for("login"))
        else:'''
        for pass_data in password_data:
            if sha256_crypt.verify(passw, pass_data):
                flash("You are logged", "success")
                return render_template("logged.html")
            else:
                flash("Incorrect password", "danger")
                return redirect(url_for("login"))


        cursor.close()
    return render_template("login.html")


@app.route("/register", methods=['GET','POST'])
def register():

    if request.method == "POST":
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        email = request.form.get("reg-email")
        password = request.form.get("reg-password")
        confirm = request.form.get("retype-reg-password")
        secure_password = sha256_crypt.encrypt(str(password))

        if password == confirm:
            cursor = db.cursor()

            new_query = """
            INSERT INTO registered_users (name, lastname, email, password) 
            VALUES (%s, %s, %s, %s)
            """
            query = (name, lastname, email, secure_password)
            # query (inputed values) saves in new_query via %s in SQL
            cursor.execute(new_query, query)
            db.commit()
            cursor.close()
            flash("You are  successfully registered", "success")
            return redirect(url_for("login"))
        else:
            flash("passwords does not match", "danger")
            return render_template("register.html")

    return render_template("register.html")

if __name__ == '__main__':
    app.secret_key="123456789bookbooks"
    app.run(debug = True)
