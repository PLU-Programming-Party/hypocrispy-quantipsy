import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances
from openai import OpenAI

embeddings_df = pd.read_csv('thedata/embeddings.csv')

# quotes = embeddings_df['description'][:100].tolist()
embeddings = np.vstack(
    embeddings_df['embedding'][:100].apply(
        lambda s: np.fromstring(s.strip('[]'), sep=',')
    )
)

#embedding = get_embedding(quotes_df['quote'][102])

distances = euclidean_distances(embeddings)

print('Hello world!')