import numpy as np

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.datasets import load_iris
from sklearn.cluster import AgglomerativeClustering


def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)


iris = load_iris()
X = iris.data

# Creazione e addestramento del modello
model = AgglomerativeClustering(distance_threshold=0, n_clusters=None)                      # distance_threshold=0: costruisce l’intero albero dei cluster senza fermarsi a un numero specifico 
                                                                                            # n_clusters=None: non fissa il numero di cluster, lascia che il modello costruisca una gerarchia completa
model = model.fit(X)
plt.title("Hierarchical Clustering Dendrogram")


# plot the top three levels of the dendrogram
plot_dendrogram(model, truncate_mode="level", p=3)                                          # taglia il dendrogramma a 3 livelli
plt.xlabel("Number of points in node (or index of point if no parenthesis).")
plt.show()