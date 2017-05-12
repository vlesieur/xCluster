#!/usr/bin/python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import numpy as np
import zerorpc
import coclust

from sklearn.datasets import fetch_20newsgroups
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.preprocessing import normalize

from coclust.visualization import plot_reorganized_matrix
from scipy.io import loadmat
from coclust.coclustering import CoclustMod
from coclust.coclustering import CoclustSpecMod
from coclust.coclustering import CoclustInfo
from coclust.io.data_loading import load_doc_term_data
from coclust.visualization import (plot_reorganized_matrix, plot_cluster_top_terms, plot_max_modularities)
from coclust.evaluation.internal import best_modularity_partition

import signal
import sys
import zerorpc
import time
import os
from datetime import datetime

import logging
logging.basicConfig()

logger = logging.getLogger(__name__)


def getDateTimeNowString():
    string = datetime.now().strftime("%Y %m %d %H %M %S %f")
    return string

def exit_handler(signal, frame):
    print("You are now leaving the Python sector.")
    sys.exit(0)


class Api(object):

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
        print('coclustMod appel le : %s/%s' % (path, original_file_name))
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
        plt.spy(X_reorg, precision=0.8, markersize=0.9)
        file_name ='%s-%s' % (original_file_name.split(".",1)[0], int(time.time()))
        file_path = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s.png' % (os.getcwd(), path.replace("/", "\\"), file_name)
        plt.tick_params(axis='both', which='both', bottom='off', top='off',right='off', left='off')
        plt.savefig(file_path)
        plt.close()
        modMatrix = np.asarray(X_reorg);
        csv_path = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s.csv' % (os.getcwd(), path.replace("/", "\\"), file_name)
        # np.savetxt(csv_path, modMatrix, delimiter=";")
        new_file_path = '%s/%s' % (path, file_name)
        
        if n_terms > 0:
            top_terms_file_path = self.coclustFormat(path, original_file_name, model , n_terms, dictionnaire, label_matrix);
            return [predicted_row_labels, predicted_column_labels, new_file_path, top_terms_file_path]

        return [predicted_row_labels, predicted_column_labels, new_file_path, None]

    def coclustSpecMod(self, path, original_file_name, n_clusters=2, init=None, max_iter=20, n_init=1, random_state=np.random.RandomState, tol=1e-9, dictionnaire='doc_term_matrix',  label_matrix="term_labels", n_terms=0 ):
        print('coclustSpecMod appel le : %s/%s' % (path, original_file_name))
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
        plt.spy(X_reorg, precision=0.8, markersize=0.9)
        file_name ='%s-%s' % (original_file_name.split(".",1)[0], int(time.time()))
        file_path = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s.png' % (os.getcwd(), path.replace("/", "\\"), file_name)
        plt.tick_params(axis='both', which='both', bottom='off', top='off',right='off', left='off')
        plt.savefig(file_path)
        plt.close()
        specMatrix = np.asarray(X_reorg);
        csv_path = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s.csv' % (os.getcwd(), path.replace("/", "\\"), file_name)
        np.savetxt(csv_path, specMatrix, delimiter=";")
        new_file_path = '%s/%s' % (path, file_name)
        
        if n_terms > 0:
            top_terms_file_path = self.coclustFormat(path, original_file_name, model , n_terms, dictionnaire, label_matrix);
            return [predicted_row_labels, predicted_column_labels, new_file_path, top_terms_file_path]        

        return [predicted_row_labels, predicted_column_labels, new_file_path, None]
		
    def coclustInfo(self, path, original_file_name, n_row_clusters=2, n_col_clusters=2, init=None, max_iter=20, n_init=1, tol=1e-9, random_state=None, dictionnaire='doc_term_matrix', label_matrix="term_labels", n_terms=0):
        print('coclustInfo appel le : %s/%s' % (path, original_file_name))
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
        plt.spy(X_reorg, precision=0.8, markersize=0.9)
        file_name ='%s-%s' % (original_file_name.split(".",1)[0], int(time.time()))
        file_path = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s.png' % (os.getcwd(), path.replace("/", "\\"), file_name)
        plt.tick_params(axis='both', which='both', bottom='off', top='off',right='off', left='off')
        plt.savefig(file_path)
        plt.close()
        infoMatrix = np.asarray(X_reorg);
        csv_path = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s.csv' % (os.getcwd(), path.replace("/", "\\"), file_name)
        np.savetxt(csv_path, infoMatrix, delimiter=";")
        new_file_path = '%s/%s' % (path, file_name)

        n_terms = n_terms

        if n_terms > 0:
            top_terms_file_path = self.coclustFormat(path, original_file_name, model , n_terms, dictionnaire, label_matrix);
            return [predicted_row_labels, predicted_column_labels, new_file_path, top_terms_file_path]

        return [predicted_row_labels, predicted_column_labels, new_file_path, None]

    def createUserDirectory(self, username, mode=0777):
        directory = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s' % (os.getcwd(), username)
        if not os.path.exists(directory) and not os.path.isdir(directory) :
            os.mkdir(directory, mode)
        success = os.path.exists(directory) and os.path.isdir(directory)
        return success

    def coclustFormat(self, path, original_file_name,  model, n_terms, matrix, label_matrix):
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
        plt.subplots(figsize = (8, 8))
        plt.subplots_adjust(hspace = 0.200)
        plt.suptitle("      Top %d terms" % n_terms, size = 15)
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

        file_name ='%s-%s-%s' % (original_file_name.split(".",1)[0],'topTerms', int(time.time()))
        file_path = '%s\\..\\front\\angular-seed\\app\\storage\\users\\%s\\%s.png' % (os.getcwd(), path.replace("/", "\\"), file_name)
        plt.tick_params(axis='both', which='both', bottom='off', top='off',right='off', left='off')
        plt.savefig(file_path)
        plt.close()

        new_file_path = '%s/%s' % (path, file_name)

        return new_file_path

signal.signal(signal.SIGINT, exit_handler)

try:
    server = zerorpc.Server(Api(), heartbeat=360)
    bindingData = "{0}:{1}".format("tcp://0.0.0.0", 4242)
    server.bind(bindingData)
    print("RPC Channels Server ecoute sur : {0}".format(bindingData))
    server.run()
except Exception as e:
    logger.warning(str(e))
    print(str(e))
