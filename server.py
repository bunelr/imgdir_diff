#!/usr/bin/python
import os
import sys
import webbrowser

webbrowser.get("/usr/bin/chromium-browser %s").open_new("http://localhost:8000")

from flask import Flask, render_template, send_file

first_folder = sys.argv[1]
second_folder = sys.argv[2]

first_files = os.listdir(first_folder)
second_files = os.listdir(second_folder)

first_files = [os.path.join(os.getcwd(), first_folder, img_name) for img_name in first_files]
second_files = [os.path.join(os.getcwd(), second_folder, img_name) for img_name in second_files]

first_files.sort()
second_files.sort()

app = Flask(__name__)

@app.route('/<img_id>')
def img_comp(img_id):
    index = int(img_id)
    file_1 = first_files[index]
    file_2 = second_files[index]
    return render_template('image_diff.html', file_1= file_1, file_2=file_2, index = index)


@app.route('/')
def index():
    return img_comp('0')

@app.route('/media', defaults={'path': ''})
@app.route('/media/<path:path>')
def serve_images(path):
    return send_file('/' + path, mimetype='image/x-windows-bmp')

app.run(debug = True, port= 8000)
