import nltk

from textProcessing import TextProcess
from vectorizing import Vectoriz
from clustering import Cluster
import numpy as np
from collections import Counter
from sklearn.neighbors import NearestNeighbors
from configs import *

import time


class Workspace:
    def __init__(self, name , src_data):
        self.name = name
        self.src_data = src_data
        self.set_default_options()

    def set_default_options(self):
        text_processing_options = TEXTPROCES_DEFAULT
        vectorization_options = VECTOR_DEFAULT
        clustering_options = CLUSTER_DEFAULT
        self.set_text_processing_options(text_processing_options)
        self.set_vectorization_options(vectorization_options)
        self.set_clustering_options(clustering_options)


#TODO CHECK exeptions on sets. mb problem in dialog windows

    def set_text_processing_options(self, options):
        # if ok
        self.text_processing_options = options
        self.apply_text_process()
        self.freq_analys()
        self.length_analys()

    def set_vectorization_options(self, options):
        # if ok
        self.vectorization_options = options
        self.apply_vectorize()
        self.k_nears()

    def set_clustering_options(self, options):
        # if ok
        self.clustering_options = options

    def freq_analys(self):
        try:
            startTime = time.time()
            data = ' '.join(self.nlp_data)
            words = nltk.word_tokenize(data)
            # words = [word.lower() for word in words]
            # words = [word for word in words if word.isalnum()]
            word_freq = Counter(words)
            words_counts_sorted = word_freq.most_common()
            self.words_sorted = [word_count[0] for word_count in words_counts_sorted]
            self.counts_sorted = [word_count[1] for word_count in words_counts_sorted]
            endTime = time.time()
            print("text freq_analys OK = ", endTime - startTime)
        except Exception as e:
         print("Error during text freq_analys:", e)

    def length_analys(self):
        try:
            startTime = time.time()
            word_counts = [len(nltk.word_tokenize(el)) for el in self.nlp_data]
            self.max_size = max(word_counts) + 1
            self.lengths = [0] * (self.max_size + 1)
            for count in word_counts:
                self.lengths[count] += 1
            endTime = time.time()
            print("text length_analys OK = ", endTime - startTime)

        except Exception as e:
           print("Error during text length_analys:", e)

    def k_nears(self):
        # https://stackoverflow.com/questions/15050389/estimating-choosing-optimal-hyperparameters-for-dbscan
        try:
            startTime = time.time()
            X = self.vectorization_text
            # k = 2 * X.shape[-1] - 1  # k = 2 * {dim(dataset)} - 1
            k = 4
            nbrs = NearestNeighbors(n_neighbors=k, algorithm='ball_tree').fit(X)
            distances, indices = nbrs.kneighbors(X)
            distances = np.sort(distances, axis=0)
            distances = distances[:, k - 1]
            self.k_dist = distances
            endTime = time.time()
            print("text k_nears OK = ", endTime - startTime)
        except Exception as e:
          print("Error during k_nears:", e)

    def apply(self):
        print("Start build on : " , self.name , "(" , self ,  ")")
        startTime = time.time()
        print("Applying options: ")
        print("text:" , self.text_processing_options)
        print("vector:" , self.vectorization_options)
        print("cluster:" , self.clustering_options)

        self.nlp = TextProcess(self.text_processing_options)
        self.vectorization = Vectoriz(self.vectorization_options)
        self.clustering = Cluster(self.clustering_options)
        self.apply_text_process()
        self.apply_vectorize()
        self.apply_clustering()
        endTime = time.time()
        print("Build complete by time: " , endTime - startTime)


    def apply_text_process(self):
        self.nlp = TextProcess(self.text_processing_options)
        try:
            self.nlp_data = [self.nlp.fit(el) for el in self.src_data if self.nlp.fit(el).strip()]
            print("Text processing = OK")
        except Exception as e:
            print("Error during text processing:", e)

    def apply_vectorize(self):
        self.vectorization = Vectoriz(self.vectorization_options)
        try:
            self.vectorization_text = self.vectorization.fit(self.nlp_data)
            print("Vectorization = OK")
            print("Testing...")
            print("###############################################")
            self.vectorization.check_model_quality(self.nlp_data)
            print("###############################################")
        except Exception as e:
            print("Error during vectorization:", e)

    def apply_clustering(self):
        self.clustering = Cluster(self.clustering_options)
        try:
            self.clustering_text = self.clustering.fit(self.vectorization_text)
            print("Clusterization = OK")
        except Exception as e:
            print("Error during clustering:", e)
        try:
            self.clustering_centrs = self.clustering.get_cluster_centers(self.vectorization_text)
            self.clustering_centrs_color = np.unique(self.clustering_text)
            print("Cluster Centrs Find = OK")
        except Exception as e:
            print("Error during Cluster Centrs Find:", e)
        try:
            self.clustering_centrs_name = self.vectorization.get_points_name(self.clustering_centrs)
            print(self.clustering_centrs_name)
            print("Name Cluster Centr Named = OK")
        except Exception as e:
            print("Error during Cluster Centrs Name:", e)