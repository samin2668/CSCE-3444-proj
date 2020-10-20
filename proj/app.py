# From the project folder, open this Python file in a terminal window
# Then visit localhost:5000 in a web browser

from flask import * # Install Python and Flask on your local machine
import sqlite3
import hashlib



app = Flask(__name__, static_url_path='')


# Create database for user accounts and apartment units and anything else
con = sqlite3.connect('data.db', check_same_thread=False)


#Homepage
@app.route('/')
@app.route('/home')
def home():

    #msg = "Hello World!"
    return render_template('index.html') #,msg=msg)

#Apply section of webpage
@app.route('/apply')
def apply():
	return render_template('apply.html')

if __name__ == '__main__':
    app.run()

    con.close()
