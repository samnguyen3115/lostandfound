from flask_mail import Message
from flask import current_app
from threading import Thread

def send_async_email(app, msg):
    """Send email asynchronously."""
    with app.app_context():
        from app import mail
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body=None):
    """Send email notification."""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    if html_body:
        msg.html = html_body
    
    # Send asynchronously
    Thread(target=send_async_email, 
           args=(current_app._get_current_object(), msg)).start()

def send_found_item_notification(post, finder_email):
    """Notify post owner that their item may have been found."""
    if not post.writer.email:
        return
    
    subject = f"Someone may have found your lost item: {post.title}"
    text_body = f"""
    Hi {post.writer.username},

    Good news! Someone may have found your lost item "{post.title}".
    
    Contact details: {finder_email}
    
    Item description: {post.description}
    
    Please contact them directly to verify and arrange pickup.
    
    Best regards,
    Lost and Found Team
    """
    
    send_email(subject, 
               current_app.config['MAIL_DEFAULT_SENDER'],
               [post.writer.email],
               text_body)

def send_verification_code(user):
    """Send email verification code to user."""
    if not user.email or not user.verification_code:
        return
    
    subject = "Verify Your Email - Lost and Found"
    text_body = f"""
    Hi {user.username},
    
    Welcome to Lost and Found! Please verify your email address by entering this 5-digit code:
    
    {user.verification_code}
    
    This code will expire in 15 minutes.
    
    If you didn't create an account, please ignore this email.
    
    Best regards,
    Lost and Found Team
    """
    
    html_body = f"""
    <html>
        <body>
            <h2>Welcome to Lost and Found!</h2>
            <p>Hi {user.username},</p>
            <p>Please verify your email address by entering this verification code:</p>
            <div style="font-size: 24px; font-weight: bold; color: #007bff; text-align: center; padding: 20px; background-color: #f8f9fa; border: 2px dashed #007bff; margin: 20px 0;">
                {user.verification_code}
            </div>
            <p><strong>This code will expire in 15 minutes.</strong></p>
            <p>If you didn't create an account, please ignore this email.</p>
            <br>
            <p>Best regards,<br>Lost and Found Team</p>
        </body>
    </html>
    """
    
    send_email(subject, 
               current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@lostandfound.com'),
               [user.email],
               text_body,
               html_body)
