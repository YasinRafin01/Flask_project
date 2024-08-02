from flask import url_for
from itsdangerous import URLSafeTimedSerializer

s = URLSafeTimedSerializer('your-secret-key')

def send_reset_email(user):
    token = s.dumps(user.email, salt='password-reset-salt')
    reset_url = url_for('auth_bp.reset_password', token=token, _external=True)
    print(f'Password reset link: {reset_url}') 
    return reset_url