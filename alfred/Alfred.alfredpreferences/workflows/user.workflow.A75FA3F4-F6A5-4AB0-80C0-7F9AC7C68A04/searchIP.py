# coding: utf-8
import os
from pydoc import getpager
import sys
import xlrd
reload(sys)
sys.setdefaultencoding("utf8")

def getNumber(str):
    try:
        f = float(str)
        return int(f)
    except ValueError:
        pass

def getPemFile(zoneName):
    suffix = ''
    if zoneName != 'us':
        suffix = '-{}'.format(zoneName)
    return '/Users/highfly029/Documents/work/ssh/superchameleon{}.pem'.format(suffix)

def main():
    excelPath = sys.argv[1]
    mixStr = sys.argv[2]
    array = mixStr.split("_")
    zoneName = array[0]
    serverType = array[1]
    id = array[2]

    #print("main excelPath={}, zoneName={}, serverType={}, id={}".format(excelPath, zoneName, serverType, id))
    
    selected = None
    workbook = xlrd.open_workbook(excelPath)
    for name in workbook.sheet_names():
        if name.find("({})".format(zoneName)) != -1:
            #print(name)
            sheet = workbook.sheet_by_name(name)
            for i in range(sheet.nrows):
                row = sheet.row_values(i)
                firstName = row[0]
                firstName = str(firstName)
                #print(firstName)
                if serverType == 'center':
                    if firstName.startswith("center"):
                        #print(row)
                        selected = row
                elif serverType == 'login':
                    if firstName.startswith("login") and firstName.endswith(id):
                        #print(row)
                        selected = row
                elif serverType == 'game':
                    num = getNumber(firstName)
                    if num == int(id):
                        #print(row)
                        selected = row

    if selected != None:
        pubIP = selected[4]
        # print('ssh -i {} ec2-user@{}'.format(getPemFile(zoneName), pubIP))
        print(pubIP)


if __name__ == '__main__':
    main()