#https://auth0.com/docs/quickstart/backend/python/01-authorization

import os
from flask import Flask, make_response, send_file,render_template, request, redirect, url_for,jsonify,g
from werkzeug.utils import secure_filename
from functools import wraps
import jwt

from flask import Flask, flash, request, redirect, url_for,_request_ctx_stack,Response,current_app,g
from werkzeug.utils import secure_filename
import json,time,os,threading
from queue import Queue
from flask_cors import CORS,cross_origin
import pdf_page_titles,zip_file
from six.moves.urllib.request import urlopen

#api auth
AUTH0_DOMAIN = 'dev-j3w5kkcgno5ahh5s.us.auth0.com'
YOUR_API_AUDIENCE='https://dev-j3w5kkcgno5ahh5s.us.auth0.com/api/v2/'
API_AUDIENCE = YOUR_API_AUDIENCE
ALGORITHMS = ["RS256"]


#payload tag needs to be changed - when I swapped it to user_email it stopped, so there's rules in play to govern what this can be
EMAIL_KEY='https://my-app.example.com/email'

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app,resources=['http://localhost:5173'])

#use a user's email address to construct a folder to store files in
def user_directory(user_email):
    return secure_filename(user_email).replace('.','_')



def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.decode(token, options={"verify_signature": False})
    if unverified_claims.get("scope"):
            token_scopes = unverified_claims["scope"].split()
            for token_scope in token_scopes:
                if token_scope == required_scope:
                    return True
    return False

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    print(request)
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

#example code for how to handle preflight - can't be implemented as a annotation because the function needs to return this response
def handle_preflight(method):
    if method.lower=='options':
        print('responding to pre-flight')
        to_respond= Response()
        to_respond.headers.add('Access-Control-Allow-Origin', '*')
        to_respond.headers.add('Access-Control-Allow-Headers','authorization')
        
        return to_respond

#this has to be the last decorator before the function or it won't work
def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        print('in decorator')
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        public_key = None
        print(jwks)
        print(jwks["keys"])
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                #this needs cryptography installed to work
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
        if public_key:
            try:
                payload = jwt.decode(
                    token,
                    public_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.InvalidAudienceError:
                raise AuthError({"code": "invalid_audience",
                                "description":
                                    "incorrect audience,"
                                    " please check the audience"}, 401)
            except jwt.InvalidIssuerError:
                raise AuthError({"code": "invalid_issuer",
                                "description":
                                    "incorrect issuer,"
                                    " please check the issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)
            #store the user from the access token
            _request_ctx_stack.top.current_user = payload[EMAIL_KEY]
            g= payload[EMAIL_KEY]
            print("current user")
            
            #payload tag needs to be changed - when I swapped it to user_email it stopped, so there's rules in play to govern what this can be
            print(payload['https://my-app.example.com/email'])
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
#setup queue for simple multithreading - could eventually be switched to celery
data_queue=Queue()
app = Flask(__name__)

#need to make this a relative path
PDF_FOLDER = 'C:\\projects\\Band_PDF_Manager\\band_pdf_manager\\src\\endpoints\\hosted_files'  # Replace with the path to your PDF folder

#do processing work on a pdf
def process_pdf(pdf_name,folder,user):
    pdf_page_titles.end_to_end_pdf(pdf_name)
    if not os.path.isdir(os.path.join('hosted_files')):
        os.mkdir('hosted_files')
    user_dir=user_directory(user)
    if not os.path.isdir(os.path.join('hosted_files')+os.path.sep+user_dir):
        os.mkdir('hosted_files'+os.path.sep+user_dir)
    final_dir=os.path.join(f'hosted_files{os.path.sep+user_directory(user)}', secure_filename(pdf_name.split('.')[0])+'.zip')
    print(final_dir)
    zip_file.zipdir(folder,final_dir)

#simple queue for now
def process_queue():
    while True:
        if not data_queue.empty():
            data = data_queue.get()
            print(data[1])
            print("processing data:", data)
            #filename, filename before the ., the user
            print(data[1])
            process_pdf(data[0],data[0].split('.')[0],data[1])
        else:
            time.sleep(1)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@cross_origin(headers=["Content-Type", "Authorization"])
@app.route('/pdf/<string:filename>',methods=['OPTIONS'])
def pdf_pre_flight(filename):
    print('responding to pre-flight pdf')
    to_respond= Response()
    to_respond.headers.add('Access-Control-Allow-Origin', '*')
    to_respond.headers.add('Access-Control-Allow-Headers','authorization')
    
    return to_respond

#serve a completed pdf/zip file
@cross_origin(headers=["Content-Type", "Authorization"])
@app.route("/pdf/<string:filename>", methods=['GET'])
@requires_auth
def return_pdf(filename):
    user_email=_request_ctx_stack.top.current_user

    try:
        filename = secure_filename(filename)  # Sanitize the filename
        file_path = os.path.join(f'{PDF_FOLDER+os.path.sep+user_directory(user_email)}', filename)
        print(file_path)
        if os.path.isfile(os.path.join('hosted_files',file_path)):
            response=send_file(file_path, as_attachment=True)
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers','authorization')
            return response
        else:
            response = make_response(f"File '{filename}' not found.", 404)
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers','authorization')
            return response
    except Exception as e:
        response = make_response(f"Error: {str(e)}", 500)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers','authorization')
        return response
    
@cross_origin(headers=["Content-Type", "Authorization"])
@app.route('/auth_get_list',methods=['OPTIONS'])
def auth_pre_flight():
    print('responding to pre-flight')
    to_respond= Response()
    to_respond.headers.add('Access-Control-Allow-Origin', '*')
    to_respond.headers.add('Access-Control-Allow-Headers','authorization')
    
    return to_respond

@cross_origin(headers=["Content-Type", "Authorization"])
@app.route('/auth_get_list',methods=['GET'])
@requires_auth
def auth_get_list():
    user_email=_request_ctx_stack.top.current_user
    print('responding to auth_get_list get')
    f = []
    for (dirpath, dirnames, filenames) in os.walk(f'hosted_files{os.path.sep+user_directory(user_email)}'):
        f.extend(filenames)
        break
    print('in get_file_list')
    print(f)
    response=jsonify(f)
    response.headers.add("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response


@cross_origin(headers=["Content-Type", "Authorization"])
@app.route('/',methods=['OPTIONS'])
def file_pre_flight():
    print('responding to pre-flight')
    to_respond= Response()
    to_respond.headers.add('Access-Control-Allow-Origin', '*')
    to_respond.headers.add('Access-Control-Allow-Headers','authorization')
    
    return to_respond

#get the PDF file for the entire song
#needs to create a folder for the files
#run the routines for pdf seperate
#place the splices in the folder
#zip the folder
#send zipped contents back to the website

@cross_origin(headers=["Content-Type", "Authorization"])
@app.route('/', methods=['POST'])
@requires_auth
def upload_file():
    print(request.method)
    print('starting file')
    user=_request_ctx_stack.top.current_user
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
            data_queue.put([filename,user])

            response=jsonify({"message": "PDF generated successfully!",
			'downloadLink': 'http://localhost:3000/${outputFilePath}','headers':''}),
            #response.headers.add('Access-Control-Allow-Origin', '*')
            return response


if __name__=='__main__':
     threading.Thread(target=process_queue,daemon=True).start()
     app.run(host='127.0.0.1', port=5002)