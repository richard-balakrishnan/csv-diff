import json
import os
import pandas as pd
from helper import *
# get the current working dir
cwd = os.getcwd()
# expected csv base dir
# expected_csv_dir = cwd + '\\compare\\expected'
# actual_csv_dir = cwd + '\\compare\\actual'
# get array of csv files
# expected_csv_list = getExtList(expected_csv_dir, "csv")
# actual_csv_list = getExtList(actual_csv_dir, 'csv')
# read the data.json
data_JSON = json.load(open('data.json'))
if(len(data_JSON) > 0):
    #check if \\compare\\diff folder exsist then del
    # if(os.path.exists(cwd + "\\compare\\diff")):
    #     os.rmdir(cwd + "\\compare\\diff")
    for data in data_JSON:
        expected_file_path = cwd + data['path']
        actual_file_path = cwd + data['path'].replace('\\expected\\','\\actual\\')
        diff_file_path = cwd + data['path'].replace('\\expected\\','\\diff\\')
        print("## Expected path: " + expected_file_path)
        print("## Actual path: " + actual_file_path)
        print("## Diff path: " + diff_file_path)
        # call api and save the file
        info = postReq(data['report_id'], data['param_value'])
        if(info.status_code == 200):
            info_content = info.json()['FileContent']
            write_base64_to_csv(info_content, actual_file_path)
            # check the csv file is exsist in expected and actual path
            if(os.path.exists(expected_file_path) and os.path.exists(cwd + data['path'].replace('\\expected\\','\\actual\\'))):
                # if the diff file path not exsist create one
                if not(os.path.exists(os.path.dirname(diff_file_path))):
                    os.makedirs(os.path.dirname(diff_file_path))
                # read the csv file
                expected_file = pd.read_csv( expected_file_path, encoding="utf-8")
                actual_file = pd.read_csv( actual_file_path, encoding="utf-8")
                print("!!!.........Starting validating column............!!!")
                # check the column size are equal
                if (expected_file.columns.size != actual_file.columns.size):
                    print("column are not equal")    
                # check the column names are equal        
                for x in range(expected_file.columns.size - 1):
                    if(expected_file.columns.values[x] != actual_file.columns.values[x]):
                        print("column not available :" + expected_file.columns.values[x])
                print("!!!.........Finished validating column............!!!")
                print("!!!.........Starting validating row............!!!")
                # check the row length are equal
                if(len(expected_file) != len(actual_file)):
                    print("row length are not equal")
                print("!!!.........Finished validating row............!!!")
                # check the column data type
                print("!!!.........Starting validating datatypes of column............!!!")
                # print(expected_file.dtypes)
                # print(actual_file.dtypes)
                for x in range(expected_file.columns.size - 1):
                    if(expected_file.dtypes[expected_file.columns.values[x]] != actual_file.dtypes[actual_file.columns.values[x]]):
                        print("Expected csv column: "+ expected_file.columns.values[x] + "datatype: " + expected_file.dtypes[expected_file.columns.values[x]].name)
                        print("Actual csv column: "+ actual_file.columns.values[x] + "datatype: " + actual_file.dtypes[actual_file.columns.values[x]].name)
                print("!!!.........Finished validating datatypes of column............!!!")
                print("!!!.........Starting comparing csv files............!!!")
                diff = expected_file.compare(actual_file)
                print(diff)
                diff.to_csv(diff_file_path)        
                print("!!!.........Finished comparing csv files............!!!")
        else:
                print("!!!.........Failed receiving data............!!!")
                print("Description : " + data['description'])
                print("Status Code : " + info.status_code)
                print("!!!.........Failed receiving data............!!!")