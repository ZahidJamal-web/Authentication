from django.core.mail import send_mail
from django.conf import settings
import secrets

def generate_token():
    return secrets.token_urlsafe(16)

def send_verification_email(user_email, user_first_name, token):
    subject = "Email Verification"
    confirmation_url = f"http://localhost:8000/confirm_email/{token}/"  # Update to your domain
    message = f"""
    Hello {user_first_name},

    Please confirm your email address by clicking the link below:
    {confirmation_url}

    Thank you!
    """
    from_email = settings.EMAIL_HOST_USER
    try:
        send_mail(subject, message, from_email, [user_email], fail_silently=False)
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")  # Raise exception for error handling in views
