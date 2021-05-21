from flask import Flask
from flask import jsonify
import utils

app = Flask(__name__)


# @app.route('/')
# def index():
#     return '<h1>Hello World!</h1>'


@app.route('/s1/ab')
def get_s1_ab_data():
    s1_ab_data = utils.get_s1_ab_data()
    response = jsonify(s1_ab_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    return response


@app.route('/s1/c')
def get_s1_c_data():
    s1_c_data = utils.get_s1_c_data()
    response = jsonify(s1_c_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    return response


@app.route('/s1/d')
def get_s1_d_data():
    s1_d_data = utils.get_s1_d_data()
    response = jsonify(s1_d_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    return response


@app.route('/s1/ef')
def get_s1_ef_data():
    s1_ef_data = utils.get_s1_ef_data()
    response = jsonify(s1_ef_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    return response


@app.route('/s2/a')
def get_s2_a_data():
    s2_a_data = utils.get_s2_a_data()
    response = jsonify(s2_a_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    return response


@app.route('/s2/b')
def get_s2_b_data():
    s2_b_data = utils.get_s2_b_data()
    response = jsonify(s2_b_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    return response


@app.route('/s2/c')
def get_s2_c_data():
    s2_c_data = utils.get_s2_c_data()
    response = jsonify(s2_c_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    return response


@app.route('/s2/d')
def get_s2_d_data():
    s2_d_data = utils.get_s2_d_data()
    response = jsonify(s2_d_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    return response


@app.route('/s2/ef')
def get_s2_ef_data():
    s2_ef_data = utils.get_s2_ef_data()
    response = jsonify(s2_ef_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    return response


@app.route('/s3/a')
def get_s3_a_data():
    s3_a_data = utils.get_s3_a_data()
    response = jsonify(s3_a_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    return response


@app.route('/s3/b')
def get_s3_b_data():
    s3_b_data = utils.get_s3_b_data()
    response = jsonify(s3_b_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    return response


@app.route('/s3/cd')
def get_s3_cd_data():
    s3_cd_data = utils.get_s3_cd_data()
    response = jsonify(s3_cd_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876, debug=True)
