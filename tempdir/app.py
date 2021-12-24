from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/login_form",methods=['GET','POST'])
def login_form():
    if request.method == 'POST':
        username=request.form.get("uname")
        password=request.form.get("psw")
        confirm=request.form.get("confirm")
        return redirect(url_for('/'))
    return render_template('login.html')

@app.route('/signup_form', methods=['GET', 'POST'])
def signup_form():
    if request.method == 'POST':
        return redirect(url_for('/'))
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)