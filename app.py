import csv

from flask import Flask, jsonify, render_template, request, send_file

from scripts.program3 import get_closest_meme, calculate_distance

data = []

with open("thedata/embeddings.csv", encoding="UTF-8") as file:
    reader = csv.DictReader(file)
    for line in reader:
        data.append(line)

exclude_indexes = set()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/meme/<int:meme_index>")
def get_meme(meme_index: int):
    return jsonify(data[meme_index] | {"id": meme_index})


@app.route("/distance")
def get_distance():
    index1 = request.args.get("id1", type=int)
    index2 = request.args.get("id2", type=int)

    # Dummy implementation, replace with actual distance calculation
    distance = abs(index1 - index2)

    return jsonify({"distance": distance})


@app.route("/gamez")
def gamez():
    meme_index = request.args.get("index", type=int)
    target_id = request.args.get("target", type=int)
    length = request.args.get("length", type=int, default=3)

    exclude_indexes.add(meme_index)
    result = [
        data[i]
        | {
            "id": i,
            "distance_to_target": calculate_distance(i, target_id),
            "distance_from_position": distance_from_position,
        }
        for i, distance_from_position in get_closest_meme(
            meme_index, length=length, exclude_indexes=exclude_indexes
        )
    ]
    return jsonify(result)
