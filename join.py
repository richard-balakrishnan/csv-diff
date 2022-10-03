import pandas as pd
salesforce = pd.read_csv('report-boldreports.csv', encoding="windows-1251")
boldreports = pd.read_csv('report-salesforce.csv', encoding="windows-1251")
# here we using inner join for getting common data from salesforce and boldreports csv
inner_join = pd.merge(salesforce, boldreports, how='inner')
# del inner_join[inner_join.columns.values[0]]
inner_join.to_csv('inner_join.csv')
diff = salesforce.compare(boldreports)
print(diff)