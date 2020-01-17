from flask import render_template, request, redirect, url_for
from cash_debt_web import app

def check_user(request):
    email = request.form.get('email')
    password = request.form.get('password')
    
    founder_user = User.query.filter_by(email=email).first()
    check_pass = check_password_hash(founder_user.password, password)
    
    return {"pass_valid":check_pass, "user":founder_user}


@app.route('/login', methods=['POST', 'GET'])
def login():    
    if request.method == 'POST':
        if 'register' in request.form:
            return redirect('/reg')
        elif 'login' in request.form:
            user_valid = check_user(request)
            if user_valid['pass_valid']:
                return render_template('index.html', user=user_valid['user'])
            else:
                return  render_template('login.html', errors='Password is incorrect :C ')      
    else:
        return render_template('login.html')
    

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')
    
    
@app.route('/reg', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        password = request.form.get('password')
        hash_pass = generate_password_hash(password)
        user_email = request.form.get('email')
        new_user = User(email=user_email, password=hash_pass)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            print("We've a new user!")
        except:
            print('There was an issue adding a new user :C')
        
        return f'hello {user_email}'
    else:
        return render_template('registry.html')