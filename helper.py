import json
import os
import requests
from base64 import b64decode
from colorama import init
from termcolor import colored
# use Colorama to make Termcolor work on Windows
init()
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

def validate_column(expected_file, actual_file):
    print("!!!.........Starting validating column............!!!")
    # check the column size are equal
    if (expected_file.columns.size != actual_file.columns.size):
        print(colored("column are not equal", 'red'))    
    # check the column names are equal
    min_index = expected_file.columns.size - 1
    if(expected_file.columns.size > actual_file.columns.size):
        min_index = actual_file.columns.size - 1
    for index, item in enumerate(expected_file.columns.to_list()):
        if(index <= min_index):
            if(expected_file.columns.values[index] != actual_file.columns.values[index]):
                print(colored("column not available :" + expected_file.columns.values[index], 'red'))
    print("!!!.........Finished validating column............!!!")

def validate_row(expected_file, actual_file):
    print("!!!.........Starting validating row............!!!")
    # check the row length are equal
    if(len(expected_file) != len(actual_file)):
        print(colored("row length are not equal", 'red'))
    print("!!!.........Finished validating row............!!!")

def validate_data_types(expected_file, actual_file):
    print("!!!.........Starting validating datatypes of column............!!!")
    min_index = expected_file.columns.size - 1
    if(expected_file.columns.size > actual_file.columns.size):
        min_index = actual_file.columns.size - 1
    for index, item in enumerate(expected_file.columns.to_list()):
        if(index <= min_index):
            if(expected_file.dtypes[expected_file.columns.values[index]].name != actual_file.dtypes[actual_file.columns.values[index]].name):
                print(colored("Expected csv column: "+ expected_file.columns.values[index] + "datatype: " + expected_file.dtypes[expected_file.columns.values[index]].name, 'red'))
                print(colored("Actual csv column: "+ actual_file.columns.values[index] + "datatype: " + actual_file.dtypes[actual_file.columns.values[index]].name, 'red'))
    print("!!!.........Finished validating datatypes of column............!!!")

def write_diff(expected_file, actual_file, diff_file_path):
    print("!!!.........Starting comparing csv files............!!!")
    try:
        diff = expected_file.compare(actual_file)
        print(diff)
        diff.to_csv(diff_file_path)     
    except ValueError as e:
        print(colored("Failed to compare : " + str(e), 'red'))   
    print("!!!.........Finished comparing csv files............!!!")
