from calendar import month
from telnetlib import STATUS
from unicodedata import name
from flask import Flask, render_template, request, redirect, url_for, session,flash, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
import urllib.request
from werkzeug.utils import secure_filename
  
  
app = Flask(__name__)
  
  
UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '8157'
app.config['MYSQL_DB'] = 'eventsconnect'
  
mysql = MySQL(app)




@app.route('/events', methods = ['POST', 'GET'])

def events():
    if request.method == 'GET':
        return "events "
     
    if request.method == 'POST':
        name = request.form['name']
        venue = request.form['venue']
        speaker = request.form['speaker']
        club = request.form['club']
        status= request.form['status']
        color = request.form['color']
        time = request.form['time']
        date = request.form['date']
        date1 = date.split("-")
        month=date1[1]
        day=date1[0]
        year=date1[2]

        prikey=date+time
        print(prikey)

        monthword="00"
        if month=="01":
           monthword="January"
        if month=="02":
           monthword="February"
        if month=="03":
           monthword="March"
        if month=="04":
           monthword="April"
        if month=="05":
           monthword="May"
        if month=="06":
           monthword="June"
        if month=="07":
           monthword="July"
        if month=="08":
           monthword="August"
        if month=="09":
           monthword="September"
        if month=="10":
           monthword="October"
        if month=="11":
           monthword="November"
        if month=="12":
           monthword="December"
           
      
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO events (club, name, date, day, month, year, monthword, time, venue, speaker, color, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (club, name, date,  day, month, year, monthword, time, venue, speaker, color, status))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('login'))


 
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'

            hai=user['name']
            c=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            c.execute("SELECT * FROM events where club='%s'"%hai)
            curcount=c.rowcount

            a=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            a.execute("SELECT * FROM events where status='approved'and club='%s'"%hai)
            counta=a.rowcount

            p=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            p.execute("SELECT * FROM events where status='pending'and club='%s'"%hai)
            countp=p.rowcount

            datecur = mysql.connection.cursor()
            datecur.execute("SELECT * FROM events")
            date = datecur.fetchall()


            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM events where club='%s'"%hai)
            data = cur.fetchall()
            cur.close()
            return render_template('hai.html', students=data, curcount=curcount,counta=counta, countp=countp,mesage = mesage,date=date )

           
            
         
          
            # return render_template('hai.html',students=data )


            

            # hai=user['name']
            # cur = mysql.connection.cursor()
            # cur.execute("SELECT * FROM events where club='%s'"%hai)
            # data = cur.fetchall()
            # cur.close()

            # club = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # club.execute("SELECT*from events ")
            # data= club.fetchall()
            # club.close()
            # return render_template('admin.html', data=data)
   
        else:
            mesage = 'Please enter correct email / password !'

    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from events ORDER BY month,day ASC")
    data=cursor.fetchall()
    return render_template("inter.html",data=data,mesage = mesage)
    # return render_template('inter.html', )










 

@app.route('/approved')
def approved():

    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from events where status='approved'")
    data=cursor.fetchall()
    return render_template("inter.html",data=data)
  
@app.route('/pending')
def pending():

    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from events where status='pending'")
    data=cursor.fetchall()
    return render_template("inter.html",data=data)
  






@app.route('/updated', methods =['GET', 'POST'])
def updated():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'

            global hai
            hai=user['name']
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM events where club='%s'"%hai)
    data = cur.fetchall()
    cur.close()
    return render_template('user.html', students=data )   
        




@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM events WHERE id=%s", (id_data,))
    mysql.connection.commit()
    
    cur1 = mysql.connection.cursor()
    cur1.execute("SELECT  * FROM events")
    data = cur1.fetchall()
    cur1.close()
    return render_template('user.html', students=data )


@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        time = request.form['time']
        venue = request.form['venue']
        speaker = request.form['speaker']
        status = request.form['status']


        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE events
               SET name=%s, time=%s, venue=%s, speaker=%s, status=%s
               WHERE id=%s
            """, (name,time, venue, speaker, status, id_data))
        flash("Data Updated Successfully")
      #   return redirect(url_for('updated'))
      #   mysql.connection.commit()
      #   cur2 = mysql.connection.cursor()
      #   cur2.execute("SELECT  * FROM events")
      #   data = cur2.fetchall()
      #   cur2.close()
      #   return render_template('home.html', students=data )
      
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from events ORDER BY month,day ASC")
    data=cursor.fetchall()
    return render_template("home.html",data=data)
    # return render_template('login.html', )



@app.route('/updatestatus',methods=['POST','GET'])
def updatestatus():

    if request.method == 'POST':
        id_data = request.form['id']
        status = request.form['status']


        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE events
               SET status=%s
               WHERE id=%s
            """, (status, id_data))
        flash("Data Updated Successfully")
   
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from events ORDER BY month,day ASC")
    data=cursor.fetchall()
    return render_template("admin.html",data=data)
    # return render_template('login.html', )












@app.route('/admin', methods =['GET', 'POST'])
def adminlogin():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'

            hai=user['name']
            c=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            c.execute("SELECT * FROM events where club='%s'"%hai)
            curcount=c.rowcount

            a=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            a.execute("SELECT * FROM events where status='approved'and club='%s'"%hai)
            counta=a.rowcount

            p=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            p.execute("SELECT * FROM events where status='pending'and club='%s'"%hai)
            countp=p.rowcount

            datecur = mysql.connection.cursor()
            datecur.execute("SELECT * FROM events")
            date = datecur.fetchall()


            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM events where club='%s'"%hai)
            data = cur.fetchall()
            cur.close()
            return render_template('admin.html', students=data, curcount=curcount,counta=counta, countp=countp,mesage = mesage,date=date )

    else:
         mesage = 'Please enter correct email / password !'

    return render_template("adminhome.html",mesage = mesage)
    # return render_template('login.html', )

         









  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))



@app.route('/test')
def test():
    return render_template("test.html")


  
@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'

    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from events ORDER BY month,day ASC")
    data=cursor.fetchall()
  
    return render_template("register.html",data=data,mesage = mesage)
    # return render_template('register.html', mesage = mesage)




@app.route('/adminregister', methods =['GET', 'POST'])
def adminregister():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO admin VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from user")
    data=cursor.fetchall()
    return render_template("adminregister.html",data=data,mesage = mesage)



# @app.route('/adminregister', methods =['GET', 'POST'])
# def adminregister():
#     mesage = ''
#     if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form and 'club' in request.form:
#         userName = request.form['name']
#         password = request.form['password']
#         email = request.form['email']
#         club = request.form['club']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM admin WHERE email = % s', (email, ))
#         account = cursor.fetchone()
#         if account:
#             mesage = 'Account already exists !'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             mesage = 'Invalid email address !'
#         elif not userName or not password or not email:
#             mesage = 'Please fill out the form !'
#         else:
#             cursor.execute('INSERT INTO admin VALUES (NULL, % s, % s, % s,% s)', (userName, email, password,club))
#             mysql.connection.commit()
#             mesage = 'You have successfully registered !'
#     elif request.method == 'POST':
#         mesage = 'Please fill out the form !'

#     cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("select * from user")
#     data=cursor.fetchall()
#     return render_template("adminregister.html",data=data,mesage = mesage)


    














# @app.route('/')
# def Index():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT  * FROM events")
#     data = cur.fetchall()
#     cur.close()
#     return render_template('user.html', students=data )




if __name__ == "__main__":
    app.run(debug=True)


