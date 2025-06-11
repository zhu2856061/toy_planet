import requests

"""
curl -X POST http://127.0.0.1:12024/mysql/delete -H 'Content-Type: application/json' -d '{"trace_id": "123", "kit_table": {"set_code": "T00002"}}'
"""
url = "http://127.0.0.1:2023/mysql/delete"
data = {"trace_id": "123", "kit_table": {"set_code": "T00002"}}
response = requests.post(url, json=data)
print(response.text)
