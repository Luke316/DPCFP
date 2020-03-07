from time import time
from dataset_processing import TruncateDatabase, ReadDataset
from preprocess_phase import MISTable
from pprint import pprint
import csv

class FPMEtreeNode:
    def __init__(self,name,MIS,sup):
        self.name = name
        self.MIS = MIS
        self.sup = sup
    # level 
    # parent 
    # child
    # def setLeft(self, left):
    #     self.left = left
    # def setRight(self, right):
    #     self.right = right 

# traverse to find FP
# recursive
# def DFSTraversal()

# delete infrequent item in transactions and sort item by mistable in asending order
def SortTransactions(dataset,sorted_frequent_items,MISTable):
    time_start = time()
    final_transactions = []
    itera =[] #not important
    for transaction in dataset:
        for item in transaction:
            if item not in sorted_frequent_items:
                continue
            itera.append(item)
        c = itera.copy()
        final_transactions.append(c)
        itera.clear()
    
    with open('final_dataset.csv', 'w',newline="") as f:
    #     #for key in dataset.keys():
    #     #    f.write("%s,%s\n"%(key,dataset[key]))
        writer = csv.writer(f)
        writer.writerows(final_transactions)

    final_sorted_transactions =[]
    for transaction in final_transactions:
        final_sorted_transactions.append(sorted(transaction,key = MISTable.get))
    
    with open('final_dataset_sorted.csv', 'w',newline="") as f:
    #     #for key in dataset.keys():
    #     #    f.write("%s,%s\n"%(key,dataset[key]))
        writer = csv.writer(f)
        writer.writerows(final_sorted_transactions)

    time_used = time() - time_start
    print('Sort transasctions. Running time: {:.3f} seconds.'.format(time_used))
    return

# build the FPME-tree
# def FPSpanning(itemset,extensions_itemset,MISTable, max_height) :
# join
#     for itemsets in extensions_itemset:
#         FPs = FPs

#     return 

# support propagate to root 
# def Propagate


if __name__ == '__main__': 
    T, n = ReadDataset('T10I4D100K')
    truncatedT, items, truncated_length = TruncateDatabase(T,0.05,n)
    sorted_frequent_items, MIS_table = MISTable(truncatedT,items,n,1,truncated_length,0.01,0.25)
    SortTransactions(truncatedT,sorted_frequent_items,MIS_table)