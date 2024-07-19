from flask_bcrypt import Bcrypt

from optview import app, db
from models.users import Users

bcrypt = Bcrypt(app)

def update_password(user_name, password):
    user = Users.query.filter_by(user_name=user_name).first()
    user.hash = bcrypt.generate_password_hash(password)
    db.session.commit()


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