import requests

"""
curl -X POST http://127.0.0.1:12024/mysql/delete -H 'Content-Type: application/json' -d '{"trace_id": "123", "rec_data": {"uid": "m1", "topk": 1}}'
"""
url = "http://127.0.0.1:2023/rec/hot"
data = {
    "trace_id": "123",
    "rec_data": {"uid": "m1", "topk": 1},
}
response = requests.post(url, json=data)
print(response.text)


url = "http://127.0.0.1:2023/rec/new"
data = {
    "trace_id": "123",
    "rec_data": {"uid": "m1", "topk": 1},
}
response = requests.post(url, json=data)
print(response.text)
