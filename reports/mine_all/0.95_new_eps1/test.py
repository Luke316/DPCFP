import csv 
import re

datasets = ['BMS1']#, 'BMS2','retail','kosarak','BMS-POS','T10I4D100K']
x = [0.1,0.55,1.0,1.45,1.9,2.35]

for dataset in datasets:
    for eps in x:
        for i in range(0,10):
            for  index, row in enumerate(open(dataset+'_privacy_vs_utility_'+ str(i) +'.csv')):
                *others, last =row.split(',')
                print(last)
                a = re.findall(r'\[(.*?)\]', row)
                print(type(a))