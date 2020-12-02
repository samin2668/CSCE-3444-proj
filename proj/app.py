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


# Create a users and floorplan table in the database
cur = con.cursor()

cur.execute(''' CREATE TABLE IF NOT EXISTS Users (
 	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "firstname" TEXT NOT NULL,
    "lastname" TEXT NOT NULL,
    "phone" TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
    "unit #" INTERGER UNIQUE
);
''')

# Create a FloorPlan table and create units if they do not yet exist
cur.execute(''' CREATE TABLE IF NOT EXISTS FloorPlan (
    "unit_num"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "price" INTEGER NOT NULL,
    "currentUser" TEXT,
    "layout" TEXT NOT NULL,
    "bedrooms" INTEGER NOT NULL,
    "bathrooms" INTEGER NOT NULL,
    "livingroom" BOOLEAN NOT NULL,
    "pool"	BOOLEAN NOT NULL
);
''')

cur.execute("SELECT * FROM FloorPlan")
if not cur.fetchone():
    print("not populated")

    # Create the apartment units in the FloorPlan table
    for i in range(0,10):
        price = 1200
        layout = "Large"
        beds = 2
        baths = 2
        cur.execute("INSERT INTO FloorPlan (price, layout, bedrooms, bathrooms, livingroom, pool) VALUES (?, ?, ?, ?, ?, ?)", (price, layout, beds, baths, True, True))

    for i in range(0,10):
        price = 900
        layout = "Medium"
        beds = 1
        baths = 1
        cur.execute("INSERT INTO FloorPlan (price, layout, bedrooms, bathrooms, livingroom, pool) VALUES (?, ?, ?, ?, ?, ?)", (price, layout, beds, baths, True, True))
    for i in range(0,10):
        price = 700
        layout = "Small"
        beds = 0
        baths = 1
        cur.execute("INSERT INTO FloorPlan (price, layout, bedrooms, bathrooms, livingroom, pool) VALUES (?, ?, ?, ?, ?, ?)", (price, layout, beds, baths, True, True))



con.commit()





#SQL Funtions
def AddUser(firstname_form, lastname_form, phone_form, email_form, password_form):
    with con:
        #cur.execute('''INSERT INTO Users (firstname, lastname, phone, email, password) VALUES (?, ?, ?, ?, ?)''', (firstname_form, lastname_form, phone_form, email_form, password_form))
        cur.execute("INSERT INTO Users (firstname, lastname, phone, email, password) VALUES (?, ?, ?, ?, ?)", (firstname_form, lastname_form, phone_form, email_form, password_form ))

def DeleteUser(email_form):
    with con:
        cur.execute("DELETE FROM Users WHERE EMAIL = (?)", (email_form))

def GetUserByEmail(email_form):
    cur.execute("SELECT rowid, * FROM Users WHERE EMAIL = (?)", (email_form))
    return cur.fetchall()

def AssignFloorPlanToUser(user_email_form, layout_form, bed_form, bath,form, livingroom_bool, pool_bool):
    with con:
        cur.execute("INSERT INTO FloorPlan (currentUser, layout, bedrooms, bathrooms, livingroom, pool) VALUES (?, ?, ?, ?, ?, ?)", (user_email_form, layout_form, bed_form, bath_form, livingroom_bool, pool_bool))

def GetUsersFloorPlan(user_email_form):
    cur.execute("SELECT rowid, * FROM FloorPlan WHERE EMAIL = (?)", (user_email_form))
    return cur.fetchall()







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
            AddUser(fn_enter, ln_enter, phone_enter, em_enter, pw_enter_hash)
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
                session['user_unit'] = 0

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
    session['loggedin'] = False
    session.pop('user_email', None)
    session.pop('user_unit', None)
    session.clear()

    # Return to the home page
    return redirect(url_for('home'))


@app.route('/user_home/', methods=['POST', 'GET'])
def user_home():

    if request.method == 'POST':
        pass
        # any form inputs will go here

    return render_template("user_home.html", user_name=session['user_email'])


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

    # Show all available units
    cur.execute("SELECT * FROM FloorPlan")
    con.commit()

    units = cur.fetchall()



    return render_template("floorplan.html", availUnits=units)


@app.route('/select/', methods=['POST', 'GET'])
def select():
    msg=""

    if request.method == 'POST':
        unit_enter = request.form['selected']
        pay_enter = request.form['pay']

        session['user_unit'] = str(unit_enter)

        print("User selected unit number " + unit_enter + " with " + pay_enter + " payment method")


    #return render_template("user_home.html", user_name=session['user_email'], user_unit=session['user_unit'], msg=msg)
    return redirect(url_for('user_home'))


if __name__ == '__main__':
    app.run(debug = True)

    con.close()
