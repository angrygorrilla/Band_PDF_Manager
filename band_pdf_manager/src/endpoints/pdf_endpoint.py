import os
from flask import Flask, make_response, send_file,render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import json

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app = Flask(__name__)
PDF_FOLDER = '/path/to/pdf/folder'  # Replace with the path to your PDF folder

@app.route("/pdf/<string:filename>", methods=['GET'])
def return_pdf(filename):
    try:
        filename = secure_filename(filename)  # Sanitize the filename
        file_path = os.path.join(PDF_FOLDER, filename)
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return make_response(f"File '{filename}' not found.", 404)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('.',filename))
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 