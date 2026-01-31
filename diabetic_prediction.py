source code
from flask import Flask, render_template, flash, request, session
from flask import render_template, redirect, url_for, request
#from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
#from werkzeug.utils import secure_filename
importmysql.connector
importsmtplib
#from PIL import Image
import pickle
importnumpy as np
# Load the Random Forest CLassifier model
filename = 'diabetes-prediction-rfc-model.pkl'
classifier = pickle.load(open(filename, 'rb'))
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['DEBUG']
@app.route("/")
def homepage():
returnrender_template('index.html')
@app.route("/Home")
def Home():
returnrender_template('index.html')
@app.route("/AdminLogin")
defAdminLogin():
returnrender_template('AdminLogin.html')
@app.route("/NewUser")
defNewUser():
returnrender_template('NewUser.html')
@app.route("/UserLogin")
defUserLogin():
returnrender_template('UserLogin.html')
@app.route("/UserHome")
defUserHome():
returnrender_template('UserHome.html')
@app.route("/AdminHome")
defAdminHome():
returnrender_template('AdminHome.html')

@app.route("/NewQuery1")
def NewQuery1():
returnrender_template('NewQueryReg.html')
@app.route("/adminlogin", methods=['GET', 'POST'])
defadminlogin():
error = None
ifrequest.method == 'POST':
ifrequest.form['uname'] == 'admin' or request.form['password'] == 'admin':
conn = mysql.connector.connect(user='root', password='', host='localhost', database='1diabetesdb')
cursor = conn.cursor()
cur = conn.cursor()
cur.execute("SELECT * FROM register")
data = cur.fetchall()
returnrender_template('AdminHome.html', data=data)

else:
returnrender_template('index.html', error=error)


@app.route("/reg", methods=['GET', 'POST'])
defreg():
ifrequest.method == 'POST':
        n = request.form['name']

address = request.form['address']
age = request.form['age']
pnumber = request.form['phone']
email = request.form['email']
zip = request.form['zip']
uname = request.form['uname']
password = request.form['psw']
conn = mysql.connector.connect(user='root', password='', host='localhost', database='1diabetesdb')
cursor = conn.cursor()
cursor.execute(
            "INSERT INTO register VALUES ('','" + n + "','" + age + "','" + email + "','" + pnumber + "','" + zip + "','" + address + "','" + uname + "','" + password + "')")
conn.commit()
conn.close()
        # return 'file register successfully'
returnrender_template('UserLogin.html')

@app.route("/userlogin", methods=['GET', 'POST'])
defuserlogin():
error = None
ifrequest.method == 'POST':
username = request.form['uname']
password = request.form['password']
session['uname'] = request.form['uname']

conn = mysql.connector.connect(user='root', password='', host='localhost', database='1diabetesdb')
cursor = conn.cursor()
cursor.execute("SELECT * from register where uname='" + username + "' and psw='" + password + "'")
data = cursor.fetchone()
if data is None:
returnrender_template('index.html')
return 'Username or Password is wrong'
else:
print(data[0])
session['uid'] = data[0]
conn = mysql.connector.connect(user='root', password='', host='localhost', database='1diabetesdb')
            # cursor = conn.cursor()
cur = conn.cursor()
cur.execute("SELECT * FROM register where uname='" + username + "' and psw='" + password + "'")
data = cur.fetchall()

returnrender_template('UserHome.html', data=data )

@app.route("/newquery", methods=['GET', 'POST'])
defnewquery():
ifrequest.method == 'POST':
uname = session['uname']
preg = request.form['pregnancies']
glucose = request.form['glucose']
bp = request.form['bloodpressure']
st = request.form['skinthickness']
insulin = request.form['insulin']
bmi = request.form['bmi']
dpf = request.form['dpf']
age = request.form['age']



conn = mysql.connector.connect(user='root', password='', host='localhost', database='1diabetesdb')
cursor = conn.cursor()
cursor.execute(
            "INSERT INTO Querytb VALUES ('','" + uname + "','" + preg + "','" + glucose + "','" + bp + "','"+st+"','"+insulin +"','"+ bmi
            +"','"+ dpf +"','"+ age +"','waiting','')")
conn.commit()
conn.close()
        # return 'file register successfully'
conn = mysql.connector.connect(user='root', password='', host='localhost', database='1diabetesdb')
        # cursor = conn.cursor()
cur = conn.cursor()
cur.execute("SELECT * FROM Querytb where UserName='" + uname + "' and DResult='waiting '")
data = cur.fetchall()
returnrender_template('UserQueryInfo.html', data=data)


@app.route("/UQueryandAns")
defUQueryandAns():

uname = session['uname']

conn = mysql.connector.connect(user='root', password='', host='localhost', database='1diabetesdb')
    # cursor = conn.cursor()
cur = conn.cursor()
cur.execute("SELECT * FROM Querytb where UserName='" + uname + "' and DResult='waiting'")
data = cur.fetchall()

conn = mysql.connector.connect(user='root', password='', host='localhost', database='1diabetesdb')
    # cursor = conn.cursor()
cur = conn.cursor()
cur.execute("SELECT * FROM Querytb where UserName='" + uname + "' and DResult !='waiting'")
    data1 = cur.fetchall()


returnrender_template('UserQueryAnswerinfo.html', wait=data, answ=data1 )

@app.route("/AdminQinfo")
defAdminQinfo():

    #uname = session['uname']

conn = mysql.connector.connect(user='root', password='', host='localhost', database='1diabetesdb')
    # cursor = conn.cursor()
cur = conn.cursor()
cur.execute("SELECT * FROM Querytb where  DResult='waiting'")
data = cur.fetchall()


returnrender_template('AdminQueryInfo.html', data=data )


@app.route("/answer")
def answer():

    Answer = ''
    Prescription=''
id =  request.args.get('lid')
conn = mysql.connector.connect(user='root', password='', host='localhost', database='1diabetesdb')
cursor = conn.cursor()
cursor.execute("SELECT  *  FROM Querytb where  id='" + id + "'")
data = cursor.fetchone()
if data:
UserName = data[1]
pregnancies = data[2]
glucose = data[3]
bloodpressure = data[4]
skinthickness = data[5]
insulin = data[6]
bmi = data[7]
dpf = data[8]
age = data[9]
else:
return 'Incorrect username / password !'
preg = int(pregnancies)
glucose = int(glucose)
bp = int(bloodpressure)
st = int(skinthickness)
insulin = int(insulin)
bmi = float(bmi)
dpf = float(dpf)
age = int(age)
data = np.array([[preg, glucose, bp, st, insulin, bmi, dpf, age]])
my_prediction = classifier.predict(data)
ifmy_prediction == 1:
        Answer = 'Diabetic'
if(glucose <= 120):
            Answer = 'Type1- Diabetic'
            Prescription='Managing Glucose in T1D Once Had But One Treatment'
else:
            Answer = 'Type2- Diabetic'
            Prescription='Medications Names:Repaglinide(Prandin)Nateglinide (Starlix)'
msg = 'Hello:According to our Calculations, You have DIABETES'
print('Hello:According to our Calculations, You have DIABETES')
else:
        Answer = 'No-Diabetic'
msg = 'Congratulations!!  You DON T have diabetes'
print('Congratulations!! You DON T have diabetes')
        Prescription='Nill'
conn = mysql.connector.connect(user='root', password='', host='localhost', database='1diabetesdb')
cursor = conn.cursor()
cursor.execute(
        "update Querytb set DResult='"+Answer+"', Prescription='" + Prescription +"'  where id='" + str(id) + "' ")
conn.commit()
conn.close()
conn3 = mysql.connector.connect(user='root', password='', host='localhost', database='1diabetesdb')
    cur3 = conn3.cursor()
cur3.execute("SELECT * FROM register where     uname='" + str(UserName) + "'")
    data3 = cur3.fetchone()
if data3:
phnumber = data3[4]
print(phnumber)
        #sendmsg(phnumber, msg)
    # return 'file register successfully'
conn = mysql.connector.connect(user='root', password='', host='localhost', database='1diabetesdb')
    # cursor = conn.cursor()
cur = conn.cursor()
cur.execute("SELECT * FROM Querytb where  DResult !='waiting '")
data = cur.fetchall()
returnrender_template('AdminAnswer.html', data=data)
@app.route("/AdminAinfo")
defAdminAinfo():
conn = mysql.connector.connect(user='root', password='', host='localhost', database='1diabetesdb')
    # cursor = conn.cursor()
cur = conn.cursor()
cur.execute("SELECT * FROM Querytb where  status !='waiting'")
data = cur.fetchall()
returnrender_template('AdminAnswer.html', data=data )
defsendmsg(targetno,message ):
import requests  requests.post("http://smsserver9.creativepoint.in/api.php?username=fantasy&password=596692&to=" + targetno + "&from=FSSMSS&message=Dear user  your msg is " + message + " Sent By FSMSG FSSMSS&PEID=1501563800000030506&templateid=1507162882948811640")
if __name__ == '__main__':
app.run(debug=True, use_reloader=True)
