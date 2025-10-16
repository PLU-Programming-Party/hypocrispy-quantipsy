import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances
from openai import OpenAI

quotes_df = pd.read_csv('thedata/quotes-wisdom.csv')

client = OpenAI(api_key="5")

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding


embeddings_df = pd.read_csv('thedata/embeddings.csv')

quotes = embeddings_df['quote'][:100].tolist()
embeddings = np.vstack(
    embeddings_df['quote_embedding'][:100].apply(
        lambda s: np.fromstring(s.strip('[]'), sep=',')
    )
)

embedding = get_embedding(quotes_df['quote'][102])

distances = euclidean_distances(embeddings, np.expand_dims(embedding, 0))

print('Hello world!')