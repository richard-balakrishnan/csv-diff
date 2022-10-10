"""
Usage : 
eg: python compare.py --report reports-data/{{dynamic}}.json //particular file
eg: python compare.py //all file
"""
import argparse
import json
import os
import sys
from turtle import color
import pandas as pd
from helper import *
# get the current working dir
cwd = os.getcwd()
from colorama import init
from termcolor import colored
# use Colorama to make Termcolor work on Windows too
init()
parser = argparse.ArgumentParser(description="Provide JSON file as input to compare CSV")
parser.add_argument("-r","--report", type=str, default="*", metavar="" ,help="Provide --report=reports-data/{{dynamic}}.json")
args = parser.parse_args()
reports_JSON = []
print(colored("Started using : " + args.report, 'green'))
if (args.report != "*"):
    reports_JSON.append(args.report)
if(args.report == "*"):
    reports_JSON = getExtList(cwd + "\\reports-data", "json")
for report in reports_JSON:
    if (os.path.exists(report)):
        data_JSON = json.load(open(report))
        root_path = data_JSON['root_path']
        data_JSON = data_JSON['reports']
        if(len(data_JSON) > 0):
            for data in data_JSON:
                data['path'] = root_path + data['path']
                expected_file_path = cwd + data['path']
                actual_file_path = cwd + data['path'].replace('\\expected\\','\\actual\\')
                diff_file_path = cwd + data['path'].replace('\\expected\\','\\diff\\')
                print(colored("## Expected path: " + expected_file_path, 'yellow'))
                print(colored("## Actual path: " + actual_file_path, 'yellow'))
                print(colored("## Diff path: " + diff_file_path, 'yellow'))
                # call api and save the file
                info = postReq(data['report_id'], data['params'])
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
                        validate_column(expected_file, actual_file)
                        validate_row(expected_file, actual_file)
                        validate_data_types(expected_file, actual_file)
                        print("!!!.........Starting comparing csv files............!!!")
                        try:
                            diff = expected_file.compare(actual_file)
                            print(diff)
                            diff.to_csv(diff_file_path)     
                        except ValueError as e:
                            print(colored("Failed to compare : " + str(e), 'red'))   
                        print("!!!.........Finished comparing csv files............!!!")
                else:
                        print("!!!.........Failed receiving data............!!!")
                        print(colored("Description : " + data['description'], 'red'))
                        print(colored("Status Code : " + info.status_code, 'red'))
                        print("!!!.........Failed receiving data............!!!")
    else:
        print(colored("The provided input : " + report + " does not exsist", 'red'))