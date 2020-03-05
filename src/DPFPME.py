from time import time
from dataset_processing import TruncateDatabase, ReadDataset
from preprocess_phase import MISTable

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

# read dataset and sort dataset by mistable
def SortTransactions(dataset,sorted_frequent_items,MISTable):
    for transaction in dataset:
        for item in transaction:
            if item not in sorted_frequent_items:
                transaction.remove(item)

    
    return

# build the FPME-tree
# def FPSpanning(itemset,extensions_itemset,MISTable, max_height) :
# join
#     for itemsets in extensions_itemset:
#         FPs = FPs

#     return 

# support propagate to root 


if __name__ == '__main__': 
    T, n = ReadDataset('T10I4D100K')
    truncatedT, items, truncated_length = TruncateDatabase(T,0.05,n)
    sorted_frequent_items, MIS_table = MISTable(truncatedT,items,n,1,truncated_length,0.01,0.25)
    SortTransactions(truncatedT,sorted_frequent_items,MIS_table)