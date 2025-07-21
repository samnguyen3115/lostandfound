
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app import db
from app.auth import auth_blueprint as bp_auth 
from app.auth.auth_forms import RegistrationForm, LoginForm
import sqlalchemy as sqla
from app.main.models import User

@bp_auth.route('/user/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    rform = RegistrationForm()
    if rform.validate_on_submit():
        try:
            user = User(
                username=rform.username.data,
                email=rform.email.data
            )
            user.set_password(rform.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Congratulations, you are now registered!", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash("Registration failed. Please try again.", "error")

    return render_template('register.html', form=rform)

@bp_auth.route('/user/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    lform = LoginForm()
    if lform.validate_on_submit():
        try:
            query = sqla.select(User).where(User.username == lform.username.data)
            user = db.session.scalars(query).first()
            
            if user is None or not user.check_password(lform.password.data):
                flash('Invalid username or password', 'error')
                return redirect(url_for('auth.login'))
            
            login_user(user, remember=lform.remember_me.data)
            flash(f'Welcome back, {user.username}!', "success")
            
            # Redirect to next page if provided
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('main.index'))
            
        except Exception as e:
            flash('Login failed. Please try again.', 'error')

    return render_template('login.html', form=lform)

@bp_auth.route('/user/logout', methods=['GET'])
def logout():
    """User logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))