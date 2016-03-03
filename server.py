#!/usr/bin/python
import os
import sys
import webbrowser
from flask import Flask, render_template, send_file

app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.CRITICAL)

webbrowser.get("/usr/bin/chromium-browser %s").open_new("http://localhost:8000")

img_suffixes = [".bmp", ".png", ".jpg", ".jpeg"]


def build_list_of_images(folder_path):
    full_paths = []
    files = os.listdir(folder_path)
    for f in files:
        base, extension = os.path.splitext(f)
        if extension in img_suffixes:
            path = os.path.join(os.getcwd(), folder_path, f)
            full_paths.append(path)
    full_paths.sort()
    return full_paths

first_folder = sys.argv[1]
second_folder = sys.argv[2]

first_files = build_list_of_images(first_folder)
second_files = build_list_of_images(second_folder)

@app.route('/favicon.ico')
def favicon():
    return ''

@app.route('/img/<img_id>')
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

app.run(port= 8000)
