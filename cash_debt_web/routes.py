from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
from cash_debt_web import app
from cash_debt_web.models import User
from cash_debt_web.models import Debtor
from cash_debt_web import db
from cash_debt_web import login_manager
from flask_login import current_user, login_user, logout_user
from cash_debt_web.forms import LoginForm, RegisterForm


@app.route('/login', methods=['POST', 'GET'])
def login():    
    if current_user.is_authenticated is True:
        return redirect(url_for('index'))
    
    login_form = LoginForm()
    registration_form = RegisterForm()
    
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = User.query.filter_by(email=email).first()
        
        if user is None or not user.check_password(password):
            flash('Invalid password or user not found')
            return redirect(url_for('login'))        
        login_user(user)
        return redirect(url_for('index'))
    
    elif registration_form.validate_on_submit():
        email = registration_form.email.data
        password = registration_form.password.data
        
        check_user_exist = User.query.filter_by(email=email).first()
        if check_user_exist is not None:
            flash('User is exist')
            return redirect(url_for('login'))
        
        new_user = User(email=email)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            print("We've a new user!")
        except:
            print('There was an issue adding a new user :C')
        
        login_user(new_user)
        return redirect(url_for('index'))
    else:
        print(f"Registration: {registration_form.is_submitted()}\t Login: {login_form.is_submitted()}")
    return render_template("login.html", login_form=login_form, registration_form=registration_form)


@app.route('/index', methods=['POST', 'GET'])
def index():
    if current_user.is_authenticated is True:
        debtors = Debtor.query.filter_by(FK_user=current_user.id).all()
        return render_template('index.html', username=str(current_user.email), debtors=debtors ,errors=None)
    else:
        return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    """User loader needed for the login manager work. Returns id of the user"""
    return User.query.get(int(user_id))





@app.route('/signout')
def sign_out():
    logout_user()
    return redirect(url_for("login"))

@app.route('/reg', methods=['POST', 'GET'])
def registration():
    
    if request.method == 'POST':
        
        password = request.form.get('password')
        user_email = request.form.get('email')
        user = User.query.filter_by(email=user_email).first()
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
        #return render_template('registry.html')
        return redirect(url_for('login'))
    
    
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
    
    