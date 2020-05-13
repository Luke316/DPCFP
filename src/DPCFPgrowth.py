# encoding: utf-8
from collections import defaultdict, namedtuple
from time import time
from dataset_processing import TruncateDatabase, ReadDataset
from preprocess_phase import MISTable, SortTransactions
import csv
import numpy as np
import copy 
from anytree import NodeMixin, RenderTree
import pdb


class MIStree():
    def __init__(self):
        self.header_table = {}
        self.root = MISTreeNode([],0)#name,sup

    def AddTransaction(self,transaction,n,epsilon,length):
        node = self.root
        for item in transaction:
            next_node = node.SearchChildNode(item)
            
            if not next_node:
                if epsilon!=0:
                    next_node = MISTreeNode(item,np.random.laplace(0, scale = (1/n)/epsilon))
                else:
                    next_node = MISTreeNode(item,0) #0328
                next_node.parent = node
                self.UpdateHeaderTable(next_node)

            node = next_node
        node.sup += 1/n
    
    def addPrefixPath(self,prefixPath,supportBeta,LMS):
        # the last element of the prefixpath contains the path minimum support
        pathCount = prefixPath[-1].sup
        node = self.root

        for item in prefixPath:
            if item == prefixPath[-1]:
                continue
            if supportBeta[item.name]<LMS :
                continue
            
            next_node = node.SearchChildNode(item.name)
            if not next_node:
                next_node = MISTreeNode(item.name,pathCount)
                next_node.parent = node
                self.UpdateHeaderTable(next_node)
            else:
                next_node.sup += pathCount
            
            node = next_node

    #node-link    
    def UpdateHeaderTable(self,node):
        if node.name not in self.header_table:
            self.header_table[node.name] = [node]
        else:
            self.header_table[node.name].append(node)
                

class TreeNodeBase():
    # frequent_itemsets = []
    pass

class MISTreeNode(TreeNodeBase,NodeMixin):
    def __init__(self,name,sup,children=None,parent=None):
        self.name = name
        self.sup = sup
        self.parent = parent        
        if children :
            self.children = children
        
    def SearchChildNode(self,item):
        node_names =[]
        for node in self.children:
            node_names.append([node.name])

            if [item] in node_names:
                return self.children[node_names.index([item])]

        return False

def Update(node):
    for child in node.children:
        Update(child)
        node.sup += child.sup
        if child.sup<0:#is this DP?
            child.sup=0
        #node.sup += child.sup

def CFPGrowth(tree,prefix,prefixSup,MISTable,support,frequent_itemsets,LMS):
    items = list(tree.header_table.keys())
    
    # if the tree only has one item and it only contains one path, check frequent
    if len(tree.header_table) == 1: 
        if len(tree.header_table[items[0]]) == 1:
            if support[items[0]] >= MISTable[prefix[-1]]:
                itemset = prefix +items
                itemset.sort()                
                frequent_itemsets[str(itemset)]= support[items[0]]
        else: 
            cfpgrowth(tree,prefix,prefixSup,MISTable,support,frequent_itemsets,LMS)
    else:
        cfpgrowth(tree,prefix,prefixSup,MISTable,support,frequent_itemsets,LMS)

       
def cfpgrowth(tree,prefix,prefixSup,MISTable,support,frequent_itemsets,LMS):
    items = list(tree.header_table.keys())
    for item in items:  
        MIS = MISTable[item] if(len(prefix))==0 else MISTable[prefix[-1]]
        
        if support[item]<MIS:
            continue
                    
        betaSup = prefixSup if prefixSup < support[item] else support[item]
        if support[item]>=MIS:
            i = []
            i.append(item)
            itemset = prefix+i
            itemset.sort()
            frequent_itemsets[str(itemset)]= betaSup          
        
        #add beta's prefixPaths a.k.a conditional pattern base
        prefixPaths = []#list of path tuples
        for node in tree.header_table[item]:
            prefixPaths.append(node.path[1:])#tuple of nodes # neglect the null root

        # get support of the items in the prefixpath
        supportBeta = {}
        for prefixPath in prefixPaths:
            pathCount = prefixPath[-1].sup
            for node in prefixPath:
                
                if node != prefixPath[-1]:
                    if node.name not in supportBeta:
                        supportBeta[node.name] = pathCount
                    else:
                        supportBeta[node.name] = supportBeta[node.name] + pathCount

        #construct beta's conditional tree
        betaTree = MIStree()
        for prefixPath in prefixPaths:#prefixPath is a tuple
            betaTree.addPrefixPath(prefixPath,supportBeta,LMS)

        # for pre, _, node in RenderTree(betaTree.root):
        #     treestr = u"%s%s , %s" % (pre, node.name ,node.sup)
        #     print(treestr.ljust(8))        

        if len(betaTree.root.children) > 0:
		    # create beta
            beta = list(prefix)
            beta.insert(0,item)
            CFPGrowth(betaTree,beta,betaSup,MISTable,supportBeta,frequent_itemsets,LMS)



if __name__ == '__main__':
    dataset = 'retail'
    print('Dataset = ' ,dataset)
    time_start1 = time()
    T, n = ReadDataset(dataset)
    ep_1,ep_2,ep_3 = 0.05,0.02,0.03
    #T10I4D100K retail kosarak BMS1 BMS2 BMS-POS
    truncatedT, items, truncated_length = TruncateDatabase(T,ep_1,n)
    sorted_MIS_table, support, LMS = MISTable(truncatedT,items,n,ep_2,truncated_length,0.01,0.25)
    final_sorted_transactions = SortTransactions(truncatedT,sorted_MIS_table)
    print('MIS Found and Transactions Sorted. Running time: {:.3f} seconds.'.format(time()-time_start1))


    time_start = time()
    master = MIStree()
    for transaction in final_sorted_transactions:
        master.AddTransaction(transaction,n,ep_3,truncated_length)
    time_used = time() - time_start
    print('FPMISTree Constructed. Running time: {:.3f} seconds.'.format(time_used))
    
    time_start = time()
    Update(master.root)
    time_used = time() - time_start
    print('FPMISTree Updated. Running time: {:.3f} seconds.'.format(time_used))

    time_start = time()
    frequent_itemsets={}
    CFPGrowth(master, [], n,sorted_MIS_table,support,frequent_itemsets,LMS)
    # test mining result
    # with open('mining_result.csv', 'w') as f:
    #     for key in frequent_itemsets.keys():
    #         f.write("%s,%s\n"%(key,frequent_itemsets[key]))
    time_used = time() - time_start
    print('CFPGrowth++ Finished . Running time: {:.3f} seconds.'.format(time_used))
    print('Total Running time: {:.3f} seconds.'.format(time()-time_start1))
