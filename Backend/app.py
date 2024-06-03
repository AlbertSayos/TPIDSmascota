from flask import Flask,jsonify #transforma un texto a json
PORT = 8081

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify(messege="hola mundo") #devolvemos un json de hola mundo


if __name__ == '__main__':
    app.run(debug=True, port=PORT)
