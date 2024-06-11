from flask import Flask, request, jsonify, Response
from werkzeug.utils import secure_filename
import os
import json
# import the libraries from model 
# chestScanPrediction -- > the evaluation function
# pred_info --> convert the index to json
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
info = "test done success"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload', methods=['POST', 'GET'])
def lung_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return Response(
                response=json.dumps({"message": "No image part"}),
                status=400,
                mimetype='application/json'
            )

        image = request.files['file']
        if image.filename == '':
            return Response(
                response=json.dumps({"message": "No image selected for uploading"}),
                status=400,
                mimetype='application/json'
            )
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure the folder exists
            image.save(image_path)
            # save to database or further processing
            return Response(
                response=json.dumps({"message": "done success cheers"}),
                status=200,
                mimetype='application/json'
            )
        else:
            return Response(
                response=json.dumps({"message": "Allowed image types are -> png, jpg, jpeg, gif"}),
                status=400,
                mimetype='application/json'
            )
    elif request.method == 'GET':
        return Response(
            response=json.dumps({"result": info}),
            status=200,
            mimetype='application/json'
        )


@app.route('/test', methods=['GET'])
def test():
    return Response(
        response=json.dumps({'message': 'You did it!!'}),
        status=200,
        mimetype='application/json'
    )


@app.errorhandler(404)
def not_found(error):
    return Response(
        response=json.dumps({"message": "route not found"}),
        status=404,
        mimetype='application/json'
    )

@app.errorhandler(500) 
def internal_error(error): 
    app.logger.error('Server Error: %s', error) 
    return Response( 
        response=json.dumps({"message": f"Internal server error : {error}"}),
        status=500, 
        mimetype='application/json' )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
