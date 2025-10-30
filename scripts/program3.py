import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances
from openai import OpenAI

quotes_df = pd.read_csv('thedata/known_memes.csv')

client = OpenAI(api_key="67")

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

embeddings_df = pd.read_csv('thedata/embeddings.csv')

embeddings = np.vstack(
    embeddings_df['embedding'][:100].apply(
        lambda s: np.fromstring(s.strip('[]'), sep=',')
    )
)

def get_closest_meme(index):

    embedding = get_embedding(quotes_df['description'][index])

    distances = euclidean_distances(embeddings, np.expand_dims(embedding, 0))
    dist = [d[0] for d in distances]
    
    return [dist.index(v) for v in sorted(dist)]

curr_index = 700
traversed_indicies = {curr_index}

for i in range(10):
    print(quotes_df['description'][curr_index])
    close = get_closest_meme(curr_index)

    for index in close:
        if index not in traversed_indicies:
            traversed_indicies.add(index)
            curr_index = index
            break


print('Hello world!')