from time import time
from dataset_processing import TruncateDatabase, ReadDataset
from preprocess_phase import MISTable
from pprint import pprint
import itertools
import csv
from anytree import NodeMixin, RenderTree
from ordered_set import OrderedSet

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
        
class FPMEtree:
    def __init__(self):
        self.root = FPMETreeNode([],None,None)

    def add(self,transaction):
        point = self.root
        for item in transaction:
            # next_point = FPMETreeNode(item,None,None)
            next_point = point.search(item)
            
            if not next_point:
                next_point = FPMETreeNode(item,None,None)
                next_point.parent = point

            point = next_point

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

# traverse to find FP
# graph is a dict 
def DFSTraversal(visited,graph,node):
    if node not in visited:
        print(node.name)
        visited.append(node)
        for neighbor in graph[node]:
            DFSTraversal(visited, graph, neighbor)

# support propagate to root 
# def Propagate

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
    
    # with open('final_dataset.csv', 'w',newline="") as f:
    # #     #for key in dataset.keys():
    # #     #    f.write("%s,%s\n"%(key,dataset[key]))
    #     writer = csv.writer(f)
    #     writer.writerows(final_transactions)

    final_sorted_transactions =[]
    for transaction in final_transactions:
        final_sorted_transactions.append(sorted(transaction,key = sorted_frequent_items.get))
    
    # with open('final_dataset_sorted.csv', 'w',newline="") as f:
    # #     #for key in dataset.keys():
    # #     #    f.write("%s,%s\n"%(key,dataset[key]))
    #     writer = csv.writer(f)
    #     writer.writerows(final_sorted_transactions)
    

    time_used = time() - time_start
    print('Sort transasctions. Running time: {:.3f} seconds.'.format(time_used))
    return final_sorted_transactions



if __name__ == '__main__': 
    T, n = ReadDataset('retail')
    #T10I4D100K retail
    truncatedT, items, truncated_length = TruncateDatabase(T,0.05,n)
    sorted_frequent_items, MIS_table = MISTable(truncatedT,items,n,1,truncated_length,0.01,0.25)
    final_sorted_transactions = SortTransactions(truncatedT,sorted_frequent_items,MIS_table)
    #print([[i] for i in sorted_frequent_items])
    #FPMETree([],[[i] for i in sorted_frequent_items],4,MIS_table)
    master = FPMEtree()
    time_start = time()

    for transaction in final_sorted_transactions:
        master.add(transaction)
    time_used = time() - time_start
    print('FPMETree Constructed. Running time: {:.3f} seconds.'.format(time_used))



    # for pre, _, node in RenderTree(master.root):
    #     treestr = u"%s%s " % (pre, node.name,)
    #     # print(treestr.ljust(8), node.MIS, node.sup)
    #     print(treestr.ljust(8))
