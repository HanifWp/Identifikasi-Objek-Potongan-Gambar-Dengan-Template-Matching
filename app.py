import os
from flask import Flask, request, redirect, url_for, render_template,flash
from werkzeug.utils import secure_filename
import numpy as np
import cv2 as cv

app = Flask(__name__, static_url_path="/static")
UPLOAD_FOLDER ='static/uploads/'
UPLOAD2_FOLDER ='static/uploads2/'
DOWNLOAD_FOLDER = 'static/downloads/'
ALLOWED_EXTENSIONS = {'jpg', 'png','.jpeg'}

# APP CONFIGURATIONS
app.config['SECRET_KEY'] = 'rahasia'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD2_FOLDER'] = UPLOAD2_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# limit upload size to 2mb
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    

@app.route('/', methods=['GET', 'POST'])
def index():
    global file
    global file2
    if request.method == 'POST':
        global templates
        global result

        if 'file' and 'file2' not in request.files:
            flash('No file attached in request')
            return redirect(request.url)

        file = request.files['file']
        file2 = request.files['file2']

        if file.filename and file2.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file2 and allowed_file(file2.filename):
            filename2 = secure_filename(file2.filename) 
            file2.save(os.path.join(UPLOAD2_FOLDER, filename2))
            data2= {
                "uploaded2_img":'static/uploads2/'+filename2
            }
            templates = 'static/uploads2/'+filename2

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            result = filename
            process_file(os.path.join(UPLOAD_FOLDER,filename),filename)
            data={
                "processed_img":'static/downloads/'+filename,
                "uploaded_img":'static/uploads/'+filename
            }

            
        return render_template("index.html",data=data, data2=data2)

    return render_template('index.html')


def process_file(path, filename):
    matchingtemplate(path, filename)


def matchingtemplate(path, filename):
    img_rgb = cv.imread(path)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread(templates ,0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        cv.imwrite('static/downloads/'+result,img_rgb)