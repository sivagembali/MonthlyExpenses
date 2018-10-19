from flask import Flask, request, render_template, session, make_response
from flask_sqlalchemy import SQLAlchemy
#import models as md
from datetime import datetime as dt

import json

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

@app.route('/expensesPage/')
def expensesPage():
    return render_template('expenses_show.html',user_name=session['username'])

@app.route('/expensesAddingPage/')
def expensesAddingPage():
    users_data = registerNew.query.all()
    return render_template('expenses_add.html', user_name=session['username'],users_data=users_data)

@app.route('/indexPage/')
def showIndex1():
    return render_template('index.html')

@app.route('/getExpensesData/',methods=['POST','GET'])
def getExpensesData():
    if(request.method=='POST'):
        from_date = dt.strptime(request.form['from_date'], "%Y-%m-%d").date()
        to_date = dt.strptime(request.form['to_date'], "%Y-%m-%d").date()
        exp_type = request.form['exp_type']
        if(exp_type=='All'):
            result_from_db = expenses.query.filter_by(user_id=session['username']).all()
        else:
            result_from_db = expenses.query.filter_by(user_id=session['username'], type=exp_type).all()
        #print(result_from_db,exp_type)
        expenses_list = []
        total_expenses = 0
        for record in result_from_db:
            if(record.date <= to_date and record.date >= from_date ):
                total_expenses += record.amount
                expenses_list.append(record)
        #print(expenses_dict)
        if(len(expenses_list)==0):
            return render_template('expenses_show.html',msg='No Records Available',user_name=session['username'])

        return render_template('expenses_show.html',user_exp_details=expenses_list,total_expenses=total_expenses,user_name = session['username'])
    return render_template('expenses_show.html',user_name=session['username'])

@app.route('/registerPage/')
def registerPage():
    return render_template('register_page.html')

@app.route('/loginPage/')
def loginPage():
    if ('username' in session):
        return render_template('home.html', user_name=session['username'])
    return render_template('login_page.html')

@app.route('/registerData/',methods=['POST','GET'])
def registerData():
    if(request.method=='POST'):
        uname = request.form['uname']
        username = request.form['username']
        uemail = request.form['uemail']
        umobile = request.form['unumber']
        upwd = request.form['upwd']
        username_check = registerNew.query.filter_by(user_id = username).all()
        email_check = registerNew.query.filter_by(email = uemail).all()
        mobile_check = registerNew.query.filter_by(mobile = umobile).all()
        if(len(username_check) == 1):
            return render_template('register_page.html', err_msg='Username Already Exist')
        elif(len(email_check) == 1):
            return render_template('register_page.html',err_msg='Email already Exist')
        elif(len(mobile_check)==1):
            return render_template('register_page.html', err_msg='Number already Exist')
        #print(name,email,mobile,pwd,gen)
        else:
            res = registerNew(user_id=username,name = uname,email=uemail ,mobile=umobile,password=upwd)
            db.session.add(res)
            db.session.commit()
            return render_template('index.html',success_msg='Register Successfully')
    return render_template('index.html')

@app.route('/storeExpensesData/',methods=['POST','GET'])
def storeExpensesData():
    if(request.method=='POST'):
        user_id = session['username']
        exp_type = request.form['exp_type']
        date = dt.strptime(request.form['date'], "%Y-%m-%d")
        amount = int(request.form['amount'])
        if(exp_type in ['Trip','Dinner','Hangout']):
            members = request.form.getlist('members')
            print('hello',members)
            if(members == []):
                members.append(session['username'])
            amount = amount/len(members)
            for member in members:
                if(len(expenses.query.all())==0):
                    ref = expenses(entry_no=1,user_id=member,date=date,amount=amount,type=exp_type)
                    db.session.add(ref)
                    db.session.commit()
                else:
                    ref = expenses(user_id=member, date=date, amount=amount, type=exp_type)
                    db.session.add(ref)
                    db.session.commit()
        else:
            if(len(expenses.query.all())==0):
                ref = expenses(entry_no=1,user_id=user_id,date=date,type=exp_type,amount=amount)
                db.session.add(ref)
                db.session.commit()
            else:
                ref = expenses(user_id=user_id,date=date,type=exp_type,amount=amount)
                db.session.add(ref)
                db.session.commit()
        users_data = registerNew.query.all()
        return render_template('expenses_add.html', user_name=session['username'],success_msg='Successfully Saved', users_data=users_data)
    users_data = registerNew.query.all()
    return render_template('expenses_add.html', user_name=session['username'], users_data=users_data)
#return loginPage(success_msg='Successfully Saved')

@app.route('/csv/',methods=['POST','GET'])
def download_csv():
    user_id = session['username']
    res = expenses.query.filter_by(user_id=user_id).all()
    csv = ''
    total = 0
    for x in res:
        csv = csv + x.date.strftime('%m-%d-%Y') + ',' + x.type + ',' + str(x.amount) + '\n'
        total = total + x.amount

    if(total==0):
        return render_template('expenses_show.html',user_name=session['username'],msg="You Don't have any Expenses")
    csv = 'All Expenses Details,'+user_id+'\n' + csv + ',Total ,' + str(total)
    response = make_response(csv)
    cd = 'attachment; filename='+ user_id +'.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'
    return response

@app.route('/allData/',methods=['POST','GET'])
def allData():
    register_data = registerNew.query.all()
    d1={}
    d2={}
    for x in register_data:
        d1[x.user_id] = {'username':x.name,'email':x.email,'mobile':x.mobile,'password':x.password}
    expenses_data = expenses.query.all()
    for x in expenses_data:
        d2[x.entry_no] = {'username':x.user_id,'type':x.type,'amount':x.amount,'date':str(x.date)}
    d={'register_data':d1,'expenses_data':d2}
    print(d)
    return json.dumps(d)

@app.route('/loginData/',methods=['POST','GET'])
def loginData():
    uname = request.form['uname']
    upwd = request.form['upwd']
    res = registerNew.query.filter_by(user_id = uname).all()
    if(len(res)==0):
        return render_template("login_page.html",err_msg='Invalid Username')
    elif(list(res)[0].password == upwd):
        session['username'] = uname
        return loginPage()
    else:
        return render_template('login_page.html',err_msg='Invalid Password')


#Classes for tables which uses ORM model
class registerNew(db.Model):
    user_id = db.Column(db.String(50),primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    mobile = db.Column(db.Integer)
    password = db.Column(db.String(50))


class expenses(db.Model):
    entry_no=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.String(50))
    date = db.Column(db.DATE)
    type = db.Column(db.String(50))
    amount = db.Column(db.Integer)

#db.create_all()


if __name__ == '__main__':
    app.run(debug=True)