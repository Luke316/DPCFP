from collections import OrderedDict, Counter
import numpy as np
from random import sample
from time import time
import csv
from pprint import pprint

def ReadDataset(dataset):
    """Read the dataset and unify the format of T"""
    #time_start = time()
    T =[]

    if (dataset == 'accidents') or (dataset == 'kosarak') or (dataset == 'retail') or \
            (dataset == 'mushroom') or (dataset == 'chess'):
        with open('..\\datasets\\real_world\\{:s}\\{:s}.dat'.format(dataset, dataset), 'r') as raw:
            for transaction in raw.readlines():
                transaction = transaction.strip('\n') #remove line feed
                transaction = transaction.split(' ') # use space to split strings 
                if dataset != 'kosarak':
                    transaction.pop()
                if dataset != 'retail':
                    transaction = [int(item) for item in transaction]
                elif dataset == 'retail':
                    transaction = [int(item) + 1 for item in transaction]
                T.append(transaction)

    elif dataset == 'T10I4D100K':
        with open('..\\datasets\\synthetic\\{:s}.dat'.format(dataset), 'r') as raw:
            for transaction in raw.readlines():
                transaction = transaction.strip('\n')
                transaction = transaction.split(' ')
                transaction.pop()
                transaction = [int(item) for item in transaction]
                T.append(transaction)

    elif dataset == 'BMS1' or dataset == 'BMS2':
        with open('..\\datasets\\real_world\\{:s}.txt'.format(dataset), 'r') as raw:
            for transaction in raw.readlines():
                transaction = transaction.strip('\n')
                transaction = transaction.split(' ')
                transaction = [int(item) for item in transaction]
                T.append(transaction)

    elif dataset == 'BMS-POS':
        with open('..\\datasets\\real_world\\{:s}.dat'.format(dataset), 'r') as raw:
            T_dict = OrderedDict()
            for row in raw.readlines():
                row = row.strip('\n')
                row = row.split('\t')

                if row[0] in T_dict.keys():
                    T_dict[row[0]].append(int(row[1]) + 1)
                elif row[0] not in T_dict.keys():
                    T_dict[row[0]] = [int(row[1]) + 1]

        T = list(T_dict.values())

    n = len(T)
    #time_used = time() - time_start
    #print('Read the {:s} dataset containing {:d} transactions. Running time: {:.3f} seconds.'.format(dataset, n, time_used))

    return T, n


def DifferentItemsCount(dataset):
    items = set()
    for transaction in dataset:
        for item in transaction:
            items.add(item)
    
    items_count = len(items)
    return items_count, items


def EstimateDistribution(T,number_of_transactions,epsilon,number_of_diff_items ):
    #get z_1 to z_n in Alg.1 line 9
    length_distribution = [0] * number_of_diff_items
    for transaction in T:
        length = len(transaction)
        length_distribution[length-1] += 1  # index = length - 1

    noisy_length_distribution = []
    for count in length_distribution:
        if epsilon !=0:
            noisy_count = int(max(count + np.random.laplace(0, 1 / epsilon), 0))/number_of_transactions  # add Laplace noise and set negative to 0
        else:
            noisy_count = count/number_of_transactions #0328
        noisy_length_distribution.append(noisy_count)
    return noisy_length_distribution


def Truncate(length, T):
    Ts_truncated = []
    for transaction in T:
        truncated_transaction = sample(transaction, min(len(transaction), length))
        Ts_truncated.append(truncated_transaction)
    return Ts_truncated 


def TruncateDatabase(dataset,epsilon,n):
    #time_start = time()
    number_of_diff_items, items = DifferentItemsCount(dataset)
    noisy_length_distribution = EstimateDistribution(dataset, n, epsilon, number_of_diff_items)
    
    summation =0.0
    truncated_length = 0.0
<<<<<<< HEAD
    truncated_length2= 0.0
    b = False #make sure loop continue without changing truncated_length
    for index, noisy_count in enumerate(noisy_length_distribution, start=1) :
        summation += noisy_count
        if summation >= (0.95) and b == False:
            truncated_length = index
            b = True
            # break
        if summation >= (0.99):
            truncated_length2 = index
            break
    # print(truncated_length,truncated_length2)

    # number_of_long_items =0
    # total_truncated_items=0
    # for transaction in dataset:
    #     if len(transaction)>truncated_length:
    #         number_of_long_items+=1
    #         total_truncated_items = total_truncated_items + len(transaction)-truncated_length
    # print(number_of_long_items,total_truncated_items,total_truncated_items/number_of_long_items)

    #print('truncated_length=',truncated_length)
    T_truncated= Truncate(truncated_length,dataset) 
    T_truncated2=Truncate(truncated_length2,dataset)
    
    #time_used = time() - time_start
    #print('Truncate Database. Running time: {:.3f} seconds.'.format(time_used))
    return T_truncated,T_truncated2 , items, truncated_length
=======
    for index, noisy_count in enumerate(noisy_length_distribution, start=1) :
        summation += noisy_count
        if summation >= (0.85):
            truncated_length = index
            break
    
    #print('truncated_length=',truncated_length)
    T_truncated= Truncate(truncated_length,dataset) 
    
    #time_used = time() - time_start
    #print('Truncate Database. Running time: {:.3f} seconds.'.format(time_used))
    return T_truncated, items, truncated_length
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf


if __name__ == '__main__': #if file wasn't imported.
    #D_name = 'accidents'
<<<<<<< HEAD
    # D_name = 'kosarak'
    D = ['BMS1', 'BMS2','retail','kosarak','BMS-POS','T10I4D100K']
    # To clarify, the initial dataset is called D
    # after reading the dataset, I call it T
    for D_name in D:
        T, n = ReadDataset(D_name)
        truncatedT,truncatedT2, items, truncated_length = TruncateDatabase(T,0.05,n)
=======
    D_name = 'T10I4D100K'

    # To clarify, the initial dataset is called D
    # after reading the dataset, I call it T
    T, n = ReadDataset(D_name)
    truncatedT, items, truncated_length = TruncateDatabase(T,0.05,n)
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf

