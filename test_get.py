import requests
import json

data = {'sender': 'Alice',
        'receiver': 'Bob',
        'message': 'how are you'}
data_json =json.dumps(data)
#payload = {'json_payload': data_json}
payload = json.dumps(data)
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
#r = requests.post("http://eggdroplabs.com/sensor/ex1/", data=payload,headers=headers)
r = requests.get("http://54.241.14.229:8001/")
print r
#    r = requests.get("http://eggdroplabs.com/sensor/",headers=headers)


