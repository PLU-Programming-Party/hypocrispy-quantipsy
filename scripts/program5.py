import csv
import json

from flask import Flask, request, jsonify, send_file
from program3 import get_closest_meme

data = []

with open("thedata/embeddings.csv", encoding="UTF-8") as file:
    reader = csv.DictReader(file)
    for line in reader:
        data.append(line)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return send_file("../frontend/index.html")

@app.route("/gamez")
def gamez():
    meme_index = request.args.get('index', type=int)
    length = request.args.get('length', type=int)
    result = [data[i] | {"id": i} for i in get_closest_meme(meme_index, length)]
    return jsonify(result)