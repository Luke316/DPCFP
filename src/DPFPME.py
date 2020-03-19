from time import time
from dataset_processing import TruncateDatabase, ReadDataset
from preprocess_phase import MISTable, SortTransactions
import csv
import numpy as np
import copy 
from anytree import NodeMixin, RenderTree

#from ordered_set import OrderedSet
#import itertools

# class FPMEtree:
#     z=1
# class FPMEtreeNode(FPMEtree,NodeMixin):
#     def __init__(self,name,MIS,sup,children=None,parent=None):
#         self.name = name
#         self.MIS = MIS
#         self.sup = sup
#         self.parent = parent
#         if children:
#             self.children = children

# # itemset is a list, extension is a list of list
# def FPMETree(itemset,extension,maxlength,MIS_table):
#     time_start = time()

#     if type(itemset) != FPMEtreeNode:
#         itemset = FPMEtreeNode(itemset,0,0)
#         #print('kkkkk')
    
#     FPSpanning(itemset,extension,maxlength,MIS_table)
#     # for pre, _, node in RenderTree(itemset):
#     #     treestr = u"%s%s %s" % (pre, node.name,node.MIS)
#     #     # print(treestr.ljust(8), node.MIS, node.sup)

#     #     print(treestr.ljust(8))
    
#     time_used = time() - time_start
#     print('Build Tree. Running time: {:.3f} seconds.'.format(time_used))
#     return 
    
# '''
# Input: itemset is a list, extension is a list of list
# '''
# def FPSpanning(itemset,extension,maxlength,MIS_table):

#     # extensions = dict.fromkeys(extension,None)
#     # items = list(extensions.keys())

#     items = list(OrderedSet(itertools.chain.from_iterable(extension)))
#     print('items = ',items)

#     for ext in extension:
#         #print('ext=',ext)
#         MIS=MIS_table.get(ext[0])
#         newnode=FPMEtreeNode(ext,MIS,0,parent=itemset)
        
#         length = len(ext)
#         if(length<maxlength):
#             newcomb = []
#             b = ext.copy()
#             i = items.index(b.pop())
#             items = items[i+1:]

#             for item in items:
#                 a=[]
#                 a.append(item)
#                 newcomb.append(ext + a)
#             FPSpanning(newnode,newcomb,maxlength,MIS_table)
#         # example:[1,2,3,4,5]-> node=[2,3] =>use[2,3] to combine with [4,5]
       
#         #print('newcombination=',newcomb,type(newcomb))
        
#         #heuristic 1
        
class FPMEtree():
    def __init__(self):
        self.root = FPMETreeNode([],0,0)

    def add(self,transaction,MISTable,n,epsilon,length):
        node = self.root
        for item in transaction:
            next_node = node.search(item)
            MIS = MISTable.get(transaction[0])

            
            if not next_node:
                next_node = FPMETreeNode(item,MIS,np.random.laplace(0, length/epsilon/n))            
                next_node.parent = node

            node = next_node
        node.sup += 1/n


class TreeNodeBase():
    z=1
class FPMETreeNode(TreeNodeBase,NodeMixin):
    def __init__(self,name,MIS,sup,children=None,parent=None):
        self.name = name
        self.MIS = MIS
        self.sup = sup
        self.parent = parent
        if children :
            self.children = children

    def search(self,item):
        node_names =[]
        for node in self.children:
            node_names.append([node.name])
            #print('og_child_names',node_names)

        if [item] in node_names:
            #print('index=',node_names.index([item]))
            return self.children[node_names.index([item])]

        return False

def Update(node):
    for child in node.children:
        Update(child)
        if child.sup<0:#is this DP?
            child.sup=0
        node.sup += child.sup


# traverse to find FP
# DFS traversal
def Traversal(node):
    with open('output.csv','a',newline='') as f:
        writer = csv.writer(f)
        for child in node.children:
            #print(child.name)
            if child.sup>=child.MIS:
                Traversal(child)
                frequent_itemsets1= []
                for path in child.path:
                    if path.name != []:
                        #print(path.name)
                        frequent_itemsets1.append(path.name)
                writer.writerow([frequent_itemsets1,child.sup])
    


if __name__ == '__main__': 
    dataset = 'retail'
    print('Dataset = ' ,dataset)
    T, n = ReadDataset(dataset)
    #T10I4D100K retail kosarak BMS1 BMS2 accidents BMS-POS
    truncatedT, items, truncated_length = TruncateDatabase(T,0.05,n)
    sorted_frequent_items, MIS_table = MISTable(truncatedT,items,n,1,truncated_length,0.01,0.25)
    final_sorted_transactions = SortTransactions(truncatedT,sorted_frequent_items,MIS_table)
    #print([[i] for i in sorted_frequent_items])
    #FPMETree([],[[i] for i in sorted_frequent_items],4,MIS_table)
    
    time_start = time()
    master = FPMEtree()
    for transaction in final_sorted_transactions:
        master.add(transaction,MIS_table,n,1,truncated_length)
    time_used = time() - time_start
    print('FPMETree Constructed. Running time: {:.3f} seconds.'.format(time_used))
    
    time_start = time()
    Update(master.root)
    time_used = time() - time_start
    print('FPMETree Updated. Running time: {:.3f} seconds.'.format(time_used))

    time_start = time()
    Traversal(master.root)
    time_used = time() - time_start
    print('Traversal Finished . Running time: {:.3f} seconds.'.format(time_used))

    # for pre, _, node in RenderTree(master.root):
    #     treestr = u"%s%s %s %s" % (pre, node.name,node.MIS, node.sup)
    #     print(treestr.ljust(8))
