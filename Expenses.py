from flask import Flask,request,render_template,session
from flask_sqlalchemy import SQLAlchemy
import models as md
from datetime import datetime as dt
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "cdkddkdkdkdkdhdhdhd"
db = SQLAlchemy(app)

@app.route('/logout/')
def logout():
    session.pop('username', None)
    return render_template('index.html',success_msg='Successfully Logout')

@app.route('/')
def showIndex():
    if('username' in session):
        return loginPage()
    return render_template('index.html')

@app.route('/home/')
def showIndex1():
    return render_template('index.html')

@app.route('/registerPage/')
def registerPage():
    return render_template('register_page.html')

@app.route('/loginPage/')
def loginPage(success_msg=None):
    if ('username' in session):
        users_data = md.registerNew.query.all()
        return render_template('home.html', user_name=session['username'],users_data=users_data,success_msg=success_msg)
    return render_template('login_page.html')

@app.route('/registerData/',methods=['POST','GET'])
def registerData():
    if(request.method=='POST'):
        uname = request.form['uname']
        username = request.form['username']
        uemail = request.form['uemail']
        umobile = request.form['unumber']
        upwd = request.form['upwd']
        username_check = md.registerNew.query.filter_by(user_id = username).all()
        email_check = md.registerNew.query.filter_by(email = uemail).all()
        mobile_check = md.registerNew.query.filter_by(mobile = umobile).all()
        if(len(username_check) == 1):
            return render_template('register_page.html', err_msg='Username Already Exist')
        elif(len(email_check) == 1):
            return render_template('register_page.html',err_msg='Email already Exist')
        elif(len(mobile_check)==1):
            return render_template('register_page.html', err_msg='Number already Exist')
        #print(name,email,mobile,pwd,gen)
        else:
            res = md.registerNew(user_id=username,name = uname,email=uemail ,mobile=umobile,password=upwd)
            db.session.add(res)
            db.session.commit()
            return render_template('index.html',success_msg='Register Successfully')
    return render_template('index.html')

@app.route('/storeExpensesData/',methods=['POST','GET'])
def storeExpensesData():
    user_id = session['username']
    exp_type = request.form['exp_type']
    date = dt.strptime(request.form['date'], "%Y-%m-%d")
    amount = int(request.form['amount'])
    if(exp_type in ['trip','dinner','hangout']):
        members = request.form.getlist('members')
        print(members)
        if(members == []):
            members.append(session['username'])
        amount = amount/len(members)
        for member in members:
            if(len(md.expenses.query.all())==0):
                ref = md.expenses(entry_no=1,user_id=member,date=date,amount=amount,type=exp_type)
                db.session.add(ref)
                db.session.commit()
            else:
                ref = md.expenses(user_id=member, date=date, amount=amount, type=exp_type)
                db.session.add(ref)
                db.session.commit()
    else:
        if(len(md.expenses.query.all())==0):
            ref = md.expenses(entry_no=1,user_id=user_id,date=date,type=exp_type,amount=amount)
            db.session.add(ref)
            db.session.commit()
        else:
            ref = md.expenses(user_id=user_id,date=date,type=exp_type,amount=amount)
            db.session.add(ref)
            db.session.commit()
    return loginPage(success_msg='Successfully Saved')


@app.route('/loginData/',methods=['POST','GET'])
def loginData():
    uname = request.form['uname']
    upwd = request.form['upwd']
    res = md.registerNew.query.filter_by(user_id = uname).all()
    if(len(res)==0):
        return render_template("login_page.html",err_msg='Invalid Username')
    elif(list(res)[0].password == upwd):
        session['username'] = uname
        return loginPage()
    else:
        return render_template('login_page.html',err_msg='Invalid Password')

if __name__ == '__main__':
    app.run(debug=True)
