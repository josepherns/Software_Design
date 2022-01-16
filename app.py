from flask import Flask,redirect,url_for,request,render_template,session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from barcode import Code128
from barcode.writer import ImageWriter
import io, cv2
import numpy as np
from datetime import datetime
from pyzbar.pyzbar import decode


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///School.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)


def yes(self):
    self.yepyep="a"

class Accounts(db.Model):
    __tablename__="account"
    email = db.Column(db.String(50), primary_key = True)
    username = db.Column(db.String(50), primary_key=True)
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

db.create_all()

@app.route("/")
def main():
    return render_template("index.html")
@app.route("/Homepage")
def Homepage():
    if not session.get("name"):
        return redirect("/")
    else:
        rows = Products.query.all()
        return render_template("Homepage.html",rows=rows)
@app.route("/login_form",methods=['GET','POST'])
def login_form():
    if request.method == 'POST':
        username2=request.form.get("Login_Username")
        password2=request.form.get("Login_Password")
        print(username2,password2)
        if username2 != "" and password2 != "":
            Check = Accounts.query.filter_by(username=username2).first()
            if Check is None:
                msg="No_Such_Account"
                return redirect(url_for('main',msg=msg))
            if Check.username == username2 and Check.password == password2:
                session["name"] = request.form.get("Login_Username")
                msg="Successfully_Logged_In"
                return redirect(url_for('Homepage',msg=msg))
            else:
                msg="Wrong_Password"
                return redirect(url_for('main',msg=msg))
        else:
            msg="Wrong_Username_and_Password"
            return redirect(url_for('main',msg=msg))

@app.route('/signup_form', methods=['GET', 'POST'])
def signup_form():
    if request.method == 'POST':
        email2=request.form.get("Register_Email")
        user=request.form.get("Register_Username")
        passs=request.form.get("Register_Password")
        passs2=request.form.get("Confirm_Password")
        Check_User= Accounts.query.filter_by(username=user).first()
        Check_Email=Accounts.query.filter_by(email=email2).first()
        if email2 == "" or user == "" or passs == "" or passs2 == "":
            msg="Please_Fill_up_the_form"
            return redirect(url_for('main',msg=msg))
        elif(passs != passs2):
            msg="Wrong_Password_and_Confirm_Password"
            print("Password and Confirm Password are not the same")
            return redirect(url_for('main',msg=msg))
        elif(Check_Email is None and Check_User is None):
            msg = "Successfully_Registered"
            new_account = Accounts(email2,user,passs)
            db.session.add(new_account)
            db.session.commit()
            return redirect(url_for('main',msg=msg))
        else:
            msg = "Existing_Email_or_Username"
            return redirect(url_for('main',msg=msg))
            
@app.route('/Product',methods=['GET','POST'])
def product():
    if not session.get("name"):
        return redirect("/")
    else:
        rows = Products.query.all()
        return render_template("products.html",rows=rows)


@app.route('/About_Us')
def about_us():
    if not session.get("name"):
        return redirect("/")
    else:
        return render_template("aboutus.html")

@app.route('/Orders')
def orders():
    if not session.get("name"):
        return redirect("/")
    else:
        return render_template("orders.html")

@app.route('/product_form', methods=['GET','POST'])
def product_form():
    if not session.get("name"):
        return redirect("/")
    else:
        if request.method == 'POST':
            Barcode2=request.form.get("Barcode_Input")
            Product=request.form.get("Product_Input")
            Status=request.form.get("Status_Input")
            Quantity=request.form.get("Quantity_Input")
            Check_Barcode= Products.query.filter_by(barcode=Barcode2).first()
            if(Check_Barcode is None and len(Barcode2) == 9):
                Create_Barcode(Barcode2)
                productss = Products(Barcode2,Product,Status,Quantity)
                msg="Successfully_Added"
                db.session.add(productss)
                db.session.commit()
                return redirect(url_for('product',msg=msg))
            else:
                msg="Existing_Barcode"
                return redirect(url_for('product',msg=msg))
            
@app.route('/Profile')
def profile():
    if not session.get('name'):
        return redirect("/")
    else:
        rows = Products.query.filter_by(barcode=yes.yepyep).first()
        return render_template("profile.html",rows=rows)

@app.route('/search_barcode', methods=['GET','POST'])
def search_barcode():
    if not session.get("name"):
        return redirect("/")
    else:
        if request.method == 'POST':
            Barcode2=request.form.get("Barcode_Input")
            Check_Barcode= Products.query.filter_by(barcode=Barcode2).first()
            if(Check_Barcode is None or len(Barcode2) != 9):
                msg="There_is_no_such_Barcode"
                return redirect(url_for('orders',msg=msg))
            else:
                msg=Barcode2
                yes.yepyep=Barcode2
                return redirect(url_for('profile',id=msg))

@app.route('/Product/<id>/Delete', methods=['GET','POST'])
def delete(id):
    if not session.get("name"):
        return redirect("/")
    else:
        product=Products.query.get(id)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('product'))


@app.route('/Product/<id>/Update',methods=['GET','POST'])
def update(id):
    if not session.get("name"):
        return redirect("/")
    else:
        bar=Products.query.get(id)
        if request.method == 'POST':
            if bar:
                db.session.delete(bar)
                db.session.commit()

                produc=request.form["Update_Product"]
                statu=request.form["Update_Status"]
                quantit=request.form["Update_Quantity"]

                bar=Products(barcode=id,product=produc,status=statu,quantity=quantit)
                db.session.add(bar)
                db.session.commit()
                return redirect(url_for('product'))

@app.route('/Profile/<id>/Add',methods=['GET','POST'])
def profile_add(id):
    if not session.get("name"):
        return redirect("/")
    else:
        product=Products.query.get(id)
        product_added=product.quantity+1
        produc=product.product
        statu=product.status
        db.session.delete(product)
        db.session.commit()

        bar=Products(barcode=id,product=produc,status=statu,quantity=product_added)
        db.session.add(bar)
        db.session.commit()
        return redirect(url_for('profile',msg="Added"))

@app.route('/Profile/<id>/Sub',methods=['GET','POST'])
def profile_sub(id):
    product=Products.query.get(id)
    if not session.get("name"):
        return redirect("/")
    elif product.quantity <= 0:
        return redirect(url_for('profile',msg="The_Quantity_is_0"))
    else:        
        product_added=product.quantity-1
        produc=product.product
        statu=product.status
        db.session.delete(product)
        db.session.commit()

        bar=Products(barcode=id,product=produc,status=statu,quantity=product_added)
        db.session.add(bar)
        db.session.commit()
        return redirect(url_for('profile',msg="Subtracted"))

@app.route('/Profile/<id>/Multiple_Add',methods=['GET','POST'])
def multiple_add(id):
    product=Products.query.get(id)
    if not session.get("name"):
        return redirect("/")
    else:
        new_value=request.form["Mul_Quantity"]
        product_added=product.quantity+int(new_value)
        produc=product.product
        statu=product.status
        db.session.delete(product)
        db.session.commit()

        bar=Products(barcode=id,product=produc,status=statu,quantity=product_added)
        db.session.add(bar)
        db.session.commit()
        return redirect(url_for('profile',msg="Added_Multiple_Times"))

@app.route('/Profile/<id>/Multiple_Sub',methods=['GET','POST'])
def multiple_sub(id):
    product=Products.query.get(id)
    new_value=request.form["Mul_Sub_Quantity"]
    if not session.get("name"):
        return redirect("/")
    elif int(new_value) < 0 or product.quantity < int(new_value):
        return redirect(url_for('profile',msg="Invalid_Input"))
    else:
        product_added=product.quantity-int(new_value)
        produc=product.product
        statu=product.status
        db.session.delete(product)
        db.session.commit()

        bar=Products(barcode=id,product=produc,status=statu,quantity=product_added)
        db.session.add(bar)
        db.session.commit()
        return redirect(url_for('profile',msg="Subtracted_Multiple_Times"))
def Create_Barcode(yes):
    hehe= 'static/barcode/'
    hehe2=hehe+yes+".jpeg"
    with open(hehe2,'wb') as f:
        Code128(yes,writer =ImageWriter()).write(f)

        

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")
if __name__ == "__main__":
    yes.yepyep="a"
    app.run(host="0.0.0.0", port=8080)