import numpy as np
import pandas as pd
import networkx as nx

embeddings_df = pd.read_csv("thedata/embeddings.csv")

embeddings = np.vstack(
    embeddings_df["embedding"][:1000].apply(
        lambda s: np.fromstring(s.strip("[]"), sep=",")
    )
)

# Get random list of indices for the random sample
random_indices = np.random.choice(len(embeddings), 50)
magic_hat = {} # personality variable (we dont need this at all)
for index in random_indices:
    magic_hat[index] = embeddings[index]

# Initialize the graph
fart = nx.Graph()
completed_nodes = set()

def poissidon_distance(compare_index):
    compare_embedding = embeddings[compare_index]
    for index in random_indices:
        embedding = embeddings[index]
        distance = np.linalg.norm(embedding - compare_embedding, ord=2)
        # WE STOPPED HERE    



def get_closest_meme(index, length=5, exclude_indexes={}):
    embedding = embeddings[index]

    distances = # AND THIS IS SUPPOSED TO CALL POISSIDON_DISTANCE
    # EVERYTHING BELOW THIS NEEDS TO BE FIXED
    dist = [d[0] for d in distances]

    return [(dist.index(v), v) for v in sorted(dist) if dist.index(v) not in exclude_indexes][1 : length + 1]


# WE ARE TRYING TO MAKE A GRAPH
for index in random_indices:
    closest = get_closest_meme(index, 5, completed_nodes)




print("hello")