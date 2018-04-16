"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Setup the Sheets API
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# Call the Sheets API
SPREADSHEET_ID = '1vUQcjj-DtOc9GUWs63zY9IbQSQpKYEpF3dmNDIAb9Hs'
RANGE_NAME = 'Sheet1!A2:E'
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                             range=RANGE_NAME).execute()
values = result.get('values', [])
if not values:
    print('No data found.')
else:
    print('Name, Major:')
    for row in values:
        # Print columns A and E, which correspond to indices 0 and 4.
        print('%s, %s' % (row[0], row[4]))

body_obj = { "range" : "Sheet1!A2:E3", "values" : [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]], "majorDimension": "ROWS" }

print(body_obj['values'])

service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,
                                     range='Sheet1!A2:E3',
                                     body = body_obj,
                                     valueInputOption = 'RAW').execute()