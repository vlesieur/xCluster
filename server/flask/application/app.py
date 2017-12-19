# coding: utf-8
"""
Python Flask backend pour xCLuster
"""
# Ressources génériques
import datetime
import json
import os
import shutil
import stat
import zipfile

# Ressources WebServices
from flask import Flask, make_response, request, current_app, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from mongokit import Connection, Document
from datetime import timedelta
from functools import update_wrapper

from .models import Users
from index import app, db
from .utils.auth import generate_token, requires_auth, verify_token

# Ressources Coclust
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import numpy as np
import zerorpc
import coclust
from sklearn.datasets import fetch_20newsgroups
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.preprocessing import normalize
from coclust.visualization import plot_reorganized_matrix
from scipy.io import loadmat
from coclust.coclustering import CoclustMod, CoclustSpecMod, CoclustInfo
from coclust.io.data_loading import load_doc_term_data
from coclust.visualization import (plot_reorganized_matrix, plot_cluster_top_terms, plot_max_modularities)
from coclust.evaluation.internal import best_modularity_partition

# Configuration
ROOT=os.path.abspath(os.getcwd()+'../../../front/angular-seed/app/storage/users')
SHOW_DOTFILES=True

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

@app.route('/copy', methods = ['POST', 'OPTIONS'])
@crossdomain(origin="*")	
def copy():
    try:
        items = request['items']
        if len(items) == 1 and 'singleFilename' in request:
            src = os.path.abspath(ROOT + items[0])
            dst = os.path.abspath(ROOT + request['singleFilename'])
            if not (os.path.exists(src) and src.startswith(ROOT) and dst.startswith(ROOT)):
                return {'result': jsonify({'success': 'false', 'error': 'File not found'}})

            shutil.move(src, dst)
        else:
            path = os.path.abspath(ROOT + request['newPath'])
            for item in items:
                src = os.path.abspath(ROOT + item)
                if not (os.path.exists(src) and src.startswith(ROOT) and path.startswith(ROOT)):
                    return jsonify({'result': {'success': 'false', 'error': 'Invalid path'}})

                shutil.move(src, path)
    except Exception as e:
        return jsonify({'result': {'success': 'false', 'error': e.message}})

    return jsonify({'result': {'success': 'true', 'error': ''}})

@app.route('/remove', methods = ['POST', 'OPTIONS'])
@crossdomain(origin="*")
def remove():
    try:
        items = request['items']
        for item in items:
            path = os.path.abspath(ROOT + item)
            if not (os.path.exists(path) and path.startswith(ROOT)):
                return jsonify({'result': {'success': 'false', 'error': 'Invalid path'}})

            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    except Exception as e:
        return jsonify({'result': {'success': 'false', 'error': e.message}})

    return jsonify({'result': {'success': 'true', 'error': ''}})

@app.route('/edit', methods = ['POST', 'PUT', 'OPTIONS'])
@crossdomain(origin="*")
def edit():
    try:
        path = os.path.abspath(ROOT + request['item'])
        if not path.startswith(ROOT):
            return jsonify({'result': {'success': 'false', 'error': 'Invalid path'}})

        content = request['content']
        with open(path, 'w') as f:
            f.write(content)
    except Exception as e:
        return jsonify({'result': {'success': 'false', 'error': e.message}})

    return jsonify({'result': {'success': 'true', 'error': ''}})

@app.route('/read', methods = ['GET', 'OPTIONS'])
@crossdomain(origin="*")
def getContent():
    try:
        path = os.path.abspath(ROOT + request['item'])
        if not path.startswith(ROOT):
            return jsonify({'result': {'success': 'false', 'error': 'Invalid path'}})

        with open(path, 'r') as f:
            content = f.read()
    except Exception as e:
        content = e.message

    return {'result': content}
	
@app.route('/folder', methods = ['POST', 'OPTIONS'])
@crossdomain(origin="*")
def createFolder():
    try:
        path = os.path.abspath(ROOT + request['newPath'])
        if not path.startswith(ROOT):
            return jsonify({'result': {'success': 'false', 'error': 'Invalid path'}})

        os.makedirs(path)
    except Exception as e:
        return jsonify({'result': {'success': 'false', 'error': e.message}})

    return jsonify({'result': {'success': 'true', 'error': ''}})

@app.route('/permissions', methods = ['POST', 'OPTIONS'])
@crossdomain(origin="*")
def changePermissions():
    try:
        items = request['items']
        permissions = int(request['perms'], 8)
        recursive = request['recursive']
        print('recursive: {}, type: {}'.format(recursive, type(recursive)))
        for item in items:
            path = os.path.abspath(ROOT + item)
            if not (os.path.exists(path) and path.startswith(ROOT)):
                return jsonify({'result': {'success': 'false', 'error': 'Invalid path'}})

            if recursive == 'true':
                change_permissions_recursive(path, permissions)
            else:
                os.chmod(path, permissions)
    except Exception as e:
        return jsonify({'result': {'success': 'false', 'error': e.message}})

    return jsonify({'result': {'success': 'true', 'error': ''}})

@app.route('/compress', methods = ['POST', 'OPTIONS'])
@crossdomain(origin="*")
def compress():
    try:
        items = request['items']
        path = os.path.abspath(os.path.join(ROOT + request['destination'], request['compressedFilename']))
        if not path.startswith(ROOT):
            return jsonify({'result': {'success': 'false', 'error': 'Invalid path'}})

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
        return jsonify({'result': {'success': 'false', 'error': e.message}})

    return jsonify({'result': {'success': 'true', 'error': ''}})

@app.route('/extract', methods = ['POST', 'OPTIONS'])
@crossdomain(origin="*")
def extract():
    try:
        src = os.path.abspath(ROOT + request['item'])
        dst = os.path.abspath(ROOT + request['destination'])
        if not (os.path.isfile(src) and src.startswith(ROOT) and dst.startswith(ROOT)):
            return jsonify({'result': {'success': 'false', 'error': 'Invalid path'}})

        zip_file = zipfile.ZipFile(src, 'r')
        zip_file.extractall(dst)
        zip_file.close()
    except Exception as e:
        return jsonify({'result': {'success': 'false', 'error': e.message}})

    return jsonify({'result': {'success': 'true', 'error': ''}})

@app.route('/upload', methods = ['POST', 'OPTIONS'])
@crossdomain(origin="*")
def upload():
    try:
        destination = handler.get_body_argument('destination', default='/')
        for name in handler.request.files:
            fileinfo = handler.request.files[name][0]
            filename = fileinfo['filename']
            path = os.path.abspath(os.path.join(ROOT, destination, filename))
            if not path.startswith(ROOT):
                return jsonify({'result': {'success': 'false', 'error': 'Invalid path'}})
            with open(path, 'wb') as f:
                f.write(fileinfo['body'])
    except Exception as e:
        return jsonify({'result': {'success': 'false', 'error': e.message}})

    return jsonify({'result': {'success': 'true', 'error': ''}})

@app.route('/download', methods = ['POST', 'OPTIONS'])
@crossdomain(origin="*")
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
Coclust fonctions
"""

def getDateTimeNowString():
    string = datetime.now().strftime("%Y %m %d %H %M %S %f")
    return string

def exit_handler(signal, frame):
    print("You are now leaving the Python sector.")
    sys.exit(0)

#############################################################################
# COCLUST MOD
# Parameters:	
# n_clusters (int, optional, default: 2) – Number of co-clusters to form
# init (numpy array or scipy sparse matrix, shape (n_features, n_clusters), optional, default: None) – Initial column labels
# max_iter (int, optional, default: 20) – Maximum number of iterations
# n_init (int, optional, default: 1) – Number of time the algorithm will be run with different initializations. The final results will be the best output of n_init consecutive runs in terms of modularity.
# random_state (integer or numpy.RandomState, optional) – The generator used to initialize the centers. If an integer is given, it fixes the seed. Defaults to the global numpy random number generator.
# tol (float, default: 1e-9) – Relative tolerance with regards to modularity to declare convergence
#############################################################################

def coclustMod(self, path, original_file_name, n_clusters=2, init=None, max_iter=20, n_init=1, random_state=np.random.RandomState, tol=1e-9, dictionnaire='doc_term_matrix',  label_matrix="term_labels", n_terms=0):
    plt.cla()
    plt.clf()
    print('coclustMod appel le : %s' % getDateTimeNowString())
    original_file_path = '../front/angular-seed/app/storage/users/%s/%s' % (path, original_file_name)
    matlab_dict = loadmat(original_file_path)
    X = matlab_dict[dictionnaire]
    model = CoclustMod(
        n_clusters=n_clusters,
        init=init,
        max_iter=max_iter,
        n_init=n_init,
        random_state=random_state,
        tol=tol
        )
    model.fit(X)
    predicted_row_labels = model.row_labels_
    predicted_column_labels = model.column_labels_
    row_indices = np.argsort(model.row_labels_)
    col_indices = np.argsort(model.column_labels_)
    X_reorg = X[row_indices, :]
    X_reorg = X_reorg[:, col_indices]
    size = model.n_clusters  * 2.7
    plt.subplots(figsize = (size, size))
    plt.subplots_adjust(hspace = 0.200)
    plt.spy(X_reorg, precision=0.8, markersize=0.9)
    file_name ='%s-mod-%s' % (original_file_name.split(".",1)[0], int(time.time()))
    file_path = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s.png' % (os.getcwd(), path.replace("/", "\\"), file_name)
    plt.tick_params(axis='both', which='both', bottom='off', top='off',right='off', left='off')
    plt.savefig(file_path)
    plt.cla()
    plt.clf()
    rowArray = np.asarray(predicted_row_labels);
    columnArray = np.asarray(predicted_column_labels);
    csv_path_row = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s-rowLabels.csv' % (os.getcwd(), path.replace("/", "\\"), file_name)
    csv_path_col = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s-columnLabels.csv' % (os.getcwd(), path.replace("/", "\\"), file_name)
    np.savetxt(csv_path_row, rowArray, delimiter=";")
    np.savetxt(csv_path_col, columnArray, delimiter=";")
    new_file_path = '%s/%s' % (path, file_name)
    
    if n_terms > 0:
        top_terms_file_path = self.coclustFormat(path, original_file_name, model , n_terms, dictionnaire, label_matrix, 'mod');
        return [predicted_row_labels, predicted_column_labels, new_file_path, top_terms_file_path]

    return [predicted_row_labels, predicted_column_labels, new_file_path, None]

def coclustSpecMod(self, path, original_file_name, n_clusters=2, init=None, max_iter=20, n_init=1, random_state=np.random.RandomState, tol=1e-9, dictionnaire='doc_term_matrix',  label_matrix="term_labels", n_terms=0 ):
    plt.cla()
    plt.clf()
    print('coclustSpecMod appel le : %s' % getDateTimeNowString())
    original_file_path = '../front/angular-seed/app/storage/users/%s/%s' % (path, original_file_name)
    matlab_dict = loadmat(original_file_path)
    X = matlab_dict[dictionnaire]
    model = CoclustSpecMod(
        n_clusters=n_clusters,
        max_iter=max_iter,
        n_init=n_init,
        random_state=random_state,
        tol=tol
        )
    model.fit(X)
    predicted_row_labels = model.row_labels_
    predicted_column_labels = model.column_labels_
    row_indices = np.argsort(model.row_labels_)
    col_indices = np.argsort(model.column_labels_)
    X_reorg = X[row_indices, :]
    X_reorg = X_reorg[:, col_indices]
    size = model.n_clusters  * 2.7
    plt.subplots(figsize = (size, size))
    plt.subplots_adjust(hspace = 0.200)
    plt.spy(X_reorg, precision=0.8, markersize=0.9)
    file_name ='%s-spec-%s' % (original_file_name.split(".",1)[0], int(time.time()))
    file_path = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s.png' % (os.getcwd(), path.replace("/", "\\"), file_name)
    plt.tick_params(axis='both', which='both', bottom='off', top='off',right='off', left='off')
    plt.savefig(file_path)
    plt.cla()
    plt.clf()
    rowArray = np.asarray(predicted_row_labels);
    columnArray = np.asarray(predicted_column_labels);
    csv_path_row = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s-rowLabels.csv' % (os.getcwd(), path.replace("/", "\\"), file_name)
    csv_path_col = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s-columnLabels.csv' % (os.getcwd(), path.replace("/", "\\"), file_name)
    np.savetxt(csv_path_row, rowArray, delimiter=";")
    np.savetxt(csv_path_col, columnArray, delimiter=";")
    new_file_path = '%s/%s' % (path, file_name)
    
    if n_terms > 0:
        top_terms_file_path = self.coclustFormat(path, original_file_name, model , n_terms, dictionnaire, label_matrix, 'spec');
        return [predicted_row_labels, predicted_column_labels, new_file_path, top_terms_file_path]        

    return [predicted_row_labels, predicted_column_labels, new_file_path, None]
    
def coclustInfo(self, path, original_file_name, n_row_clusters=2, n_col_clusters=2, init=None, max_iter=20, n_init=1, tol=1e-9, random_state=None, dictionnaire='doc_term_matrix', label_matrix="term_labels", n_terms=0):
    plt.cla()
    plt.clf()
    print('coclustInfo appel le : %s' % getDateTimeNowString())
    original_file_path = '../front/angular-seed/app/storage/users/%s/%s' % (path, original_file_name)
    matlab_dict = loadmat(original_file_path)
    X = matlab_dict[dictionnaire]
    model = CoclustInfo(
        n_row_clusters=n_row_clusters,
        n_col_clusters=n_col_clusters,
        init=init,
        n_init=n_init,
        random_state=random_state,
        tol=tol
        )
    model.fit(X)
    predicted_row_labels = model.row_labels_
    predicted_column_labels = model.column_labels_
    row_indices = np.argsort(model.row_labels_)
    col_indices = np.argsort(model.column_labels_)
    X_reorg = X[row_indices, :]
    X_reorg = X_reorg[:, col_indices]
    size = model.n_clusters  * 2.7
    plt.subplots(figsize = (size, size))
    plt.subplots_adjust(hspace = 0.200)
    plt.spy(X_reorg, precision=0.8, markersize=0.9)
    file_name ='%s-info-%s' % (original_file_name.split(".",1)[0], int(time.time()))
    file_path = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s.png' % (os.getcwd(), path.replace("/", "\\"), file_name)
    plt.tick_params(axis='both', which='both', bottom='off', top='off',right='off', left='off')
    plt.savefig(file_path)
    plt.cla()
    plt.clf()
    rowArray = np.asarray(predicted_row_labels);
    columnArray = np.asarray(predicted_column_labels);
    csv_path_row = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s-rowLabels.csv' % (os.getcwd(), path.replace("/", "\\"), file_name)
    csv_path_col = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s-columnLabels.csv' % (os.getcwd(), path.replace("/", "\\"), file_name)
    np.savetxt(csv_path_row, rowArray, delimiter=";")
    np.savetxt(csv_path_col, columnArray, delimiter=";")
    new_file_path = '%s/%s' % (path, file_name)

    n_terms = n_terms

    if n_terms > 0:
        top_terms_file_path = self.coclustFormat(path, original_file_name, model , n_terms, dictionnaire, label_matrix, 'info');
        return [predicted_row_labels, predicted_column_labels, new_file_path, top_terms_file_path]

    return [predicted_row_labels, predicted_column_labels, new_file_path, None]

def createUserDirectory(self, username, mode=0777):
    directory = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s' % (os.getcwd(), username)
    if not os.path.exists(directory) and not os.path.isdir(directory) :
        os.mkdir(directory, mode)
    success = os.path.exists(directory) and os.path.isdir(directory)
    return success

def coclustFormat(self, path, original_file_name,  model, n_terms, matrix, label_matrix, method):
    print('generation des tops terms appel le : %s/%s' % (path, original_file_name))
    original_file_path = '../front/angular-seed/app/storage/users/%s/%s' % (path, original_file_name)
    
    plt.style.use('ggplot')

    # read data
    doc_term_data = load_doc_term_data(original_file_path)
    X = doc_term_data[matrix]
    labels = doc_term_data[label_matrix]
    logger.info(labels)

    # get the best co-clustering over a range of cluster numbers
    clusters_range = range(2, 6)

    # plot the top terms
    n_terms = n_terms

    # REECRITURE DE LA FONCTION POUR SAUVEGARDER LE FICHIER
    # plot_cluster_top_terms(X, labels, n_terms, model)

    if labels is None:
        logger.warning("Term labels cannot be found. Use input argument "
        "'term_labels_filepath' in function "
        "'load_doc_term_data' if term labels are available.")

    x_label = "number of occurences"
    size = (model.n_clusters + n_terms) * 0.7
    plt.subplots(figsize = (size, size))
    plt.subplots_adjust(hspace = 0.200)
    plt.suptitle("Top %d terms" % n_terms, size = 15)
    number_of_subplots = model.n_clusters

    for i, v in enumerate(range(number_of_subplots)): #Get the row / col indices corresponding to the given cluster
        row_indices, col_indices = model.get_indices(v)# Get the submatrix corresponding to the given cluster
        cluster = model.get_submatrix(X, v)# Count the number of each term
        p = cluster.sum(0)
        t = p.getA().flatten()
        # Obtain all term names for the given cluster
        tmp_terms = np.array(labels)[col_indices]
        # Get the first n terms
        max_indices = t.argsort()[::-1][: n_terms]
        
        pos = np.arange(n_terms)
        
        v = v + 1
        ax1 = plt.subplot(number_of_subplots, 1, v)
        ax1.barh(pos, t[max_indices][::-1])
        ax1.set_title("Cluster %d (%d terms)" % (v, len(col_indices)), size = 11)

        plt.yticks(.4 + pos, tmp_terms[max_indices][::-1], size = 9.5)
        plt.xlabel(x_label, size = 9)
        plt.margins(y = 0.05)# _remove_ticks()
        plt.tick_params(axis = 'both', which = 'both', bottom = 'on', top = 'off',
            right = 'off', left = 'off')

    # Tight layout often produces nice results# but requires the title to be spaced accordingly
    plt.tight_layout()
    plt.subplots_adjust(top = 0.88)

    file_name ='%s-%s-%s-%s' % (original_file_name.split(".",1)[0], method, 'topTerms', int(time.time()))
    file_path = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s.svg' % (os.getcwd(), path.replace("/", "\\"), file_name)
    plt.tick_params(axis='both', which='both', bottom='off', top='off',right='off', left='off')
    plt.savefig(file_path, format = 'svg')
    plt.cla()
    plt.clf()

    new_file_path = '%s/%s' % (path, file_name)

    return new_file_path


"""
Lancement du serveur Flask
"""

# app.run(host='0.0.0.0', port= 8090)

@app.route("/api/user", methods=["GET"])
@requires_auth
def get_user():
    return jsonify(result=g.current_user)


@app.route("/api/create_user", methods=["POST"])
def create_user():
    try:
        incoming = request.get_json()
        email = incoming['email']
        password = incoming['password']
    except:
        return jsonify()
    if not email or not password:
        return jsonify(message="Users with that email already exists"), 409
    u = Users(email=email, password=password)
    try:
        u.save()
    except db.NotUniqueError:
        return jsonify(message="Email already exists"), 409
    except db.ValidationError:
        return jsonify(message="Email format incorrect "), 409
    new_user = Users.objects.get(email=email)
    return jsonify(
        token=generate_token(new_user)
    )


@app.route("/api/authenticate", methods=["POST", "OPTIONS"])
@crossdomain(origin="*")
def get_token():
    incoming = request.get_json();
    user = Users.get_user_with_login_and_password(incoming["login"], incoming["password"])
    if user:
        token=generate_token(user)
        return jsonify({'success':True, 'token': token})

    return jsonify({ 'success': False, 'msg': 'Echec de l\'authentification. Login ou mot de passe invalide.' }), 200


@app.route("/api/is_token_valid", methods=["POST"])
@crossdomain(origin="*")
def is_token_valid():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(token_is_valid=True)
    else:
        return jsonify(token_is_valid=False), 403