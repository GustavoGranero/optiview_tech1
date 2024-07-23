from flask_bcrypt import Bcrypt

from optview import app, db
from models.users import Users

bcrypt = Bcrypt(app)

def update_password(user_name, password):
    user = Users.query.filter_by(user_name=user_name).first()
    user.hash = get_hash(user_name, password)
    db.session.commit()

def get_hash(user_name, password):
    # TODO make provision for other hash types
    return bcrypt.generate_password_hash(password)


def get_authenticated_user(user_name, password):
    user = Users.query.filter_by(user_name=user_name).first()
    try:
        if user is not None and bcrypt.check_password_hash(user.hash, password):
            return user
        else:
            return None
    except Exception as e:
        # TODO log error
        return None