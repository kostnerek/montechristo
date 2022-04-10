#from models.User.UserModel import UserModel
from app.models.User.UserModel import UserModel
from app.blacklist import BLACKLIST
from werkzeug.security import check_password_hash
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_jwt,
                                get_jwt_identity,
                                get_jti)

user_login_parser = reqparse.RequestParser()
user_login_parser.add_argument('username', type=str, default=None)
user_login_parser.add_argument('mail',     type=str, default=None)
user_login_parser.add_argument('password', type=str, required=True, help='This field cannot be left blank')

class UserLogin(Resource):
    def check_what_creds_are_used(self):
        data = user_login_parser.parse_args()
        if(data['username']):
            return 'username'
        if(data['mail']):
            return 'mail'
        return False
    
    def post(self):
        data = user_login_parser.parse_args()
        credintials = self.check_what_creds_are_used()
        if not credintials:
            return {'message': 'No credintials provided'}, 400
        user = UserModel.find_by_username(data['username']) if credintials == 'username' else UserModel.find_by_mail(data['mail'])
        
        if not user:
            return {'message': 'User not found'}, 404
        
        if check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token= create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            },200
        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    logout_parser = reqparse.RequestParser()
    logout_parser.add_argument('refresh_token', type=str, required=True, help='This field cannot be left blank')
    @jwt_required()
    def delete(self):
        refresh_token = UserLogout.logout_parser.parse_args()['refresh_token']
        #print("Blacklist before: ", BLACKLIST)
        #print(refresh_token)
        access_token_jti=get_jwt()['jti']
        refresh_token_jti=get_jti(refresh_token)
        BLACKLIST.add(access_token_jti)
        BLACKLIST.add(refresh_token_jti)
        #print(BLACKLIST)
        return {'message': 'Successfully logged out'}, 200

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        print('Non fresh token: ',get_jwt()['jti'])
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200