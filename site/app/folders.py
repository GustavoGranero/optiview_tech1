
from optview import db
from models.folders import Folders

def get_new_folder_name_from_number(app, number):
    return app.config['FOLDER_NEW_NAME_TEMPLATE'].format(number=number)

def folder_name_exists(app, number, user_id):
    new_folder_name = get_new_folder_name_from_number(app, number)
    return Folders.get_one(name = new_folder_name, user_id = user_id)

def get_new_folder_name(app, current_user):
    number = ''
    seq = 0
    while folder_name_exists(app, number, current_user.id) is not None:
        seq += 1
        number = f' {seq}'

    return get_new_folder_name_from_number(app, number)

