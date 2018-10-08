from flask import Flask,request,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
import models as md
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "cdkddkdkdkdkdhdhdhd"
db = SQLAlchemy(app)

@app.route('/')
def showIndex():
    return render_template('index.html')

@app.route('/registerPage/')
def registerPage():
    return render_template('register_page.html')
@app.route('/loginPage/')
def loginPage():
    return render_template('login_page.html')

@app.route('/registerData/',methods=['POST','GET'])
def registerData():
    uname = request.form['uname']
    uemail = request.form['uemail']
    umobile = request.form['unumber']
    ugen = request.form['ugender']
    upwd = request.form['upwd']
    email_check = md.registerNew.query.filter_by(email = uemail).all()
    mobile_check = md.registerNew.query.filter_by(mobile = umobile).all()
    if(len(email_check) == 1):
        return render_template('register_page.html',err_msg='Email already Exist')
    elif(len(mobile_check)==1):
        return render_template('register_page.html', err_msg='Number already Exist')
    #print(name,email,mobile,pwd,gen)
    else:
        res = md.registerNew(name = uname,email=uemail ,mobile=umobile,gender=ugen,password=upwd)
        db.session.add(res)
        db.session.commit()
        return render_template('index.html',success_msg='Register Successfully')

@app.route('/loginData/',methods=['POST','GET'])
def loginData():
    uname = request.form['uname']
    upwd = request.form['upwd']
    #print(uname,upwd)
    if(len(uname)==10 and ('@' not in list(uname))):
        res = md.registerNew.query.filter_by(mobile = int(uname)).all()
    else:
        res = md.registerNew.query.filter_by(email = uname).all()
    for x in res:
        if(x.password == upwd):
            return render_template('home.html')
    return render_template('login_page.html',err_msg='Invalid Credentials')

if __name__ == '__main__':
    app.run(debug=True)
