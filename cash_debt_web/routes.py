from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash
from cash_debt_web import app, db, login_manager
from cash_debt_web.models import User
from cash_debt_web.models import Debtor
from flask_login import login_user, logout_user, current_user, login_required


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST', 'GET'])
def login():    
    if request.method == 'POST':
        what_return = None
        if 'register' in request.form:
            what_return = registration()
            
        elif 'login' in request.form:            
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            
            if user is not None:
                password_is_correct = user.check_password(password)
                if password_is_correct:
                    login_user(user)
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
    if current_user.is_authenticated:
        if 'add_debtor' in request.form:
            add_debt()
        debtors = Debtor.query.filter_by(FK_user=current_user.id).all()
        return render_template('index.html', username=current_user, debtors=debtors ,errors=None)
    else:
        return redirect(url_for('login'))

@app.route('/signout')
@login_required
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
        login_user(new_user)
        return redirect(url_for('index'))
    
    else:
        return redirect(url_for('login'))
    
    

def add_debt():    
    name = request.form.get('name')
    money = request.form.get('money')
    description = request.form.get('description')
    FK_user = current_user
    
    new_debter = Debtor(name=name, money=money, description=description, FK_user=FK_user.id)
    errors = None
    try:
        db.session.add(new_debter)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        errors = e
        
    
@app.route('/del_debt/<int:id>')
@login_required
def delete_debt(id):
    debt_to_delete = Debtor.query.filter_by(id=id).first()
    user_id = current_user.id
    
    if debt_to_delete.FK_user != user_id:
        return redirect(url_for('index'))
    
    try:
        db.session.delete(debt_to_delete)
        db.session.commit()        
    except:
        pass
    
    return redirect(url_for('index'))

@app.route('/edit_debt/<int:id>', methods=['POST', 'GET'])
@login_required
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
    