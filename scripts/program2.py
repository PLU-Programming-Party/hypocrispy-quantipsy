import pandas as pd
import numpy as np
from openai import OpenAI
# import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from collections import defaultdict
from sklearn.cluster import AgglomerativeClustering

df = pd.read_csv('thedata/embeddings.csv')

quotes = df['quote'][:100].tolist()
embeddings = np.vstack(
    df['quote_embedding'][:100].apply(
        lambda s: np.fromstring(s.strip('[]'), sep=',')
    )
)
print(quotes)
print(embeddings)

clustering = AgglomerativeClustering(
    distance_threshold=1,
    n_clusters=None,
    metric='euclidean',
    linkage='average'
)

labels = clustering.fit_predict(embeddings)
clusters = defaultdict(list)
for key, cluster_id in zip(quotes, labels):
    clusters[cluster_id].append(key)

cluster_rows = []
for cluster_id in sorted(clusters.keys()):
    cluster_rows.append({
        'Cluster': cluster_id,
        'Keys': ', '.join(clusters[cluster_id])
    })

clusters_df = pd.DataFrame(cluster_rows)
print(clusters_df)

print('Hello world!')