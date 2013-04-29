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
r = requests.post("http://54.241.14.229/sensor/tweets/", data=payload,headers=headers)
print r.text
#    r = requests.get("http://eggdroplabs.com/sensor/",headers=headers)


