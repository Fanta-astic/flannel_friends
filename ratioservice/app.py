# flask_web/app.py
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def sample_post():

    if request.method == 'GET':

        # Determine compression ratio given size parameters
        origFileSize = request.args['origFileSize']
        gzipFileSize = request.args['gzipFileSize']
        fileName = request.args['fileName']
        ratio = int(origFileSize) / int(gzipFileSize)
        return fileName + " was compressed with a ratio of " + str(ratio)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
