import requests
base_url="http://127.0.0.1:8000/bank/users/"
response=requests.get(base_url)
print(response.json()[0])

a={"milan":"dada","age":0}
