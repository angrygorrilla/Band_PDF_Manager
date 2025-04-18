import os
from flask import Flask, make_response, send_file,render_template, request, redirect, url_for,jsonify
from werkzeug.utils import secure_filename

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import json,time,os,threading
from queue import Queue
from flask_cors import CORS

import pdf_page_titles,zip_file
UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

#setup queue for simple multithreading - could eventually be switched to celery
data_queue=Queue()
app = Flask(__name__)
PDF_FOLDER = 'C:\\projects\\band_ocr\\Band_PDF_Manager\\band_pdf_manager\\src\\endpoints\\hosted_files'  # Replace with the path to your PDF folder

#serve a completed pdf zip file
@app.route("/pdf/<string:filename>", methods=['GET'])
def return_pdf(filename):
    try:
        filename = secure_filename(filename)  # Sanitize the filename
        file_path = os.path.join(PDF_FOLDER, filename)
        print(file_path)
        if os.path.isfile(os.path.join('hosted_files',file_path)):
            response=send_file(file_path, as_attachment=True)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            response = make_response(f"File '{filename}' not found.", 404)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    except Exception as e:
        response = make_response(f"Error: {str(e)}", 500)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
#do processing work on a pdf
def process_pdf(pdf_name,folder):
    pdf_page_titles.end_to_end_pdf(pdf_name)
    if not os.path.isdir(os.path.join('hosted_files')):
        os.mkdir('hosted_files')
        #error in ziping files - Cannot create a file when that file already exists: 'hosted_files'
    zip_file.zipdir(folder,os.path.join('hosted_files', secure_filename(pdf_name.split('.')[0])+'.zip'))

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

            response=json.dumps({"message": "PDF generated successfully!",
			'downloadLink': 'http://localhost:3000/${outputFilePath}'}),
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

@app.route('/file_list', methods=['GET'])
def seperated_files():
    f = []
    for (dirpath, dirnames, filenames) in os.walk('hosted_files'):
        f.extend(filenames)
        break
    print('in get_file_list')
    print(f)
    response=jsonify(f)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__=='__main__':
     threading.Thread(target=process_queue,daemon=True).start()
     app.run(host='127.0.0.1', port=5002)