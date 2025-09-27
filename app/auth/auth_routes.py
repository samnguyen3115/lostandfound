
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user
from app import db
from app.auth import auth_blueprint as bp_auth 
from app.auth.auth_forms import RegistrationForm, LoginForm, EmailVerificationForm, ResendCodeForm
import sqlalchemy as sqla
from app.main.models import User
from app.email import send_verification_code
from datetime import datetime, timezone

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
            
            # Generate verification code
            verification_code = user.generate_verification_code()
            print(f"DEBUG: Generated verification code for {user.email}: {verification_code}")
            
            db.session.add(user)
            db.session.commit()
            
            # Send verification email
            send_verification_code(user)
            print(f"DEBUG: Verification email sent to {user.email}")
            
            # Store user ID in session for verification
            session['pending_user_id'] = user.id
            
            flash(f"Registration successful! We've sent a 5-digit verification code to {user.email}. Please check your email and enter the code to complete registration.", "info")
            return redirect(url_for('auth.verify_email'))
            
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
            query = sqla.select(User).where(User.email == lform.email.data)
            user = db.session.scalars(query).first()
            
            if user is None or not user.check_password(lform.password.data):
                flash('Invalid email or password', 'error')
                return redirect(url_for('auth.login'))
            
            # Check if email is verified
            if not user.email_verified:
                session['pending_user_id'] = user.id
                flash('Please verify your email address before logging in.', 'warning')
                return redirect(url_for('auth.verify_email'))
            
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

@bp_auth.route('/user/verify-email', methods=['GET', 'POST'])
def verify_email():
    """Email verification page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Check if user has a pending verification
    pending_user_id = session.get('pending_user_id')
    if not pending_user_id:
        flash('No pending email verification found.', 'error')
        return redirect(url_for('auth.register'))
    
    user = db.session.get(User, pending_user_id)
    if not user:
        flash('User not found.', 'error')
        session.pop('pending_user_id', None)
        return redirect(url_for('auth.register'))
    
    if user.email_verified:
        flash('Email already verified! You can now log in.', 'success')
        session.pop('pending_user_id', None)
        return redirect(url_for('auth.login'))
    
    form = EmailVerificationForm()
    resend_form = ResendCodeForm()
    
    if form.validate_on_submit():
        try:
            print(f"DEBUG: User attempting to verify with code: '{form.verification_code.data}'")
            print(f"DEBUG: User stored code: '{user.verification_code}'")
            print(f"DEBUG: Code expires at: {user.verification_code_expires}")
            print(f"DEBUG: Current time: {datetime.now(timezone.utc)}")
            
            if user.verify_email_code(form.verification_code.data):
                db.session.commit()
                session.pop('pending_user_id', None)
                print(f"DEBUG: Email verification successful for {user.email}")
                flash('Email verified successfully! You can now log in.', 'success')
                return redirect(url_for('auth.login'))
            else:
                print(f"DEBUG: Email verification failed for {user.email}")
                flash('Invalid or expired verification code. Please try again.', 'error')
        except Exception as e:
            db.session.rollback()
            print(f"DEBUG: Exception during verification: {e}")
            flash('Verification failed. Please try again.', 'error')
    
    return render_template('email_verification.html', form=form, resend_form=resend_form, user_email=user.email)

@bp_auth.route('/user/resend-verification', methods=['POST'])
def resend_verification():
    """Resend verification code."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    pending_user_id = session.get('pending_user_id')
    if not pending_user_id:
        flash('No pending email verification found.', 'error')
        return redirect(url_for('auth.register'))
    
    user = db.session.get(User, pending_user_id)
    if not user:
        flash('User not found.', 'error')
        session.pop('pending_user_id', None)
        return redirect(url_for('auth.register'))
    
    if user.email_verified:
        flash('Email already verified! You can now log in.', 'success')
        session.pop('pending_user_id', None)
        return redirect(url_for('auth.login'))
    
    try:
        # Generate new verification code
        verification_code = user.generate_verification_code()
        print(f"DEBUG: Resent verification code for {user.email}: {verification_code}")
        db.session.commit()
        
        # Send new verification email
        send_verification_code(user)
        print(f"DEBUG: Resent verification email to {user.email}")
        
        flash('New verification code sent! Please check your email.', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Failed to send verification code. Please try again.', 'error')
    
    return redirect(url_for('auth.verify_email'))