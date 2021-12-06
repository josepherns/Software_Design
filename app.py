from flask import Flask,redirect,url_for,jsonify
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///School.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Accounts(db.Model):
    __tablename__="account"
    email = db.Column(db.String(50), primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password = password

class AccountsMeta(ma.Schema):
    class Meta:
        fields = ("email", "username", "password")


account_meta = AccountsMeta()
accounts_meta = AccountsMeta(many = True)

class Products(db.Model):
    __tablename__="product"
    barcode = db.Column(db.Integer,primary_key=True)
    product = db.Column(db.String(50))
    status = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    def __init__(self,barcode,product,status,quantity):
        self.barcode = barcode
        self.product = product
        self.status = status
        self.quantity = quantity

class ProductsMeta(ma.Schema):
    class Meta:
        fields = ("barcode","product","status","quantity")

product_meta = ProductsMeta()
products_meta = ProductsMeta(many = True)

@app.route("/")
def main():
    return render_template("index.html")
@app.route("/Homepage")
def Homepage():
    return render_template("Homepage.html")
@app.route("/login_form",methods=['GET','POST'])
def login_form():
    if request.method == 'POST':
        username2=request.form.get("Login_Username")
        password2=request.form.get("Login_Password")
        print(username2,password2)
        if username2 != "" and password2 != "":
            Check = Accounts.query.filter_by(username=username2).first()
            if Check is None:
                return redirect(url_for('main'))
            if Check.username == username2 and Check.password == password2:
                print(Check.password)
                return redirect(url_for('Homepage'))
            else:
                print("No such account")
                return redirect(url_for('main'))
        else:
            return redirect(url_for('main'))

@app.route('/signup_form', methods=['GET', 'POST'])
def signup_form():
    if request.method == 'POST':
        email=request.form.get("Register_Email")
        user=request.form.get("Register_Username")
        passs=request.form.get("Register_Password")
        passs2=request.form.get("Confirm_Password")
        print(email,user,passs,passs2,(passs == passs2))
        if email == "" or user == "" or passs == "" or passs2 == "":
            print("Please Fill up the form")
            return redirect(url_for('main'))
        elif(passs != passs2):
            print("Password and Confirm Password are not the same")
            return redirect(url_for('main'))
        else:
            print("Signup Successful")
            new_account = Accounts(email,user,passs)
            db.session.add(new_account)
            db.session.commit()
            return redirect(url_for('main'))

@app.route('/Product',methods=['GET','POST'])
def product():
    rows = Products.query.all()
    return render_template("products.html",rows=rows)

@app.route('/About_Us')
def about_us():
    return render_template("aboutus.html")

@app.route('/Orders')
def orders():
    return render_template("orders.html")

@app.route('/product_form', methods=['GET','POST'])
def product_form():
    if request.method == 'POST':
        Barcode=request.form.get("Barcode_Input")
        Product=request.form.get("Product_Input")
        Status=request.form.get("Status_Input")
        Quantity=request.form.get("Quantity_Input")
        print(Barcode,Product,Status,Quantity)
        productss = Products(Barcode,Product,Status,Quantity)
        db.session.add(productss)
        db.session.commit()
        return redirect(url_for('product'))
#this is our update route where we are going to update our Product
@app.route('/Product_update', methods = ['GET', 'POST'])
def Product_update():
 
    if request.method == 'POST':
        rows = Products.query.get(request.form.get('id'))
 
        rows.Barcode=request.form.get("Barcode_Edit")
        rows.Product=request.form.get("Product_Edit")
        rows.Status=request.form.get("Status_Edit")
        rows.Quantity=request.form.get("Quantity_Edit")
        db.session.commit() 
        return redirect(url_for('product'))
 
 
 
 
#This route is for deleting our product
@app.route('/Product_delete/<id>/', methods = ['GET', 'POST'])
def Product_delete(id):
    rows = Products.query.get(id)
    db.session.delete(rows)
    db.session.commit()
    
 
    return redirect(url_for('product'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
