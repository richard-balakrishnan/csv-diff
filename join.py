import pandas as pd
salesforce = pd.read_csv('sample1.csv', encoding="ascii")
boldreports = pd.read_csv('sample1.csv', encoding="ascii")
# since we dont have id for unique, create an column with row number
salesforce.insert(0, 'id', range(0, 0 + len(salesforce)))
boldreports.insert(0, 'id', range(0, 0 + len(boldreports)))

print(salesforce)
print(boldreports)

# here we using inner join for getting common data from salesforce and boldreports csv
inner_join = pd.merge(salesforce, boldreports, on='id', how='inner')

print(inner_join)
# inner_join = inner_join.iloc[: , 1:]
# del inner_join[inner_join.columns.values[0]]
inner_join.to_csv('join.csv')
# diff = salesforce.compare(inner_join)
# print(salesforce)
# print(inner_join)