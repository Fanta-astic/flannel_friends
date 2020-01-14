# flask_web/app.py
from werkzeug.utils import secure_filename
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
import os
import gzip
import requests

app = Flask(__name__)
UPLOAD_FOLDER = '/app/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['POST'])
def main():

    if request.method == 'POST':
        if 'file':

            # Save file uploaded by user
            f = request.files['file']
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Compress uploaded file
            in_file = "/app/uploads/" + f.filename
            in_data = open(in_file, "rb").read()
            out_gz = "/app/uploads/" + f.filename + ".gz"
            gz_file = gzip.open(out_gz, "wb")
            gz_file.write(in_data)
            gz_file.close()

            # Determine compression ratio with other microservice
            origFileSizeVal =  os.path.getsize(in_file)
            gzipFileSizeVal = os.path.getsize(out_gz)
            ratio = {'fileName':f.filename, 'origFileSize':origFileSizeVal, 'gzipFileSize':gzipFileSizeVal}
            stats = requests.get('http://ratioservice:5001', params = ratio)
            print(stats.content, flush=True)

            # Generate CPU load with other microservice
            result = requests.get('http://detailservice:5002')
            print(result.content, flush=True)

            # Delete original and return compressed file to user
            return send_file(out_gz, as_attachment=True)

    else:
        return "Failure"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
