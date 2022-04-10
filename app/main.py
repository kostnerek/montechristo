from flask import Flask, jsonify
import time
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_required
from datetime import timedelta
import os
from dotenv import load_dotenv, dotenv_values

#from models.User.UserModel import UserModel
from .db import db
from .blacklist import BLACKLIST


app = Flask(__name__, static_folder='../build', static_url_path='/')

load_dotenv(override=True)
app.config["MONGODB_SETTINGS"] = {
    "host": os.environ["MONGODB_URL"],
    "port": 27017,
}
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=5)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.secret_key = os.getenv("SECRET_KEY")

api = Api(app)
jwt = JWTManager(app) # /auth
db.init_app(app)

@jwt.token_in_blocklist_loader
def check_if_in_bl(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLACKLIST


from .resources.User.UserLoginResource import UserLogin, UserLogout, TokenRefresh
from .resources.User.UserRegisterResource import UserRegister
from .resources.User.UserResource import User

api.add_resource(UserLogin,    '/api/login')
api.add_resource(UserLogout,   '/api/logout')
api.add_resource(TokenRefresh, '/api/token/refresh')
api.add_resource(UserRegister, '/api/register')
api.add_resource(User,         '/api/user/<string:username>')


""" 
@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the API'})

@app.route('/api/time')
def temperature():
    return jsonify({'time': time.time()})

@app.route('/v')
def version():
    return jsonify({'version': '0.1.0'}) """


if __name__ == '__main__':
    
    app.run(debug=True, port=5000)