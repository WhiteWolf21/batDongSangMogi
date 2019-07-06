import sys
import pandas as pd
import os.path as path
import re
import special_characters as sp
from pandas import DataFrame

def check(value, i):
    value_i = value.lower()
    for x in intentFile.columns:
        for y in range(len(intentFile)):
            intent_file = intentFile[x][:][y]
            if type(intent_file) is str:
                
                if intent_file in value_i:
                    return x
                # Specialized for Banks
                elif x == 'Ngân hàng bảo lãnh' and ',' in intent_file:
                    tmp = intent_file.split(',')
                    intent = tmp[0] + '.*' + tmp[1]
                    intent2 = tmp[1] + '.*' + tmp[0]
                    if re.search(intent, value_i, re.M|re.I) or re.search(intent2, value_i, re.M|re.I):
                        return x
                """
                elif 'ngân hàng' in value_i or 'n.hàng' in value_i:
                    for z in ['hỗ trợ','bảo lãnh','cho vay','vay','tài trợ']:
                        if z in value_i:
                            return 'ngân hàng bảo lãnh'
                            
                a = re.search('(ng'+sp.aw+'n' 'h'+sp.a+'ng|n.h'+sp.a+'ng).*(h'+sp.oo+'tr'+sp.ow+'|b'+sp.a+'o l'+sp.a+'nh|cho vay|vay|t'+sp.a+'i tr'+sp.ow+')', value_i, re.M|re.I)
                b = re.search('(h'+sp.oo+'tr'+sp.ow+'|b'+sp.a+'o l'+sp.a+'nh|cho vay|vay|t'+sp.a+'i tr'+sp.ow+').*(ng'+sp.aw+'n' 'h'+sp.a+'ng|n.h'+sp.a+'ng)', value_i, re.M|re.I)               
                elif a or b:
                    return 'ngân hàng bảo lãnh'
                """

if __name__ == '__main__':

    resultFile = pd.read_csv(path.relpath('result.csv'), encoding='utf-8')
    intentFile = pd.read_csv(path.relpath('intent.csv'), encoding='utf-8')
    frames = [DataFrame(
        {},
        columns = ['Index','Link','Content','User','Type','Intent','PIC']
    )]
    pd.concat(frames).to_csv(path.relpath('categorized.csv'), encoding='utf-8', index=False)
    file_ = pd.read_csv(path.relpath('categorized.csv'), encoding='utf-8')

    for row in range(len(resultFile)):
        value = resultFile.values[row][2]
        if type(value) is str and value != '.':

            # Get intent
            intent = check(value, row)

            # Append DataFrames to a list
            frames.append(
                pd.DataFrame (
                    {
                    'Index':[row],
                    'Link':[resultFile.values[row][1]],
                    'Content':[value],
                    'User':[resultFile.values[row][3]],
                    'Type':[resultFile.values[row][4]],
                    'Intent':[intent],
                    'PIC':[resultFile.values[row][6]]
                    },
                    columns=['Index','Link','Content','User','Type','Intent','PIC']
                )
            )
    # Write to .csv
    pd.concat(frames).to_csv(path.relpath('categorized.csv'), encoding='utf-8', index=False)