# install smartsheet sdk with pip install smartsheet-python-sdk
import smartsheet
# install pagerduty-api-python-client with pip install pypd
import pypd
import os
import logging
from datetime import datetime, timedelta

# Initialize client
smartsheet_token = os.environ['SMAR_API_KEY_PD_DEV']
smart = smartsheet.Smartsheet(access_token=smartsheet_token)
sheet_id = 3884170637272964

pypd.api_key = os.environ['PD_API_KEY']

# Make sure we don't miss any error
smart.errors_as_exceptions(True)

# Log all calls
logging.basicConfig(filename='pd-incidents-to-sheet.log', level=logging.INFO)

# fetch all incidents from PagerDuty
incidents = pypd.Incident.find(since=datetime.now() - timedelta(days=30))

smartsheet_column_map = {}

# Helper function to find cell in a row
def get_cell_by_column_name(row, column_name):
    column_id = smartsheet_column_map[column_name]
    return row.get_column(column_id)

# Helper function to find the incident ids of incidents already in the sheet
def get_existing_incidents(ids_column_id):
    sheet_incident_ids_only = smart.Sheets.get_sheet(sheet_id, column_ids=ids_column_id)
    incident_row_map = {}

    for r in sheet_incident_ids_only.rows:
        for cell in r.cells:
            incident_row_map[cell.value] = r.id
    return incident_row_map

# Helper function to get list of assignee names on call
def get_assignee_names(assignee_array):
    assignee_name_string = ""
    name_array = []

    for a in assignee_array:
        if a.get('assignee'):
            name_array.append(a.get('assignee').get('summary'))

    assignee_name_string = ",".join(name_array)
    return assignee_name_string

# Load entire sheet
sheet = smart.Sheets.get_sheet(sheet_id)
# Build column map for later reference - translates column names to column id
for column in sheet.columns:
    smartsheet_column_map[column.title] = column.id

# existing_incidents:  map of incident_id: row_id
existing_incidents = get_existing_incidents(smartsheet_column_map["ID"])

new_rows = []
update_rows = []

for i in incidents:
    row = smart.models.Row()
    
    id_cell = smart.models.Cell()
    id_cell.column_id = smartsheet_column_map["ID"]
    id_cell.value = i.get('id')
    row.cells.append(id_cell)
    
    number_cell = smart.models.Cell()
    number_cell.column_id = smartsheet_column_map["Number"]
    number_cell.value = i.get('incident_number')
    row.cells.append(number_cell)

    title_cell = smart.models.Cell()
    title_cell.column_id = smartsheet_column_map["Incident"]
    title_cell.value = i.get('title')
    row.cells.append(title_cell)

    desc_cell = smart.models.Cell()
    desc_cell.column_id = smartsheet_column_map["Description"]
    desc_cell.value = i.get('description')
    row.cells.append(desc_cell)

    created_cell = smart.models.Cell()
    created_cell.column_id = smartsheet_column_map["Created At"]
    created_cell.value = i.get('created_at')
    row.cells.append(created_cell)

    status_cell = smart.models.Cell()
    status_cell.column_id = smartsheet_column_map["Status"]
    status_cell.value = i.get('status')
    row.cells.append(status_cell)

    service_cell = smart.models.Cell()
    service_cell.column_id = smartsheet_column_map["Service"]
    service_cell.value = i.get('service').get('summary')
    row.cells.append(service_cell)

    if i.get('assignments'):
        service_cell = smart.models.Cell()
        service_cell.column_id = smartsheet_column_map["On Call"]
        service_cell.value = get_assignee_names(i.get('assignments'))
        row.cells.append(service_cell)


    if existing_incidents[i.get('id')]:
        row.id = existing_incidents[i.get('id')]
        update_rows.append(row)
    else:
        row.to_bottom = True
        new_rows.append(row)

if new_rows:
    add_result = smart.Sheets.add_rows(sheet_id, new_rows)
    print("Creating " + str(len(new_rows)) + " new rows to " + str(sheet.name))
else:
    print("No new incidents to add to sheet.")

if update_rows:
    result = smart.Sheets.update_rows(sheet_id, update_rows)
    print("Updating " + str(len(update_rows)) + " rows in " + str(sheet.name))
else:
    print("No new incidents to update in the sheet.")

print("Done")    
