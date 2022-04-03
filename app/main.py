from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'endpoints': {'/': 'Home', '/temperature': 'returns temperature', '/v': 'returns version'}})

@app.route('/temperature')
def temperature():
    return jsonify({'temperature': '20'})

@app.route('/v')
def version():
    return jsonify({'version': '0.1.0'})
#app.run()