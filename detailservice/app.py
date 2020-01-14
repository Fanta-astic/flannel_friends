# flask_web/app.py
from flask import Flask
from flask import request
from math import sqrt

app = Flask(__name__)

@app.route('/', methods=['GET'])
def sample_post():

    if request.method == 'GET':

        # Perform random computation
        for x in range (1, 1000000, 1):
            x += sqrt(x)

        return "Computation Complete!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
