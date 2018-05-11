import json

def navigate_json_path(json, path):
    for e in path:
        json = json[e]
    return json


def extract_data(json_data, json_path=['GSP', 'RES', 'R']):
    try:
        data = navigate_json_path(json_data, json_path)
        results = []
        for row in data:
            results.append(row['MT'])
        return results
    except Exception:
        return []