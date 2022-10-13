import json
import os
import pathlib
import re
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
            if (file.endswith('.' + ext)):
                collect.append(os.path.join(root, file))
    return collect


def postReq(report_id, body):
    api = config_JSON[0]['api'].replace("{{report_name}}", report_id)
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
    expected_file = expected_file.sort_index(axis=1)
    actual_file = actual_file.sort_index(axis=1)
    equal_col_size = True
    not_avl_col = []
    print("!!!.........Starting validating column............!!!")
    # check the column size are equal
    if (expected_file.columns.size != actual_file.columns.size):
        equal_col_size = False
        print(colored("column are not equal", 'red'))
    # check the column names are equal
    min_index = expected_file.columns.size - 1
    if (expected_file.columns.size > actual_file.columns.size):
        min_index = actual_file.columns.size - 1
    for index, item in enumerate(expected_file.columns.to_list()):
        if (index <= min_index):
            if (expected_file.columns.values[index] != actual_file.columns.values[index]):
                not_avl_col.append(expected_file.columns.values[index])
                print(colored("column not available :" +
                      expected_file.columns.values[index], 'red'))
    print("!!!.........Finished validating column............!!!")
    return ({"column_size": equal_col_size, "column_name": not_avl_col})


def validate_row(expected_file, actual_file):
    row_count = True
    print("!!!.........Starting validating row............!!!")
    # check the row length are equal
    if (len(expected_file) != len(actual_file)):
        row_count = False
        print(colored("row length are not equal", 'red'))
    print("!!!.........Finished validating row............!!!")
    return (row_count)


def validate_data_types(expected_file, actual_file):
    expected_file = expected_file.sort_index(axis=1)
    actual_file = actual_file.sort_index(axis=1)
    data_format = {
    }
    collection = []
    print("!!!.........Starting validating datatypes of column............!!!")
    min_index = expected_file.columns.size - 1
    if (expected_file.columns.size > actual_file.columns.size):
        min_index = actual_file.columns.size - 1
    for index, item in enumerate(expected_file.columns.to_list()):
        if (index <= min_index):
            if (expected_file.dtypes[expected_file.columns.values[index]].name != actual_file.dtypes[actual_file.columns.values[index]].name):
                data_format["expected"] = expected_file.columns.values[index]
                data_format["actual"] = actual_file.columns.values[index]
                data_format["expected_type"] = expected_file.dtypes[expected_file.columns.values[index]].name
                data_format["actual_type"] = actual_file.dtypes[actual_file.columns.values[index]].name
                collection.append(data_format)
                data_format={}
                print(colored("Expected csv column: " +
                      expected_file.columns.values[index] + "datatype : " + expected_file.dtypes[expected_file.columns.values[index]].name, 'red'))
                print(colored("Actual csv column: " +
                      actual_file.columns.values[index] + "datatype : " + actual_file.dtypes[actual_file.columns.values[index]].name, 'red'))
    print("!!!.........Finished validating datatypes of column............!!!")
    return (collection)


def write_diff(expected_file, actual_file, diff_file_path):
    error = ""
    diff_html = ""
    print("!!!.........Starting comparing csv files............!!!")
    try:
        expected_file = expected_file.sort_index(axis=1)
        actual_file = actual_file.sort_index(axis=1)
        diff = expected_file.compare(actual_file)
        print(diff)
        diff.to_csv(diff_file_path)
        diff_html = diff.to_html()
    except ValueError as e:
        error = str(e)
        print(colored("Failed to compare : " + str(e), 'red'))
    print("!!!.........Finished comparing csv files............!!!")
    return ({"error": error, "diff_html": diff_html})


def gen_html_report(info, path):
    template = """
        <button class="sf_accordion"> {{name}} </button>
        <div class="sf_panel">
        <h2>Description : {{description}} </h2>
        <h2>Export API : {{api_state}}</h2>
        <div id="sf_content">
        <h3>Column validation: </h3>
        <h4>Size of expected and actual column are : {{column_size}}</h4>
        <h4>The below columns are not available in compared file</h4>
        <ol>
        {{column_name}}
        </ol>
        <h4>The below datatypes mismatch</h4>
        <table>
        <tr>
          <th>Expected column name</th>
          <th>Actual column name</th>
          <th>Expected datatype</th>
          <th>Actual datatype</th>
        </tr>
        <tr>
          {{column_type}}
        </tr>
        </table>
        <h3>Row validation:</h3>
        <h4> Row length are : {{row_size}}</h4>
        <h3>Comparision diff:</h3>
        {{diff_html}}
        <h3>Error : <span class="red">{{error}}</span></h3>
        </div>
        <hr>
        </div>"""
    template_HTML = open("template\\index.html", "r")
    template_str = template_HTML.read()
    template_HTML.close()
    formed_template = ""
    col_not_avail_template = ""
    col_dtype_mismatch_template = ""
    # re.sub("{{description}}", info[0]['description'], data)
    for data in info:
        if (data["api_state"] == False):
            data["api_state"] = "<span class='red'>FAILED</span>"
        else:
            data["api_state"] = "<span class='green'>SUCCESS</span>"
        
        if(data["column_size"] == False):
            data["column_size"] = "<span class='red'>NOT EQUAL</span>"
        else:
            data["column_size"] = "<span class='green'>EQUAL</span>"

        if(data["row_size"] == False):
            data["row_size"] = "<span class='red'>NOT EQUAL</span>"
        else:
            data["row_size"] = "<span class='green'>EQUAL</span>"

        replace_data = re.sub("{{description}}", data["description"], template)
        replace_data = re.sub("{{name}}", data["name"] + " ( " + "CSV Export: " + data["api_state"] + ", Column name mismatch : " + str(len(data["column_name"])) + " ,Values mismatch : " + str(len(data["column_type"])) + " )", replace_data)
        replace_data = re.sub("{{api_state}}", data["api_state"] , replace_data)
        replace_data = re.sub("{{column_size}}", data["column_size"] , replace_data)
        replace_data = re.sub("{{row_size}}", data["row_size"], replace_data)
        replace_data = re.sub("{{diff_html}}", data["diff_html"], replace_data)
        replace_data = re.sub("{{error}}", data["error"], replace_data)

        for col_name in data["column_name"]:
            col_not_avail_template = col_not_avail_template + "<li>" + col_name + "</li>"
        replace_data = re.sub("{{column_name}}", col_not_avail_template, replace_data)
        col_not_avail_template = ""
    
        col_dtype_mismatch_template = ""
        for col_name in data["column_type"]:
            col_dtype_mismatch_template = "<tr>" + col_dtype_mismatch_template + "<td>" + col_name["expected"] + "</td>" + "<td>" + col_name["actual"] + "</td>" + "<td>" + col_name["expected_type"] + "</td>" + "<td>" + col_name["actual_type"] + "</td>" + "</tr>" 
        replace_data = re.sub("{{column_type}}", col_dtype_mismatch_template, replace_data)
        col_dtype_mismatch_template = ""

        formed_template = formed_template + replace_data
    
    formed_template = re.sub("{{template}}", formed_template ,template_str)
    print("Report generated path : "+"Report\\"+pathlib.PurePath(path).name+".html")
    if not(os.path.exists("Report")):
        os.makedirs("Report")
    html_file = open("Report\\"+pathlib.PurePath(path).name+".html", "w")
    html_file.write(formed_template)
    html_file.close()
    formed_template = ""