# flask_web/app.py
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, send_from_directory
import os
import gzip
import requests
import tempfile

app = Flask(__name__)
UPLOAD_FOLDER = '/app/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Default Landing Page
@app.route('/')
def index():
    return render_template('index.html')

# Download Compressed File
@app.route('/download/<filename>', methods=['POST','GET'])
def download(filename):
    tempDir = tempfile.TemporaryDirectory(dir = "/app/uploads")
    os.replace("/app/uploads/" + filename, tempDir.name + "/" + filename)
    os.replace("/app/uploads/" + filename.strip('.gz'), tempDir.name + "/" + filename.strip('.gz'))
    return send_from_directory(tempDir.name, filename)


@app.route('/uploadFile', methods=['POST'])
def uploadFile():

    if request.method == 'POST':
        if 'file':

            # Save file uploaded by user
            f = request.files['file']
            upload_file = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], upload_file))

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

            return (render_template('download.html', filename=f.filename+".gz", stats=stats.text))

@app.route('/generateLoad', methods=['GET'])
def formY():

    if request.method == 'GET':

            # Generate CPU load with other microservice
            result = requests.get('http://detailservice:5002')
            return result.content

    else:
        return "Failure"
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
