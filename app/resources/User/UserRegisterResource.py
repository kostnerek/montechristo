from app.models.User.UserModel import UserModel
import re
from flask_restful import Resource, reqparse
from email_validator import validate_email
from string import punctuation, whitespace, digits, ascii_lowercase, ascii_uppercase


user_register_parser = reqparse.RequestParser()
user_register_parser.add_argument('username', type=str, required=True, help='This field cannot be left blank')
user_register_parser.add_argument('mail',     type=str, required=True, help='This field cannot be left blank')
user_register_parser.add_argument('password', type=str, required=True, help='This field cannot be left blank')

class UserRegister(Resource):    
    def check_if_user_exists(self, username, mail):
        error = ''
        if UserModel.find_by_username(username):
            error+= f"User with username '{username}' already exists"
        if UserModel.find_by_mail(mail):
            error+= f" User with mail '{mail}' already exists"
        return error if len(error)>0 else False
    
    def validate_mail(self, mail):
        try:
            validate_email(mail)
            return True
        except Exception as e:
            return False

    def validate_password(self, password):
        """
            password must be between 6 and 20 characters,
            must have at least one lowercase letter and uppercase letter,
            must have at least one digit,
            must have one of the special characters '-', '_', '.', '!', '@', '#', '$', '^', '&', '(', ')'
        """
        new_password = password.strip()

        MIN_SIZE = 6
        MAX_SIZE = 20
        password_size = len(new_password)
        if password_size < MIN_SIZE or password_size > MAX_SIZE:
            return False
        valid_chars = {'-', '_', '.', '!', '@', '#', '$', '^', '&', '(', ')'}
        invalid_chars = set(punctuation + whitespace) - valid_chars
        for char in invalid_chars:
            if char in new_password:
                return False
        password_has_digit = False
        for char in password:
            if char in digits:
                password_has_digit = True
                break
        if not password_has_digit:
            return False
        password_has_lowercase = False
        for char in password:
            if char in ascii_lowercase:
                password_has_lowercase = True
                break
        if not password_has_lowercase:
            return False
        password_has_uppercase = False
        for char in password:
            if char in ascii_uppercase:
                password_has_uppercase = True
                break
        if not password_has_uppercase:
            return False
        return True

    
    def post(self):
        data = user_register_parser.parse_args()
        check_if_exist = self.check_if_user_exists(data['username'], data['mail'])
        if check_if_exist:
            return {'message': check_if_exist}, 400
        if not self.validate_mail(data['mail']):
            return {'message': 'Invalid mail'}, 400
        if not self.validate_password(data['password']):
            return {'message': 'Invalid password'}, 400
        if len(data['username']) < 3:
            return {'message': 'Username must be at least 3 characters long'}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User created successfully', 'user': user.json()}, 201