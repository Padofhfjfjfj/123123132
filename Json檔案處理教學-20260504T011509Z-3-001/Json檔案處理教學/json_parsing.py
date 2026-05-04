import json
json_string = '{"name": "張三", "age": 30}'
data = json.loads(json_string)
print(data)