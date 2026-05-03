import os
import json

def save_candidate(candidate_data):
    os.makedirs("data", exist_ok=True)

    file_path = "data/candidates.json"

    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(candidate_data)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)