import requests

"""
curl -X POST http://127.0.0.1:2023/search/hot -H 'Content-Type: application/json' -d '{"trace_id": "123", "rec_data": {"keyword": "熊猫", "topk": 1}}'
"""
url = "http://127.0.0.1:2023/search/hot"
data = {
    "trace_id": "123",
    "search_data": {"keyword": "熊猫", "topk": 1},
}
response = requests.post(url, json=data)
print(response.text)
