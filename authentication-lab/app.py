from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config= {
  "apiKey": "AIzaSyCx_PRgQSNOnNS6Sckx2YzGk-mGxtcsnQ0",
  "authDomain": "fir-project-1-17fcf.firebaseapp.com",
  "projectId": "fir-project-1-17fcf",
  "storageBucket": "fir-project-1-17fcf.appspot.com",
  "messagingSenderId": "688890008130",
  "appId": "1:688890008130:web:befaa2e9838638fc3613db",
  "measurementId": "G-036GGX7ZGG",
  "databaseURL":""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app= Flask(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try: 
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('add_tweet'))
        except: 
            error = "Authentication failed"
    return render_template("signup.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try: 
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            return redirect(url_for('add_tweet'))
        except: 
            error = "Authentication failed"
    return render_template("signup.html")

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")

if __name__ == '__main__':
    app.run(debug=True)