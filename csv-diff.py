from csv_diff import load_csv, compare
diff = compare(
    load_csv(open("report-boldreports.csv")),
    load_csv(open("report-salesforce.csv"))
)
print(diff)