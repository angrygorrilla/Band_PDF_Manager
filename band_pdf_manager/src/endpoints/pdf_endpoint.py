import os
from flask import Flask, make_response, send_file,render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import json,time,os,threading
from queue import Queue

import pdf_page_titles,zip_file
UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#setup queue for simple multithreading - could eventually be switched to celery
data_queue=Queue()
app = Flask(__name__)
PDF_FOLDER = '/path/to/pdf/folder'  # Replace with the path to your PDF folder

#serve a completed pdf zip file
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
    
#do processing work on a pdf
def process_pdf(pdf_name,folder):
    pdf_page_titles.end_to_end_pdf(pdf_name)
    zip_file.zipdir(folder,pdf_name.split('.')[0]+'.zip')

#simple queue for now
def process_queue():
    while True:
        if not data_queue.empty():
            data = data_queue.get()
            print("processing data:", data)
            process_pdf(data,data.split('.')[0])
        else:
            time.sleep(1)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#get the PDF file for the entire song
#needs to create a folder for the files
#run the routines for pdf seperate
#place the splices in the folder
#zip the folder
#send zipped contents back to the website
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
            data_queue.put(filename)
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
        
if __name__=='__main__':
     threading.Thread(target=process_queue,daemon=True).start()
     app.run(host='127.0.0.1', port=5002)