"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import time

SPREADSHEET_ID = '1vUQcjj-DtOc9GUWs63zY9IbQSQpKYEpF3dmNDIAb9Hs'

def init():
    # Setup the Sheets API
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    return service

def create_sheet(service, name):
    body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': name,
                        'sheetType': 'GRID'
                    }
                }
            }]
        }

    response = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID,
                                                  body = body)
    response.execute()

def read_sheet(service, sheet_name):
    RANGE_NAME = sheet_name
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


def write_to_sheet(service, sheet_name, double_array):
    body_obj = { "range" : sheet_name, "values" : double_array, "majorDimension": "ROWS" }

    response = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,
                                         range= sheet_name,
                                         body = body_obj,
                                         valueInputOption = 'RAW')
    response.execute()

def append_to_sheet(service, sheet_name, double_array):
    body_obj = { "range" : sheet_name, "values" : double_array, "majorDimension": "ROWS" }

    response = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID,
                                         range= sheet_name,
                                         body = body_obj,
                                         valueInputOption = 'RAW')
    response.execute()

'''Example:
service = init()
create_sheet(service, "test")
append_to_sheet(service, "test", [[0,1,2,3]])
'''

