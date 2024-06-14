from sklearn.cluster import DBSCAN, KMeans
import os
import numpy as np
os.environ["LOKY_MAX_CPU_COUNT"] = "10"


class Cluster:
    def __init__(self, options):
        self.method = options.get('method', 'dbscan')
        self.options = options
        self.model = None

    def fit(self, points):
        if self.method == 'dbscan':
            eps = self.options.get('epsilon', 0.5)
            min_samples = self.options.get('minpts', 1)
            self.model = DBSCAN(eps=float(eps), min_samples=min_samples)
        elif self.method == 'k-means':
            n_clusters = self.options.get('num_clusters', 25)
            # n_init = self.options.get('max_iterations', 10)
            self.model = KMeans(n_clusters=n_clusters, n_init=10)
        else:
            raise ValueError("Unsupported method. Choose 'dbscan' or 'k-means'.")
        self.model.fit(points)
        return self.model.labels_

    def get_cluster_centers(self, points):
        if self.method == 'k-means':
            return self.model.cluster_centers_
        elif self.method == 'dbscan':
            unique_labels = np.unique(self.model.labels_)
            cluster_centers = []
            for label in unique_labels:
                cluster_points = points[self.model.labels_ == label]
                cluster_center = np.mean(cluster_points, axis=0)
                cluster_centers.append(cluster_center)
            return np.array(cluster_centers)
        else:
            raise ValueError("Unsupported method. Choose 'dbscan' or 'k-means'.")


