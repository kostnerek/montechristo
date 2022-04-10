from app.models.User.UserModel import UserModel
from flask_restful import Resource

class User(Resource):
    def get(self, username):
        user = UserModel.find_by_username(username)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json(), 200
    def delete(self, username):
        user = UserModel.find_by_username(username)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200



