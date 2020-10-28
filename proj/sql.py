import sqlite3

conn = sqlite3.connect(':memory:') #saves to memory to make debugging easier


cur = conn.cursor()



cur.execute("""CREATE TABLE USER(
   FIRST_NAME CHAR(20) NOT NULL,
   LAST_NAME CHAR(20),
   PHONE CHAR(20),
   EMAIL CHAR(30),
   PASSWORD CHAR(20)
)""")





def AddUser(firstname_form, lastname_form, phone_form, email_form, password_form):
	with conn:
		cur.execute("INSERT INTO USER VALUES (:FIRST_NAME, :LAST_NAME, :PHONE, :EMAIL, :PASSWORD)", {'FIRST_NAME': firstname_form, 'LAST_NAME': lastname_form, 'PHONE': phone_form, 'EMAIL': email_form, 'PASSWORD': password_form })

def DelUser(email_form):
	with conn:
		cur.execute("DELETE FROM USER WHERE EMAIL = :EMAIL)", {'EMAIL': email_form})

def GetUserByEmail(email_form):
	cur.execute("SELECT rowid, * FROM USER WHERE EMAIL =:EMAIL", {'EMAIL': email_form})
	return cur.fetchall()




AddUser('Sedek', 'Ciprien', '1234567890', 'tigers@gmail.com', 'hashedpassword')
AddUser('Salem', 'Ciprien', '5555555555', 'lions@gmail.com', 'hashedpassword2')

person = GetUserByEmail('tigers@gmail.com')
print(person)


conn.close()
