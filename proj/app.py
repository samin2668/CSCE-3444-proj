# From the project folder, open this Python file in a terminal window
# Then visit localhost:5000 in a web browser

from flask import * # Install Python and Flask on your local machine
from users import Registration, Login
import sqlite3
import hashlib



app = Flask(__name__, static_url_path='')

app.config['SECRET_KEY'] = '3bfcd4ebd54cb9f7896c76c7f2b6b1d1'

# Create database for user accounts and apartment units and anything else
con = sqlite3.connect('data.db', check_same_thread=False)


#Homepage
@app.route('/')
@app.route('/home')
def home():

    #msg = "Hello World!"
    return render_template('home.html') #,msg=msg)

#Apply section of webpage
@app.route('/apply')
def apply():
	form = Registration()
	return render_template('apply.html', form=form)


#Apply reg section of webpage
@app.route('/register')
def register():
	return render_template('reg.html')




if __name__ == '__main__':
    app.run(debug=True)

    con.close()
