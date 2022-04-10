#from db import db
from app.db import db 
from werkzeug.security import generate_password_hash
class UserModel(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    mail     = db.StringField(required=True, unique=True)
    
    def json(self):
        return {
                'username': self.username, 
                'mail': self.mail
                }
    @classmethod
    def find_by_username(cls, username):
        return cls.objects(username=username).first()
    @classmethod
    def find_by_mail(cls, mail):
        return cls.objects(mail=mail).first()