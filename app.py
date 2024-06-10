from flask import Flask, request, jsonify,Response
from werkzeug.utils import secure_filename
import os
import json
import os
# import the libraries from model 
# chestScanPrediction -- > the evaluation function
# pred_info --> convert the index to json
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = APP_ROOT
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
info ="test done success"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    

@app.route('/api/upload', methods=['POST','GET'])
def lung_upload():
    # target = os.path.join(APP_ROOT, 'lung-images/')  #folder path

    # if not os.path.isdir(target):
        # os.mkdir(target)     # create folder if not exits

    if request.method == 'POST':
        
        if 'file' not in request.files:
            return Response(
               response = json.dumps(
                   {"message":"No image part"}),
                   status = 500,
                   mimetype = 'application/json'
            )

        image = request.files['file']
        if image.filename == '':
           return Response(
               response = json.dumps(
                   {"message":"No image selected for uploading"}),
                   status = 500,
                   mimetype = 'application/json'
            )
        if image and allowed_file(image.filename): 
            filename = secure_filename(image.filename)
            # destination = "/".join([target, filename]) #/APP_ROOT/lung-images/something.jpg
            image.save('lung-images/'+filename)
            # save to database
            return Response(
               response = json.dumps(
                   {"message":"done success cheers"}),
               status = 200,
               mimetype = 'application/json'
            )
        else:
            return Response(
               response = json.dumps(
                   {"message":"Allowed image types are -> png, jpg, jpeg, gif"}),
               status = 500,
               mimetype = 'application/json'
            )
    elif request.method == 'GET':
        return Response(
            response= json.dumps({
                "result": "info"
                }))
    return {"message":f"{request.method}"}

# for test purposes 
@app.route('/test',methods=['GET'])
def test():
    return Response(
        response= json.dumps({
            'message':'You did it!!'
            }),
        status=200,
        mimetype='application/json')

@app.errorhandler(404)
def not_found():
    return Response(
       response = json.dumps(
           {"message":"route not found"}),
       status = 500,
       mimetype = 'application/json'
    )
            
            


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug= True)


# see more at
# https://stackoverflow.com/questions/65298241/what-does-this-tensorflow-message-mean-any-side-effect-was-the-installation-su
