import os
import requests
from base64 import b64decode
from helper import *


# url = "https://sateam.boldreports.com/reporting/api/site/main/v1.0/reports/export"
# req_headers = {
#     "Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJpY2hhcmQuYmFsYWtyaXNobmFuQHN5bmNmdXNpb24uY29tIiwibmFtZWlkIjoiNDgiLCJ1bmlxdWVfbmFtZSI6IjhkZjExZjI4LTBiMzItNGViMi1iMmI5LTFkZDcxZGJjMjE4OSIsIklQIjoiMTU5Ljg5LjIzNy42NyIsImlzc3VlZF9kYXRlIjoiMTY2NDk4MTg5MiIsIm5iZiI6MTY2NDk4MTg5MiwiZXhwIjoxNjY4ODY5ODkyLCJpYXQiOjE2NjQ5ODE4OTIsImlzcyI6Imh0dHBzOi8vc2F0ZWFtLmJvbGRyZXBvcnRzLmNvbS9yZXBvcnRpbmcvc2l0ZS9tYWluIiwiYXVkIjoiaHR0cHM6Ly9zYXRlYW0uYm9sZHJlcG9ydHMuY29tL3JlcG9ydGluZy9zaXRlL21haW4ifQ.ddHIQ24dp89Ds5rrMBIJPsOgQn6nLJl7bGu7UGq1bPs",
#     "Content-Type": "application/json"
# }

# data = {
#     "ReportId" : "68b69c3f-13f2-4345-9b23-7c2c9bd2c652",
#     "ExportType" : "CSV"
# }

# req = requests.post(url, headers=req_headers, json=data)
# byte_code = req.json()['FileContent']
# # print(req.status_code)
# # print(byte_code)

# url1 = "https://sateam.boldreports.com/reporting/api/site/main/v1.0/reports/c84b204b-d072-4114-931a-c9776ff08752/CSV/export-filter"
# data1 = {"FilterParameters": "{'Sales Order No': ['S050750']}"}

# req1 = requests.post(url1, headers=req_headers, json=data1)
# byte_code1 = req1.json()['FileContent']

# bytes = b64decode(byte_code1, validate=True)
# f = open('file.csv', 'wb')
# f.write(bytes)
# f.close()

postReq()