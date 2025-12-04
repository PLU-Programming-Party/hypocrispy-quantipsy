import csv
import json
from program3 import client, get_embedding

def get_motion_picture_association_rating_please_for_our_description_of_a_meme_thank_you(text):
    response = client.responses.create(model='gpt-5.1', input=f'What motion picture association rating would you give to this meme: {text}. Just give me the rating and no other text.')
    return response.output_text

data = []
with open("thedata/known_memes.csv") as file:
    reader = csv.DictReader(file)
    for line in reader:
        text = f"{line['description']} -- {line['theAbout']}"
        # embedding = get_embedding(text)
        rating = get_motion_picture_association_rating_please_for_our_description_of_a_meme_thank_you(text)
        
        
# with open("frontend/embeddings.js", "w") as file:
#     file.write("const data =")
#     file.write(json.dumps(data))

