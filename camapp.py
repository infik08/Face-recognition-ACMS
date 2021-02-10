# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 21:04:26 2021

@author: z0043zrx
"""

from flask import Flask, render_template, Response, request, redirect, flash, url_for
import cv2
import os
import torch
from PIL import Image
from werkzeug.utils import secure_filename
import time
import glob

app = Flask(__name__)

#declaraties voor uploads:  
UPLOAD_FOLDER = "./static/uploads"
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#def Toegestaande uploads:
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# pagina voor uploaden 
@app.route('/')
def upload_form():
	return render_template('upload.html')

# functionaliteit uploaden
@app.route('/', methods=['POST'])
def upload_image():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('files[]')
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            callProgram = str("python detect.py --source .\\static\\uploads\\" + filename + " --weights weights\\best.pt --conf 0.75 --save-txt --save-conf")
            os.system(callProgram)
            
            txtfile = filename[:-3]
            txtfile = txtfile + 'txt'
            labelsTxt = './static/recognized/labels/' + txtfile

            data = [ ]
            with open(labelsTxt, 'r') as f:
                for x in f:
                    val = x.strip().split(' ')   # tokenize the row based on spaces
                    data.append(val)
                    
            for z in range(len(data)):
                for y in range(1,5):
                    data[z][y] = round(float(data[z][y]) * 416, 2)
                    
            os.remove(labelsTxt)
            print('\n', filename)
            print('\n', data[0])
            print('\n', data[1])
        return render_template('upload.html', filenames=file_names, data=data)

# weergeven geuploadde afbeeldingen
@app.route('/static/recognized/<filename>')
def display_image(filename):
 	# print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='Recognized/' + filename), code=301)

# weergeven info
@app.route('/info')
def info():
	return render_template("info.html")
    
# pagina voor gallerij 
@app.route('/gallery')
def gallery():
	return render_template("gallery.html")

# main
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')  #connect to http://127.0.0.1:5000/
    #app.run(debug=True, host= '172.20.10.3') #connect to http://172.20.10.3:5000/
