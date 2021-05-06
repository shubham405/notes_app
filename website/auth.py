from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User,Notes
from . import db
from flask_login import login_user,login_required,logout_user,current_user
#generating hash pasword
from werkzeug.security import generate_password_hash,check_password_hash
auth=Blueprint('auth',__name__)
@auth.route('/forget_password',methods=['GET','POST'])
def forget_password():
    if request.method=='POST':
        email=request.form.get('email')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        user=User.query.filter_by(email=email).first()
        if user is None:
            flash('User doesn\'t exist ',category='error')
        elif len(password1)<8:
            flash('Password is too weak',category='error')
        elif password1 !=password2:
            flash('Password did not matched',category='error')
        else:
            user.password=generate_password_hash(password1,method='sha256')
            flash('Password is updated',category='success')
            db.session.commit()
            return redirect(url_for('auth.login')) 
    return render_template('fgt_pass.html')

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        #checking if email exist in db
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Login Successful\t'+str(user.first_name),category='success')
                #this will remeber the fact that user have loged in 
                #unless they clear there browsing history or session 
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('email or password is incorrect, please try again',category='error')
        else:
            flash('email or password is incorrect, please try again',category='error')
    
    return render_template("login.html",user=current_user)
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been loged out ')
    return redirect(url_for('auth.login'))
@auth.route('/signup',methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        #fatching data using  name of that tag variable
        email=request.form.get('email')
        fname=request.form.get('firstName')
        lname=request.form.get('lastName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        #validation
        user=User.query.filter_by(email=email).first()
        if user:
            flash('User already exist',category='error')
        elif len(email)<4:
            flash('Error: Your email is too short',category='error')
        elif len(fname)<2:
            flash('Error: Your First Name is too short',category='error')
        elif len(lname)<2:
            flash('Error: Your Last Name is too short',category='error')
        elif password1 != password2:
            flash("Password doesn't match",category='error')
        elif len(password1)<7:
            flash('Your password is too weak',category='error')
        else:
            #add user to database
            new_user=User(email=email,first_name=fname,last_name=lname,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            #after signup user will automatically login
            #login_user(new_user, remember=True)
            flash('Acount Created Successfuly',category='success')
            return redirect(url_for('auth.login'))
            #views is views.py home is function inside it
    return render_template("signup.html",user=current_user)
