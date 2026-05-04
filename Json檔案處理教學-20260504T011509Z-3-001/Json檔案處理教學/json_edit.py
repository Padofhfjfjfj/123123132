import  json
with open('data.json', 'r') as f:
    data = json.load(f)
data['age'] = 31
with open('data.json', 'w') as f:
    json.dump(data, f)