from flask import Flask
from flask import jsonify
import utils

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/test')
def get_view_test():
    jdata = utils.test()
    return jsonify(jdata)


@app.route('/s1')
def get_s1_data():
    s1_data = utils.get_s1_data()
    return jsonify(s1_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876, debug=True)
