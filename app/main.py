from flask import Flask, jsonify
import time
app = Flask(__name__, static_folder='../build', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/time')
def temperature():
    return jsonify({'time': time.time()})

@app.route('/v')
def version():
    return jsonify({'version': '0.1.0'})
#app.run()