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
  "databaseURL":"https://fir-project-1-17fcf-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db= firebase.database()

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
        #try: 
        login_session['user'] = auth.create_user_with_email_and_password(email,password)
        user= {"name": request.form['name'], "email":request.form['email'], "username":request.form['username'], "bio":request.form['bio']}
        db.child("Users").child(login_session['user']['localId']).set(user)
        return redirect(url_for('add_tweet'))
        # except: 
        #     error = "Authentication failed"
    return render_template("signup.html")

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error =""
    if request.method== 'POST':
        try:
            tweet = {"uid": login_session['user']['localId'],"title":request.form['title'], "text":request.form['text']}
            db.child("Tweets").push(tweet)
            return redirect(url_for('add tweet'))
        except:
            error = "Authentication failed"
    return render_template("add_tweet.html")


@app.route('/tweets')
def display_users():
    users=db.child("Users").get().val()
    return render_template("/tweets.html", users=users)



if __name__ == '__main__':
    app.run(debug=True)