# coding: utf-8
"""
Python Flask backend pour xCLuster
"""

import datetime
import json
import os
import shutil
import stat
import zipfile

from flask import Flask, make_response, request, current_app, jsonify
from mongokit import Connection, Document
from datetime import timedelta
from functools import update_wrapper

# Configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DATABASE = 'xclusterdb'
ROOT=os.path.abspath(os.getcwd()+'../../../front/angular-seed/app/storage/users')
SHOW_DOTFILES=True
SECRET = 'jf1G2tZvFc74yetoo1ElmrFUT3UN91ZS'

# Application
app = Flask(__name__)
app.config.from_object(__name__)

# Connexion à la base de données MongoDB
connection = Connection(app.config['MONGODB_HOST'],
                        app.config['MONGODB_PORT'])

"""
Decorateur
"""
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Authorization'
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

"""
Fonctions de base
"""
def timestamp_to_str(timestamp, format_str='%Y-%m-%d %I:%M:%S'):
    date = datetime.datetime.fromtimestamp(timestamp)
    return date.strftime(format_str)


def filemode(mode):
    is_dir = 'd' if stat.S_ISDIR(mode) else '-'
    dic = {'7': 'rwx', '6': 'rw-', '5': 'r-x', '4': 'r--', '0': '---'}
    perm = str(oct(mode)[-3:])
    return is_dir + ''.join(dic.get(x, x) for x in perm)


def get_file_information(path):
    fstat = os.stat(path)
    if stat.S_ISDIR(fstat.st_mode):
        ftype = 'dir'
    else:
        ftype = 'file'

    fsize = fstat.st_size
    ftime = timestamp_to_str(fstat.st_mtime)
    fmode = filemode(fstat.st_mode)

    return ftype, fsize, ftime, fmode


def change_permissions_recursive(path, mode):
    for root, dirs, files in os.walk(path, topdown=False):
        for d in [os.path.join(root, d) for d in dirs]:
            os.chmod(d, mode)
        for f in [os.path.join(root, f) for f in files]:
            os.chmod(f, mode)

"""
Fonctions métiers
"""
@app.route('/lists', methods = ['POST', 'OPTIONS'])
@crossdomain(origin="*")
def list():
    print('/lists called !')
    json = request.get_json(silent=True)
    path = os.path.abspath(ROOT + json['path'])
    if not os.path.exists(path) or not path.startswith(ROOT):
        return {'result': ''}

    files = []
    for fname in sorted(os.listdir(path)):
        if fname.startswith('.') and not SHOW_DOTFILES:
            continue

        fpath = os.path.join(path, fname)

        try:
            ftype, fsize, ftime, fmode = get_file_information(fpath)
        except Exception as e:
            continue

        files.append({
            'name': fname,
            'rights': fmode,
            'size': fsize,
            'date': ftime,
            'type': ftype,
        })

    return jsonify({'result': files})

@app.route('/rename', methods = ['POST', 'OPTIONS'])
@crossdomain(origin="*")
def rename():
    json = request.get_json(silent=True)
    print('/rename called !')
    try:
        src = os.path.abspath(ROOT + json['item'])
        dst = os.path.abspath(ROOT + json['newItemPath'])
        print('rename {} {}'.format(src, dst))
        if not (os.path.exists(src) and src.startswith(ROOT) and dst.startswith(ROOT)):
            return jsonify({'result': {'success': 'false', 'error': 'Invalid path'}})

        shutil.move(src, dst)
    except Exception as e:
        return jsonify({'result': {'success': 'false', 'error': e.message}})

    return jsonify({'result': {'success': 'true', 'error': ''}})

def copy():
    try:
        items = request['items']
        if len(items) == 1 and 'singleFilename' in request:
            src = os.path.abspath(ROOT + items[0])
            dst = os.path.abspath(ROOT + request['singleFilename'])
            if not (os.path.exists(src) and src.startswith(ROOT) and dst.startswith(ROOT)):
                return {'result': {'success': 'false', 'error': 'File not found'}}

            shutil.move(src, dst)
        else:
            path = os.path.abspath(ROOT + request['newPath'])
            for item in items:
                src = os.path.abspath(ROOT + item)
                if not (os.path.exists(src) and src.startswith(ROOT) and path.startswith(ROOT)):
                    return {'result': {'success': 'false', 'error': 'Invalid path'}}

                shutil.move(src, path)
    except Exception as e:
        return {'result': {'success': 'false', 'error': e.message}}

    return {'result': {'success': 'true', 'error': ''}}

def remove():
    try:
        items = request['items']
        for item in items:
            path = os.path.abspath(ROOT + item)
            if not (os.path.exists(path) and path.startswith(ROOT)):
                return {'result': {'success': 'false', 'error': 'Invalid path'}}

            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    except Exception as e:
        return {'result': {'success': 'false', 'error': e.message}}

    return {'result': {'success': 'true', 'error': ''}}

def edit():
    try:
        path = os.path.abspath(ROOT + request['item'])
        if not path.startswith(ROOT):
            return {'result': {'success': 'false', 'error': 'Invalid path'}}

        content = request['content']
        with open(path, 'w') as f:
            f.write(content)
    except Exception as e:
        return {'result': {'success': 'false', 'error': e.message}}

    return {'result': {'success': 'true', 'error': ''}}

def getContent():
    try:
        path = os.path.abspath(ROOT + request['item'])
        if not path.startswith(ROOT):
            return {'result': {'success': 'false', 'error': 'Invalid path'}}

        with open(path, 'r') as f:
            content = f.read()
    except Exception as e:
        content = e.message

    return {'result': content}

def createFolder():
    try:
        path = os.path.abspath(ROOT + request['newPath'])
        if not path.startswith(ROOT):
            return {'result': {'success': 'false', 'error': 'Invalid path'}}

        os.makedirs(path)
    except Exception as e:
        return {'result': {'success': 'false', 'error': e.message}}

    return {'result': {'success': 'true', 'error': ''}}

def changePermissions():
    try:
        items = request['items']
        permissions = int(request['perms'], 8)
        recursive = request['recursive']
        print('recursive: {}, type: {}'.format(recursive, type(recursive)))
        for item in items:
            path = os.path.abspath(ROOT + item)
            if not (os.path.exists(path) and path.startswith(ROOT)):
                return {'result': {'success': 'false', 'error': 'Invalid path'}}

            if recursive == 'true':
                change_permissions_recursive(path, permissions)
            else:
                os.chmod(path, permissions)
    except Exception as e:
        return {'result': {'success': 'false', 'error': e.message}}

    return {'result': {'success': 'true', 'error': ''}}

def compress():
    try:
        items = request['items']
        path = os.path.abspath(os.path.join(ROOT + request['destination'], request['compressedFilename']))
        if not path.startswith(ROOT):
            return {'result': {'success': 'false', 'error': 'Invalid path'}}

        zip_file = zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED)
        for item in items:
            path = os.path.abspath(ROOT + item)
            if not (os.path.exists(path) and path.startswith(ROOT)):
                continue

            if os.path.isfile(path):
                zip_file.write(path)
            else:
                for root, dirs, files in os.walk(path):
                    for f in files:
                        zip_file.write(
                            f,
                            os.path.relpath(os.path.join(root, f), os.path.join(path, '..'))
                        )

        zip_file.close()
    except Exception as e:
        return {'result': {'success': 'false', 'error': e.message}}

    return {'result': {'success': 'true', 'error': ''}}

def extract():
    try:
        src = os.path.abspath(ROOT + request['item'])
        dst = os.path.abspath(ROOT + request['destination'])
        if not (os.path.isfile(src) and src.startswith(ROOT) and dst.startswith(ROOT)):
            return {'result': {'success': 'false', 'error': 'Invalid path'}}

        zip_file = zipfile.ZipFile(src, 'r')
        zip_file.extractall(dst)
        zip_file.close()
    except Exception as e:
        return {'result': {'success': 'false', 'error': e.message}}

    return {'result': {'success': 'true', 'error': ''}}

def upload():
    try:
        destination = handler.get_body_argument('destination', default='/')
        for name in handler.request.files:
            fileinfo = handler.request.files[name][0]
            filename = fileinfo['filename']
            path = os.path.abspath(os.path.join(ROOT, destination, filename))
            if not path.startswith(ROOT):
                return {'result': {'success': 'false', 'error': 'Invalid path'}}
            with open(path, 'wb') as f:
                f.write(fileinfo['body'])
    except Exception as e:
        return {'result': {'success': 'false', 'error': e.message}}

    return {'result': {'success': 'true', 'error': ''}}

def download():
    path = os.path.abspath(ROOT + path)
    print(path)
    content = ''
    if path.startswith(ROOT) and os.path.isfile(path):
        print(path)
        try:
            with open(path, 'rb') as f:
                content = f.read()
        except Exception as e:
            pass
    return content

"""
Lancement du serveur Flask
"""
app.run(host='0.0.0.0', port= 8090)