from app.models.User.UserModel import UserModel
from flask_restful import Resource

class User(Resource):
    def get(self, user_id):
        user = UserModel.find_by_username(username)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json(), 200
    def delete(self, user_id):
        user = UserModel.find_by_username(username)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete()
        return {'message': 'User deleted'}, 200



