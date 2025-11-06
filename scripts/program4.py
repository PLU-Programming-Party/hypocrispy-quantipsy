import csv
import json

data = []
with open("thedata/embeddings.csv") as file:
    reader = csv.DictReader(file)
    for line in reader:
        data.append(line)

with open("frontend/embeddings.js", "w") as file:
    file.write("const data =")
    file.write(json.dumps(data))