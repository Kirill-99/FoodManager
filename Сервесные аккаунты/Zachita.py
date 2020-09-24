from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

import wmi
import datetime


def idTest():
    c = wmi.WMI()
    for item in c.Win32_PhysicalMedia():
        if "PHYSICALDRIVE" in str(item.Tag).upper():
            serialNo = item.SerialNumber
            return serialNo
            break

def idGoogleTest(idHDDNamber):
    # Файл, полученный в Google Developer Console
    CREDENTIALS_FILE = 'Foodtest-8f838db737a4.json'
    # ID Google Sheets документа (можно взять из его URL)
    spreadsheet_id = '1GoxF5tf_fflVmAxzgAg9spHifiwAoeGqpChX4TQZEpA'

    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
    
    # Пример чтения файла
    # Диапазон
    diap = 'G2:G100'
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=diap,
        majorDimension='ROWS'
    ).execute()
    idHDD = values['values']
    # return(tuple(idHDD))
    i = 0
    for element in idHDD:
        if str(idHDD[i]) == str("['"+idHDDNamber+"']"):
            print('Win')
            break
        elif str(idHDD[i]) != str("['"+idHDDNamber+"']"):
            i+=1
            continue
        else:
            print('stop')
            

primerid=idTest()
idGoogleTest(primerid)
input()
