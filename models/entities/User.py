from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password, fullname='') -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

""" print(generate_password_hash('alf123'), len(generate_password_hash('alf123')))
print("d:", len("7a3ed351bca401918c58dac8a5314a70c289527c")) """