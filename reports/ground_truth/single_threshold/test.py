import csv

if __name__ == '__main__':
    a = ['BMS1','BMS2','BMS-POS','retail','kosarak','T10I4D100K']

    for dataset in a:
        if dataset == 'BMS1':
            n=59602
        if dataset == 'BMS2':
            n=77512
        if dataset == 'BMS-POS':
            n=515597
        if dataset == 'retail':
            n=88162
        if dataset == 'kosarak':
            n=990002
        if dataset == 'T10I4D100K':
            n=100000

        new ={}
        with open(dataset+'_new.csv', 'w') as f1:
            with open(dataset+'.csv', 'r') as f:
                result = csv.reader(f)
                
                for lines in result:
                    print(lines[1])
                    new[lines[0]] = float(lines[1])/n
                    print(new)
            for key in new.keys():
                f1.write("%s,%s\n"%(key,new[key]))
            