#!/usr/bin/python
import os
import sys
import hashlib
import webbrowser
from flask import Flask, render_template, send_file
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.CRITICAL)

webbrowser.get(
    "/usr/bin/chromium-browser %s").open_new("http://localhost:8000")

img_suffixes = [".bmp", ".png", ".jpg", ".jpeg"]


def get_id_from_path(path_to_image):
    basename = os.path.basename(path_to_image)
    all_numbers = [char for char in basename if char.isdigit()]
    str_id = ''.join(all_numbers)
    return str_id


def keep_only_similar_images(paths_1, paths_2):
    # To optimise
    first_ids = [get_id_from_path(path) for path in paths_1]
    second_ids = [get_id_from_path(path) for path in paths_2]
    to_keep_ids = set(first_ids) & set(second_ids)

    filtered_paths_1 = []
    filtered_paths_2 = []

    for i, ids in enumerate(first_ids):
        if ids in to_keep_ids:
            filtered_paths_1.append(paths_1[i])
    for i, ids in enumerate(second_ids):
        if ids in to_keep_ids:
            filtered_paths_2.append(paths_2[i])
    return filtered_paths_1, filtered_paths_2


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

first_files, second_files = keep_only_similar_images(first_files,
                                                     second_files)


@app.route('/favicon.ico')
def favicon():
    return ''


@app.route('/img/<img_id>')
def img_comp(img_id):
    index = int(img_id)
    file_1 = first_files[index]
    file_2 = second_files[index]
    hasher1 = hashlib.md5()
    with open(file_1, 'rb') as f1:
        hasher1.update(f1.read())
    hasher2 = hashlib.md5()
    with open(file_2, 'rb') as f2:
        hasher2.update(f2.read())
    return render_template('image_diff.html',
                           file_1=file_1,
                           file_2=file_2,
                           hash_1=hasher1.hexdigest(),
                           hash_2=hasher2.hexdigest(),
                           index=index)


@app.route('/')
def index():
    return img_comp('0')


@app.route('/media', defaults={'path': ''})
@app.route('/media/<path:path>')
def serve_images(path):
    return send_file('/' + path, mimetype='image/x-windows-bmp')

app.run(port=8000)
