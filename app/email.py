from flask_mail import Mail, Message
from flask import current_app
from threading import Thread

mail = Mail()

def send_async_email(app, msg):
    """Send email asynchronously."""
    with app.app_context():
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
