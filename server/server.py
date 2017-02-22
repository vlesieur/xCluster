#!/usr/bin/python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import zerorpc
import coclust
from coclust.coclustering import CoclustInfo
from sklearn.datasets import fetch_20newsgroups
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.cluster import normalized_mutual_info_score

from coclust.visualization import plot_reorganized_matrix
from scipy.io import loadmat
from coclust.coclustering import CoclustMod

import signal
import sys
import zerorpc
import time
import os
from datetime import datetime

def getDateTimeNowString():
    string = datetime.now().strftime("%Y %m %d %H %M %S %f")
    return string

def exit_handler(signal, frame):
    print("You are now leaving the Python sector.")
    sys.exit(0)


class Api(object):

    def hello(self, name):
        print('hello appel le : %s' % getDateTimeNowString())
        return 'Hello, %s' % name

    def coclustMod(self, username, path):
        print('coclustMod appel le : %s' % getDateTimeNowString())
        file_name = 'tmp/%s/%s' % (username, path)
        matlab_dict = loadmat(file_name)
        X = matlab_dict['fea']
        model = CoclustMod(n_clusters=4)
        model.fit(X)
        predicted_row_labels = model.row_labels_
        predicted_column_labels = model.column_labels_
        row_indices = np.argsort(model.row_labels_)
        col_indices = np.argsort(model.column_labels_)
        X_reorg = X[row_indices, :]
        X_reorg = X_reorg[:, col_indices]
        plt.spy(X_reorg, precision=0.8, markersize=0.9)
        file_path = '%s\\tmp\\%s\\%s.png' % (os.getcwd(), username, int(time.time()))
        plt.savefig(file_path)
        plt.close()
        return [predicted_row_labels, predicted_column_labels, file_path]

signal.signal(signal.SIGINT, exit_handler)

try:
    server = zerorpc.Server(Api(), heartbeat=360)
    bindingData = "{0}:{1}".format("tcp://0.0.0.0", 4242)
    server.bind(bindingData)
    print("RPC Channels Server ecoute sur : {0}".format(bindingData))
    server.run()
except Exception as e:
    print(str(e))
