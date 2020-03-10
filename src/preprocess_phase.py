from collections import OrderedDict
from random import sample
import numpy as np
from dataset_processing import DifferentItemsCount, TruncateDatabase, ReadDataset
from time import time
from pprint import pprint
import csv

#from dataset_processing import init_T

# def NoisySupportCount(T, items,n,epsilon,truncated_length):
#     #init support with 0
#     support = dict.fromkeys(items, 0) 

#     #scan dataset to get origin support
#     for transaction in T:
#         for item in transaction:
#             if item in items:
#                 support[item]=support.get(item) + 1    
#     #pprint (support)
#     # with open('origin_support.csv', 'w') as f:
#     #     for key in support.keys():
#     #         f.write("%s,%s\n"%(key,support[key]))

#     # can use the same dictionary if need to reduce memory
#     #sensitivity = truncated_length/n
#     for item in support.keys():
#         #support[item] = support.get(item)/n + np.random.laplace(0, sensitivity / epsilon)
#         noisy_support[item] = noisy_support.get(item) + np.random.laplace(0, truncated_length/ epsilon)
#     # with open('noisy_support.csv', 'w') as f:
#     #     for key in noisy_support.keys():
#     #         f.write("%s,%s\n"%(key,noisy_support[key]))

#     sorted_noisy_support={k: v for k, v in sorted(noisy_support.items(), key=lambda item: item[1],reverse = True)}
#     # with open('sorted_noisy_support.csv', 'w') as f:
#     #     for key in sorted_noisy_support.keys():
#     #         f.write("%s,%s\n"%(key,sorted_noisy_support[key]))

#     #pprint (sorted_support)
#     return sorted_noisy_support, support

def MISTable(T, items,n,epsilon,truncated_length,threshold, beta): #beta in DPARM = 0.25
    time_start=time()
    #init support with 0
    support = dict.fromkeys(items, 0) 

    #scan dataset to get origin support
    #can use collections.Counter() to speed up 
    for transaction in T:
        for item in transaction:
            if item in items:
                support[item]=support.get(item) + 1    #origin support
    # test
    with open('original_support.csv', 'w') as f:
        for key in support.keys():
            f.write("%s,%s\n"%(key,support[key]))

    sensitivity = truncated_length/n
    MIS_table = dict.fromkeys(items, 0)
    frequent_items = dict.fromkeys(items,1.1)
    for item in support.keys():
        support[item] = support.get(item)/n + np.random.laplace(0, sensitivity / epsilon) # noisy support
        MIS_table[item] = max(beta*support[item],threshold) #if beta =0, the MIS is basically threshold and equals to FIM
        if (support[item] >= MIS_table[item]):
            #print('the support is bigger than MIS',item,'sup',support[item],'MIS',MIS_table[item])
            frequent_items[item] = support[item]
        else:
            frequent_items.pop(item,None)

    # sort the frequent item in ascending order
    sorted_frequent_items={k: v for k, v in sorted(frequent_items.items(), key=lambda item: item[1])}

    # test
    with open('noisy_support.csv', 'w') as f:
        for key in support.keys():
            f.write("%s,%s\n"%(key,support[key]))
    # test
    with open('sorted_frequent_items&support.csv', 'w') as f:
        for key in sorted_frequent_items.keys():
            f.write("%s,%s\n"%(key,sorted_frequent_items[key]))

    time_used = time() - time_start
    print('MISTable&frequent 1-itemset. Running time: {:.3f} seconds.'.format(time_used))
    return sorted_frequent_items, MIS_table

if __name__ == '__main__': #if file wasn't imported.
    T, n = ReadDataset('T10I4D100K')
    truncatedT, items, truncated_length = TruncateDatabase(T,0.05,n)
    MISTable(truncatedT,items,n,1,truncated_length,0.01,0.25)
    #print('preprocess')