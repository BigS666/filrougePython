import io
import json
import os
import math
import magic
import fileManager
import awsInterface

from sys import getsizeof
from werkzeug.utils import secure_filename

from flask import (Flask, Response, jsonify, request, send_file,
                   send_from_directory)

from flask_swagger_ui import get_swaggerui_blueprint
from flask_swagger import swagger

app = Flask(__name__)



ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','docx','csv','pptx'])
dictionnaire_type = dict((('txt','text/plain'),('pdf','application/pdf'),('png','image/png'),('jpg','image/jpeg'),('jpeg','image/jpeg'),('gif','image/gif'),('docx','application/vnd.openxmlformats-officedocument.wordprocessingml.document'),('pptx','application/vnd.openxmlformats-officedocument.presentationml.presentation'),('csv','text/plain')))

app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['AWS_BUCKET_NAME'] = "filrouge-poirier"

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Mon PAI FilRouge"
    return jsonify(swag)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Jsonifyeur de documents"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###


@app.route("/document", methods=["POST"])
def soumissionDocument():
    """upload a doc, responds whith its content and metadatas in a json

    >>> curl -F mydata=@mondoc.type http://127.0.0.1:5000/document \n
    >{"type":docx}
    """
    retour = ""
    
    # testing existance of 'mydata' as attached file to upload
    if "mydata" not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp

    file = request.files["mydata"]

    # testing filname not empty
    if file.filename == "":
        resp = jsonify({'message' : 'No file selected for josonifying'})
        resp.status_code = 400
        return resp

    # f is a file-like object. 
    old_file_position = file.tell()
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(old_file_position, os.SEEK_SET)

    #testing size of the file
    if(size > app.config['MAX_CONTENT_LENGTH']):
        resp = jsonify({'message' : 'File too big, more than 5MB'})
        resp.status_code = 400
        return resp


    if file and allowed_file(file.filename):
        
        filename = secure_filename(file.filename)
        fullFile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(fullFile)

        extension = file.filename.rsplit('.', 1)[1].lower()
        mimetype = magic.from_file(fullFile, mime=True)

        if(dictionnaire_type.get(extension) == mimetype):

            content,metas = fileManager.getFileMetasAndContent(file=fullFile,mimetype=mimetype)

            #Upload vers S3

            uploaded = False
            #with open(fullFile,"rb") as s3File:
            if(awsInterface.upload_file(fullFile, app.config['AWS_BUCKET_NAME'],filename)):
                uploaded = True
                if(mimetype=='image/jpeg' or mimetype=='image/png'):
                    labels = awsInterface.detect_labels(app.config['AWS_BUCKET_NAME'],filename)
                    if(labels != False):
                        metas["rekognition_labels"] = labels

            resp = jsonify({'message' : 'File successfully analyzed','size' : convert_size(size), 's3-uploaded' : uploaded, 'mimetype' : mimetype, 'SecuredFileName' : filename, 'content' : content, 'metasdatas' : metas})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'message' : 'Incoherence between extension of file and its content, extension: '+extension+", mimetype: "+mimetype})
            resp.status_code = 400
            os.remove(fullFile)
            return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, pptx, gif, docx, csv'})
        resp.status_code = 400
        return resp

    return retour