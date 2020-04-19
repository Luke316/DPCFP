from collections import OrderedDict
from random import sample
import numpy as np
from dataset_processing import DifferentItemsCount, TruncateDatabase, ReadDataset
from time import time
from pprint import pprint
import csv

#from dataset_processing import init_T

def MISTable(T, items,n,epsilon,truncated_length,threshold=0.01, beta=0.25): #beta in DPARM = 0.25
    #time_start=time()
    #init support with 0
    support = dict.fromkeys(items, 0) 

    #scan dataset to get origin support
    #can use collections.Counter() to speed up 
    for transaction in T:
        for item in transaction:
            if item in items:
                support[item]=support.get(item) + 1    #origin support
    # test original support
    # with open('original_support.csv', 'w') as f:
    #     for key in support.keys():
    #         f.write("%s,%s\n"%(key,support[key]))

    sensitivity = truncated_length/n
    MIS_table = dict.fromkeys(items, 0)
    for item in support.keys():
        if epsilon!=0:
            support[item] = support.get(item)/n + np.random.laplace(0, sensitivity / epsilon) # noisy support
        else:
            support[item] = support.get(item)/n #0328
        MIS_table[item] = max(beta*support[item],threshold) #if beta =0, the MIS is basically threshold and equals to FIM
    
    sorted_MIS_table={k: v for k, v in sorted(MIS_table.items(), key=lambda item: item[1],reverse = True)}#descending order
    
    # prune Strategy 1, find LMS
    for item in range(len(items)):
        key = list(sorted_MIS_table)[-1]
        if sorted_MIS_table[key]>support[key]:
            support.pop(key)
            sorted_MIS_table.pop(key)
        else :
            LMS = sorted_MIS_table[key]
            break

    for key in list(sorted_MIS_table):
        if support[key]<LMS:
            support.pop(key)
            sorted_MIS_table.pop(key)

    # test noisy support
    # with open('noisy_support.csv', 'w') as f:
    #     for key in support.keys():
    #         f.write("%s,%s\n"%(key,support[key]))
    # test LMS-frequent items and noisy support
    # with open('LMS_frequent_items&support.csv', 'w') as f:
    #     for key in support.keys():
    #         f.write("%s,%s\n"%(key,support[key]))
    # # test MIS
    # with open('MIStable.csv', 'w') as f:
    #     for key in sorted_MIS_table.keys():
    #         f.write("%s,%s\n"%(key,sorted_MIS_table[key]))

    #time_used = time() - time_start
    #print('MISTable&frequent 1-itemset. Running time: {:.3f} seconds.'.format(time_used))
    #return sorted_frequent_items, MIS_table
    return sorted_MIS_table, support, LMS


# delete infrequent items w.r.t LMS in transactions and sort item by MIStable in descending order
def SortTransactions(dataset,sorted_MIS_table):
    #time_start = time()
    final_transactions = []
    itera =[] #not important
    for transaction in dataset:
        for item in transaction:
            if item not in sorted_MIS_table:
                continue
            itera.append(item)
        c = itera.copy()
        final_transactions.append(c)
        itera.clear()
    
    # with open('final_dataset.csv', 'w',newline="") as f:
    # #     #for key in dataset.keys():
    # #     #    f.write("%s,%s\n"%(key,dataset[key]))
    #     writer = csv.writer(f)
    #     writer.writerows(final_transactions)

    final_sorted_transactions =[]
    for transaction in final_transactions:
        final_sorted_transactions.append(sorted(transaction,key = sorted_MIS_table.get,reverse = True))
    
    # with open('final_dataset_sorted.csv', 'w',newline="") as f:
    # #     #for key in dataset.keys():
    # #     #    f.write("%s,%s\n"%(key,dataset[key]))
    #     writer = csv.writer(f)
    #     writer.writerows(final_sorted_transactions)
    

    #time_used = time() - time_start
    #print('Sort transasctions. Running time: {:.3f} seconds.'.format(time_used))
    return final_sorted_transactions

if __name__ == '__main__': #if file wasn't imported.
    T, n = ReadDataset('T10I4D100K')
    truncatedT, items, truncated_length = TruncateDatabase(T,0.05,n)
    print(truncated_length)
    sorted_MIS_table, support, LMS = MISTable(truncatedT,items,n,1,truncated_length,0.01,0.25)
    SortTransactions(truncatedT,sorted_MIS_table)
    #print('preprocess')