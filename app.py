# From the project folder, open this Python file in a terminal window
# Then visit localhost:5000 in a web browser

from flask import * # Install Python and Flask on your local machine
import sqlite3
import hashlib



app = Flask(__name__)


# Create database for user accounts and apartment units and anything else
con = sqlite3.connect('data.db', check_same_thread=False)


# Connect to database and create a Users table if it is new.
# con = sqlite3.connect('users.db', check_same_thread=False)
# cur = con.cursor()
# cur.execute(''' CREATE TABLE IF NOT EXISTS Users (
# 	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#	"username"	TEXT UNIQUE NOT NULL,
#	"email"	TEXT NOT NULL,
#	"password"	TEXT NOT NULL
# );
# ''')
# con.commit()


#Homepage
@app.route('/')
#@app.route('/home/')
def home():

    #msg = "Hello World!"
    return render_template('home.html') #,msg=msg)



# Page to create a user account
@app.route('/apply/', methods=['POST', 'GET'])
def apply():
    msg = ""

    print("gets to apply")
    # User creates an account
    if request.method == 'POST':

        print("gets to apply")

        # Get the form data
        fn_enter = request.form['fname']
        ln_enter = request.form['lname']
        phone_enter = request.form['phone']
        em_enter = request.form['email']
        pw_enter = request.form['pass']
        pwCon_enter = request.form['conPass']

        # Hash the attempted password
        pw_enter_hash = hashlib.sha256(pw_enter.encode())
        pw_enter_hash = pw_enter_hash.hexdigest()

        try:
            if pw_enter == pwCon_enter:
                msg = "Password confirmed"
                print(msg)
                return render_template('apply.html', msg=msg)
            else:
                msg = "Passwords do not match"
                print(msg)
                return render_template('apply.html', msg=msg)

        except:
            msg = "Invalid form. Try again."
            return render_template('apply.html', msg=msg)


    return render_template('apply.html', msg=msg)


# Login page
@app.route('/login/', methods=['POST', 'GET'])
def login():
    msg = ""

    # User login attempt
    if request.method == 'POST':

        em_enter = request.form['email']
        pw_enter = request.form['pass']

        # Hash the attempted password
        pw_enter_hash = hashlib.sha256(pw_enter.encode())
        pw_enter_hash = pw_enter_hash.hexdigest()

        msg = "Login attempt with email: " + em_enter + " and password: " + pw_enter_hash


    return render_template('login.html', msg=msg)



# Apartment registration page
@app.route('/register/', methods=['POST', 'GET'])
def register():
    msg=""

    # User register form
    if request.method == 'POST':
        pass
        # all form inputs will go here



    return render_template("reg.html", msg=msg)



if __name__ == '__main__':
    app.run()

    con.close()