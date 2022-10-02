# from openpyxl import load_workbook
import pandas as pd
# if we are printing in console
# pd.options.display.max_rows = 9999
# read salesforce csv file
salesforce = pd.read_csv('report-salesforce.csv', encoding="windows-1251")
# read boldreports csv file
boldreports = pd.read_csv('report-boldreports.csv', encoding="windows-1251")

# get column 0 name
salesforce_columns = salesforce.columns.values[0]
# get column 0 name
boldreports_columns = boldreports.columns.values[0]
print("!!!.........Starting validating column count............!!!")
# check if both the column count match
if salesforce.columns.size != boldreports.columns.size:
    print("boldreports column count is not equal to salesforce column count")
print("!!!.........Finished validating column count............!!!")
print("!!!.........Starting validating column names............!!!")
# check the column names are same
for x in range(salesforce.columns.size - 1):
    if(salesforce.columns.values[x] != boldreports.columns.values[x]):
        print("column names mis match")
print("!!!.........Finished validating column names............!!!")
print("!!!.........Starting validating column values............!!!")
# diff for the csv files
diff = salesforce[[salesforce_columns]].compare(boldreports[[boldreports_columns]])
print(diff)
# write into excel
diff.to_excel("diff.xlsx")
print("!!!.........Finished validating column values............!!!")