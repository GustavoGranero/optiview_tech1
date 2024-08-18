import datetime

from flask_bcrypt import Bcrypt

from optview import app, db
from models.users import Users

bcrypt = Bcrypt(app)

def update_password(user, password):
    user.hash = get_hash(user.user_name, password)
    db.session.commit()

def get_hash(user_name, password):
    # TODO make provision for other hash types
    return bcrypt.generate_password_hash(password)

def get_authenticated_user(user_name_or_email, password):
    user = Users.get_one(user_name=user_name_or_email)
    if user is None:
        user = Users.get_one(email=user_name_or_email)  
        
    if user is not None and bcrypt.check_password_hash(user.hash, password):
        return user
    else:
        return None

def is_suspended(user_name_or_email):
    user = Users.get_one(user_name=user_name_or_email)
    if user is None:
        user = Users.get_one(email=user_name_or_email)

    if user is None:
        return False

    too_many_attemps = user.login_failure_count >= app.config['LOGIN_FAILED_ATTEMPTS_LIMIT']

    login_failure_timestamp = user.login_failure_timestamp
    if login_failure_timestamp is not None:
        suspension_elapsed_time = datetime.datetime.now(datetime.timezone.utc) -  login_failure_timestamp
        suspension_expired = suspension_elapsed_time.total_seconds() / 3600 >= app.config['LOGIN_SUSPENSION_TIME']
    else:
        suspension_expired = False

    return too_many_attemps and not suspension_expired
