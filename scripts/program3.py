import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances
from openai import OpenAI

quotes_df = pd.read_csv("thedata/known_memes.csv")

client = OpenAI(api_key="67")



def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


embeddings_df = pd.read_csv("thedata/embeddings.csv")

embeddings = np.vstack(
    embeddings_df["embedding"][:1000].apply(
        lambda s: np.fromstring(s.strip("[]"), sep=",")
    )
)



def calculate_distance(index1, index2):
    print(index1, index2)
    em1 = get_embedding(quotes_df["description"][index1])
    em2 = get_embedding(quotes_df["description"][index2])

    return np.linalg.norm(np.array(em1) - np.array(em2))


def get_closest_meme(index, length=5, exclude_indexes={}):
    embedding = get_embedding(quotes_df["description"][index])

    distances = euclidean_distances(embeddings, np.expand_dims(embedding, 0))
    dist = [d[0] for d in distances]

    return [
        (dist.index(v), v) for v in sorted(dist) if dist.index(v) not in exclude_indexes
    ][1 : length + 1]

# BFS takes in starting index and goal index, and returns the path from start to goal as a list of indices. If no path exists, it returns None.
def bfs(start_index, goal_index):
    visited = set()
    queue = [(start_index, [start_index])]

    while queue:
        current_index, path = queue.pop(0)

        if current_index == goal_index:
            return path

        if current_index not in visited:
            visited.add(current_index)
            neighbors = get_closest_meme(current_index, length=5, exclude_indexes=set(path))

            for neighbor_index, _ in neighbors:
                if neighbor_index not in visited:
                    queue.append((neighbor_index, path + [neighbor_index]))

    return None  # Return None if no path is found

def game():
    start_index = 69
    goal_index = 420

    path = bfs(start_index, goal_index)

    if path is not None:
        print("Path found:")
        for index in path:
            print(quotes_df["description"][index])
    else:
        print("No path found.")

game()

# curr_index = 67
# traversed_indicies = {curr_index}

# for i in range(10):
#     print(quotes_df['description'][curr_index])
#     close = get_closest_meme(curr_index)

#     for index in close:
#         if index not in traversed_indicies:
#             traversed_indicies.add(index)
#             curr_index = index
#             break


# print('Hello world!')
