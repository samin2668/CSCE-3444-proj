# From the project folder, open this Python file in a terminal window
# Then visit localhost:5000 in a web browser

from flask import * # Install Python and Flask on your local machine
import sqlite3
import hashlib


# Create Flask
app = Flask(__name__)

# Custom key for the Flask app
app.secret_key = 'this is a key'


# Create database for user accounts and apartment units and anything else
con = sqlite3.connect('data.db', check_same_thread=False)


# Create a users table in the database
cur = con.cursor()
cur.execute(''' CREATE TABLE IF NOT EXISTS Users (
 	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "firstname" TEXT NOT NULL,
    "lastname" TEXT NOT NULL,
    "phone" TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"password"	TEXT NOT NULL
);
''')
con.commit()


#Homepage
@app.route('/')
#@app.route('/home/')
def home():

    # Check if a user is currently logged in
    if session.get('loggedin') == True:
        print("logged in = " + str(session['loggedin']) + "    " + str(session['user_email']))
        pass
    else:
        # Session variables
        session['loggedin'] = False
        session['user_email'] = ""


    #msg = "Hello World!"
    return render_template('home.html', user=session['user_email'])



# Page to create a user account
@app.route('/apply/', methods=['POST', 'GET'])
def apply():
    msg = ""
    print("gets to apply")

    # User creates an account
    if request.method == 'POST':

        print("gets to apply")

        # Get the form input
        fn_enter = request.form['fname']
        ln_enter = request.form['lname']
        phone_enter = request.form['phone']
        em_enter = request.form['email']
        pw_enter = request.form['pass']
        pwCon_enter = request.form['conPass']

        # Hash the attempted password
        pw_enter_hash = hashlib.sha256(pw_enter.encode())
        pw_enter_hash = pw_enter_hash.hexdigest()

        # Confirm that the passwords match
        try:
            if pw_enter == pwCon_enter:
                msg = "Password confirmed"
                print(msg)

            else:
                msg = "Passwords do not match"
                print(msg)
                return render_template('apply.html', msg=msg)

        except:
            msg = "Invalid input. Try again."
            return render_template('apply.html', msg=msg)


        # Add the user to the users table
        try:
            cur.execute('''INSERT INTO Users (firstname, lastname, phone, email, password) VALUES (?, ?, ?, ?, ?)''', (fn_enter, ln_enter, phone_enter, em_enter, pw_enter_hash))
            con.commit()

            # Display account creation message
            msg = "Account created!"
            return render_template("apply.html", msg=msg)

        except Exception as e:
            # Display error
            msg = "An error occured."
            print(str(e))
            return render_template("apply.html", msg=msg)


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

        # If nothing is entered
        if request.form['email'] == '' or request.form['pass'] == '':
            msg = "Please enter an email AND a password..."

        else:
            # Look for user in the Users table
            cur.execute('''SELECT * FROM Users WHERE email = ? AND password = ?''', (em_enter, pw_enter_hash))
            con.commit()
            foundUser = cur.fetchall()

            # Success
            if foundUser:
                msg = "Successful login!"
                session['loggedin'] = True
                session['user_email'] = em_enter

                # Go back to the homepage
                return redirect('/')

            # Invalid input
            else:
                msg = "Invalid username and password..."
                session.clear()

    # Reload the login page with the "invalid" message
    return render_template('login.html', msg=msg)


# Logout of the user's account
@app.route('/logout/', methods=['POST', 'GET'])
def logout():

    # Clear the session variables
    session["loggedin"] = False
    session.pop('user_email', None)
    session.clear()

    # Return to the home page
    return redirect(url_for('home'))


# Apartment registration page
@app.route('/register/', methods=['POST', 'GET'])
def register():
    msg=""

    # User register form
    if request.method == 'POST':
        pass
        # all form inputs will go here



    return render_template("reg.html", msg=msg)




@app.route('/amenities/', methods=['POST', 'GET'])
def amenities():
    msg=""

    if request.method == 'POST':
        pass
        # any form inputs will go here


    return render_template("amenities.html", msg=msg)




@app.route('/gallery/', methods=['POST', 'GET'])
def gallery():
    msg=""

    if request.method == 'POST':
        pass
        # any form inputs will go here


    return render_template("gallery.html", msg=msg)



@app.route('/floorplan/', methods=['POST', 'GET'])
def floorplan():
    msg=""

    if request.method == 'POST':
        pass
        # any form inputs will go here


    return render_template("floorplan.html", msg=msg)



if __name__ == '__main__':
    app.run(debug = True)

    con.close()
