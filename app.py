from flask import Flask, request
import pandas as pd
from flask import render_template
from flask import jsonify
from flask_restful import Api
from service import find_street


app = Flask(__name__)
api = Api(app)

df_csv = pd.read_csv('data.csv')
street_names = df_csv['streetName'].unique()


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/find', methods=['POST'])
def find():
    data = request.get_json()
    json_to_send = find_street(street_names, data)
    return jsonify(json_to_send)


if __name__ == '__main__':
    app.run(port='5002', debug=True)
