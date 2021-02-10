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

app = Flask(__name__)

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path_or_model='weights/best.pt', force_reload=True).autoshape() 
model.eval()

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
    # if os.path.exists("./static/results0.jpg"):
      # os.remove("./static/results0.jpg")
      # print("Bestand verwijderd!")
    # else:
      # print("The file does not exist") 

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
            
            callProgram = str("python detect.py --source .\\static\\uploads\\" + filename + " --weights weights\\best.pt --save-txt --save-conf")
            os.system(callProgram)
            
            # # Open image
            # imgName = './static/uploads/' + filename
            # img = Image.open(imgName)  # PIL image
            # # Inference
            # results = model(img, size=416)  # includes NMS
            # # Results
            # results.save()  # 
            # data = [ ]
            # for object in range(len(results.xyxy[0])):
                # data.append([])
                # for val in range(len(results.xyxy[0][object])):
                    # i = round(results.xyxy[0][object][val].item(), 2)
                    # data[object].append(i)
            # print(data)
            # data = [[694.20, 116.37, 995.70, 441.81, 0.66, 1.0], [71.19, 26.40, 573.51, 459.90, 0.32, 1.0]]
            txtfile = filename[:-3]
            txtfile = txtfile + 'txt'
            labelsTxt = './static/recognized/labels/' + txtfile
            # f = open(labelsTxt, "r")
            # print(f.read()) 
            # f.close()
            data = [ ]
            with open(labelsTxt, 'r') as f:
                for x in f:
                    tokens = x.strip().split(' ')   # tokenize the row based on spaces
                    data.append(tokens)
                    # for line in f:
                        # tokens = line.strip().split(' ')   # tokenize the row based on spaces
                        # myList.append(tokens)
            print(data)
            
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
    app.run(debug=True)  #connect to http://127.0.0.1:5000/
    #app.run(debug=True, host= '172.20.10.3') #connect to http://172.20.10.3:5000/
