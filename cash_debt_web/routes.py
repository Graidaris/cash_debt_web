from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash
from cash_debt_web import app
from cash_debt_web.models import User
from cash_debt_web.models import Debtor
from cash_debt_web import db


@app.route('/login', methods=['POST', 'GET'])
def login():    
    if request.method == 'POST':
        what_return = None
        if 'register' in request.form:
            what_return = redirect('/reg')
        elif 'login' in request.form:
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            
            if user is not None:
                password_is_correct = user.check_password(password)
                if password_is_correct:
                    session['CURRENT_USER'] = user.id
                    what_return = redirect(url_for('index'))
                else:
                    what_return =  render_template('login.html', errors=f'Password is not correct') 
            else:
                what_return = render_template('login.html', errors=f'The user is not found')
    else:
        what_return = render_template('login.html')
        
    return what_return
    

@app.route('/', methods=['POST', 'GET'])
def index():
    user_id = session.get('CURRENT_USER')
    if user_id is not None:
        user = User.query.filter_by(id=user_id).first()
        debtors = Debtor.query.filter_by(FK_user=user_id).all()
        return render_template('index.html', username=user, debtors=debtors ,errors=None)
    else:
        return redirect(url_for('login'))

@app.route('/signout')
def sign_out():
    session.pop("CURRENT_USER", None)    
    return redirect(url_for("login"))

@app.route('/reg', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        password = request.form.get('password')
        user_email = request.form.get('email')
        
        if User.query.filter_by(email=user_email).first() is not None:
            return render_template('registry.html', errors="This email already exist")
        
        new_user = User(email=user_email, password=password)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            print("We've a new user!")
        except:
            print('There was an issue adding a new user :C')
        
        return redirect(url_for('index'))
    else:
        return render_template('registry.html')
    
    
@app.route('/add_debt', methods=['POST', 'GET'])
def add_debt():
    if request.method == "POST":
        name = request.form.get('name')
        money = request.form.get('money')
        description = request.form.get('description')
        FK_user = session['CURRENT_USER']
        
        new_debter = Debtor(name=name, money=money, description=description, FK_user=FK_user)
        errors = None
        try:
            db.session.add(new_debter)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            errors = e
        
        return render_template("add_debtor.html", error=errors)
        
    else:
        return render_template("add_debtor.html")
    
@app.route('/del_debt/<int:id>')
def delete_debt(id):
    debt_to_delete = Debtor.query.filter_by(id=id).first()
    user_id = session.get('CURRENT_USER')##
    
    if debt_to_delete.FK_user != user_id:
        return redirect(url_for('index'))##
    
    try:
        db.session.delete(debt_to_delete)
        db.session.commit()        
    except:
        pass
    
    return redirect(url_for('index'))

@app.route('/edit_debt/<int:id>', methods=['POST', 'GET'])
def edit_debt(id):
    debt_to_edit = Debtor.query.filter_by(id=id).first()
    
    user_id = session.get('CURRENT_USER')###
    
    if debt_to_edit.FK_user != user_id:
        return redirect(url_for('index'))##
    
    if request.method =='POST':
        name = request.form.get('name')
        money = request.form.get('money')
        description = request.form.get('description')
        
        debt_to_edit.name = name
        debt_to_edit.money = money
        debt_to_edit.description = description
        
        try:
            db.session.commit()
        except:
            return render_template('edit_debt.html', error="Edit failure")
        return redirect(url_for('index'))
    else:
        return render_template('edit_debt.html', debtor=debt_to_edit)
    
    