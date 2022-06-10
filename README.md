# PagerDuty Incidents to Smartsheet
This is a Python script that sends [PagerDuty](https://www.pagerduty.com) incidents to a sheet in [Smartsheet](https://www.smartsheet.com/). The script adds new incidents to the bottom of the sheet, and updates any existing incident already in the sheet. 

This is very basic. The update only checks if the incident id is already in the sheet, and then updates the entire row no matter if there are any changes in the incident.

## Dependencies
This script relies on the [PDPYRAS: PagerDuty Python REST API Sessions](https://github.com/PagerDuty/pdpyras) as well as the [Smartsheet Python SDK](https://github.com/smartsheet-platform/smartsheet-python-sdk). Before using the script please install both of those libraries using [PIP](https://pip.pypa.io/en/stable/installing/).

```
pip install pdpyras
pip install smartsheet-python-sdk
```

## Instructions
1. Create a sheet, and get the Sheet ID from File->Sheet Properties in the Smartsheet UI.
1. As the code stands right now, it relies on the names of the columns in the sheet to put the PagerDuty information in the correct cells. Currently, the names of the  columns are as follows:
- ID
- Number
- Incident
- Description
- Created At
- Status
- Service
- On Call

If you change the names of the columns in the sheet, then make changes to the code around lines 66-108. 

1. Set your value for `smartsheet_token` on line 10.
1. Set your value for `sheet_id` on line 12.
1. Set your value for `pypd.api_key` on line 14.
