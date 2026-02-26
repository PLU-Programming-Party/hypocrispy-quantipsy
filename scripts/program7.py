
from sklearn.decomposition import PCA
import pandas as pd

embeddings_df = pd.read_csv('thedata/embeddings.csv')

pca = PCA(n_components=2)

embed = embeddings_df['embedding']

pca.fit_transform(embed)
