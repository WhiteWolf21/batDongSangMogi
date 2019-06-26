# import csv

# with open('result.csv', 'r', encoding='UTF-8', newline='') as csvarchive:
#     entrada = csv.reader(csvarchive)
#     for reg in entrada:
#         print(reg)

import pandas as pd

# resultFile = pd.read_csv('result.csv', encoding='utf-8')
resultFile = pd.read_csv('result.xlsx - Comment.csv', encoding='utf-8')
intentFile = pd.read_csv('intent.csv', encoding='utf-8')

def check(value):
    for x in intentFile.columns:
        for y in range(len(intentFile)):
            if type(value) is str and type(intentFile[x][:][y]) is str:
                if 'ngân hàng' in value.lower() or 'n.hàng' in value.lower():
                    for z in ['hỗ trợ','bảo lãnh','cho vay','vay','tài trợ']:
                        if z in value.lower():
                            print(value)
                            return 'ngân hàng bảo lãnh'
                elif (intentFile[x][:][y] in value.lower() and value != '.'):
                    print(value)
                    return x

count = 0
for row in range(len(resultFile)):
    if type(resultFile.values[row][2]) is str:
        intent = check(resultFile.values[row][1])
        # TODO write intent to file
        print(count, ' : ', intent)
    count += 1
    
# resultFile.to_csv('result_modified.csv')