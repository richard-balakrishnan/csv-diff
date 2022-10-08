import json
import os
import requests
from base64 import b64decode
config_JSON = json.load(open('config.json'))

# path - path or directory
# ext - extension of file to be found
# eg: getExtList('D:\folder','csv')
def getExtList(path, ext):
    collect = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if(file.endswith('.' + ext)):
                collect.append(os.path.join(root,file))
    return collect

def postReq(report_id, body):
    api = config_JSON[0]['api'].replace("{{report_name}}",report_id)
    bearer_token = config_JSON[0]['bearer_token']
    req_headers = {
     "Authorization": bearer_token,
     "Content-Type": "application/json"
    }
    return (requests.post(api, headers=req_headers, json=body))

def write_base64_to_csv(base64, write_path):
    base64_decode = b64decode(base64, validate=True)
    os.makedirs(os.path.dirname(write_path), exist_ok=True)
    file = open(write_path, 'wb')
    file.write(base64_decode)
    file.close()