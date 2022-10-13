"""
Usage : 
eg: python compare.py --report reports-data/{{dynamic}}.json //particular file
eg: python compare.py //all file
"""
import argparse
import json
import os
import pandas as pd
from helper import *
cwd = os.getcwd()
from colorama import init
from termcolor import colored
init()

error_model = {
}
error_obj = []

# command prompt args start
parser = argparse.ArgumentParser(description="Provide JSON file as input to compare CSV")
parser.add_argument("-r","--report", type=str, default="*", metavar="" ,help="Provide --report=reports-data/{{dynamic}}.json")
args = parser.parse_args()
#command prompt args
reports_JSON = []
print(colored("Started using : " + args.report, 'green'))
if (args.report != "*"):
    reports_JSON.append(args.report)
if(args.report == "*"):
    reports_JSON = getExtList(cwd + "\\reports-data", "json")
for report in reports_JSON:
    if (os.path.exists(report)):
        data_JSON = json.load(open(report))
        root_path = "\\compare\\expected\\" + data_JSON['root_path'] + "\\"
        report_id = data_JSON['report_id'] 
        data_JSON = data_JSON['reports']
        if(len(data_JSON) > 0):
            for data in data_JSON:
                error_model['name'] = data['name']
                error_model['description'] = data['description']
                data['name'] = root_path + data['name']
                expected_file_path = cwd + data['name']
                actual_file_path = cwd + data['name'].replace('\\expected\\','\\actual\\')
                diff_file_path = cwd + data['name'].replace('\\expected\\','\\diff\\')
                print(colored("Description : " + data['description'], 'magenta'))
                print(colored("## Expected path: " + expected_file_path, 'yellow'))
                print(colored("## Actual path: " + actual_file_path, 'yellow'))
                print(colored("## Diff path: " + diff_file_path, 'yellow'))
                # call api and save the file
                info = postReq(report_id, {"FilterParameters": repr(data['params'])})
                if(info.status_code == 200):
                    error_model['api_state'] = True
                    info_content = info.json()['FileContent']
                    write_base64_to_csv(info_content, actual_file_path)
                    # check the csv file is exsist in expected and actual path
                    if(os.path.exists(expected_file_path) and os.path.exists(cwd + data['name'].replace('\\expected\\','\\actual\\'))):
                        # if the diff file path not exsist create one
                        if not(os.path.exists(os.path.dirname(diff_file_path))):
                            os.makedirs(os.path.dirname(diff_file_path))
                        # read the csv file
                        expected_file = pd.read_csv( expected_file_path, encoding="utf-8", dtype=str)
                        actual_file = pd.read_csv( actual_file_path, encoding="utf-8", dtype=str)
                        col_valid = validate_column(expected_file, actual_file)
                        row_valid = validate_row(expected_file, actual_file)
                        col_dtype = validate_data_types(expected_file, actual_file)
                        compare_file = write_diff(expected_file, actual_file, diff_file_path)
                        error_model['column_size'] = col_valid['column_size']
                        error_model['column_name'] = col_valid['column_name']
                        error_model['row_size'] = row_valid
                        error_model['error'] = compare_file['error']
                        error_model['diff_html'] = compare_file['diff_html']
                        error_model['diff_len'] = compare_file['diff_len']
                        error_model['column_type'] = col_dtype
                        error_obj.append(error_model)
                        error_model = {}
                else:
                        print("!!!.........Failed receiving data............!!!")
                        print(colored("Description : " + data['description'], 'red'))
                        print(colored("Status Code : " + str(info.status_code), 'red'))
                        print("!!!.........Failed receiving data............!!!")
            # write into html for every json completion
            gen_html_report(error_obj, root_path)
            error_obj = []
    else:
        print(colored("The provided input : " + report + " does not exsist", 'red'))