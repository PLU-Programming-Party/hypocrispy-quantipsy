import pandas as pd
import numpy as np
from openai import OpenAI

df = pd.read_csv('thedata/known_memes.csv')

client = OpenAI(api_key="67")

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    print(text)
    return client.embeddings.create(input = [text], model=model).data[0].embedding

df['embedding'] = df['description'][:100].apply(lambda x: get_embedding(x, model='text-embedding-3-small'))
df.to_csv('thedata/embeddings.csv', index=False)

print('Hello world!')