# Prerequisite

    Install python using the link - [Download](https://www.python.org/downloads/windows/)

    using python run the below commands - 
    * pip install pandas
    * pip install requests
    * pip install colorama

# Run   

    python compare.py --report reports-data/{{dynamic}}.json 

```batch
    python compare.py --report reports-data/crr_opps_closed_won_this_month.json
```

# Config.json

```
[{
    "api" : "https://sateam.boldreports.com/reporting/api/site/main/v1.0/reports/{{report_name}}/CSV/export-filter",
    "bearer_token" : "bearer <<token-here>>"
}]
```

* `api` - The API url to export the csv from the Bold Reports salesforce tenant.
* `bearer_token` - Token to authenticate the user to export the csv files.

# Reports Data JSON

* Create single JSON file for each reports of salesforce and keep it in `reports-data` folder.
    ```
    reports-data/crr_opps_closed_won_this_month.json
    ```
* The JSON format should be like the below.

```json
{
    "root_path": "crr_opps_closed_won_this_month", --> (1)
    "reports": [ --> (2)
        {
            "name": "2021_Jan_close_date.csv", --> (2.1)
            "report_id": "c84b204b-d072-4114-931a-c9776ff08752", --> (2.2)
            "params": { --> (2.3)
                "SalesOrderNumber" : ["SO50754"] --> (2.3.1)
            },
            "description": "report of data between 2021 jan" --> (3)
        }        
    ]
}

```

> Ensure the salesforce exported file should the `UTF-8` encoding format.

* (1) - Root path of the JSON file with the `reports-data` folder. If we introduce the new folder inside the `reports-data` we need to mention the folder name in the `root_path` entry.

```json
"root_path": "new-folder//crr_opps_closed_won_this_month"
```

* (2) - Here we are maintaining the reports attributes as array of objects.
    * (2.1) - `name` - Specify the name of the csv file.
    * (2.2) - `report_id` - Specific the ID of the report which is obtained from the report URL.
    * (2.3) - `params` - Specify the parameter values. The `key` should match with the report's parameter name.
        * (2.3.1) - Name of the parameter with the value.
* (3) - `Optional` report description, used only in console.
