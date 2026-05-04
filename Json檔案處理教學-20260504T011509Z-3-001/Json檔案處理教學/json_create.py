import json
data = {"name": "張三", "age": 30}
with open('data.json', 'w') as f:
    json.dump(data, f)