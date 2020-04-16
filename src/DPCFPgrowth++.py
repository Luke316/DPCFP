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
    header_table = {}

    def __init__(self):
        self.root = MISTreeNode([],0,0)

    def AddTransaction(self,transaction,n,epsilon,length):
        node = self.root
        for item in transaction:
            next_node = node.SearchChildNode(item)
            
            if not next_node:
                # next_node = MISTreeNode(item,np.random.laplace(0, length/epsilon/n))
                next_node = MISTreeNode(item,0) #0328
                next_node.parent = node
                self.UpdateHeaderTable(next_node)

            node = next_node
        node.sup += 1/n
    
    def AddPrefixPath(self,prefixPath,supportBeta,LMS):
        pathCount = prefixPath[-1].sup
        node = self.root
        for item in prefixPath:

            #pdb.set_trace()
            if item == prefixPath[-1]:
                continue
            if supportBeta[item.name]<LMS :
                continue
            
            
            
            next_node = node.SearchChildNode(item)
            
            if not next_node:
                next_node = MISTreeNode(item,pathCount)
                next_node.parent = node
                self.UpdateHeaderTable(next_node)
                node = next_node
            else:
                node.sup += pathCount
                node = next_node

        
    def UpdateHeaderTable(self,node):#node-link
        if node.name not in self.header_table:
            self.header_table[node.name] = [node]
        else:
            self.header_table[node.name].append(node)

    # def InfrequentLeafNodePruning(self, support , sorted_MIS_table):
    #     for item in support.keys():
    #         if support[item] < sorted_MIS_table[item]:
    #             if item
                

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

def CFPGrowth(tree,prefix,prefixSup,MISTable,support,frequent_itemsets,LMS):
    items = list(tree.header_table.keys())
    
    # if the tree only has one item and it only contains one path, check frequent
    if len(tree.header_table) == 1: 
        if len(tree.header_table[items[0]]) == 1:
            if support[items[0]] > MISTable[items[0]]:
                frequent_itemsets[items[0]]= support[items[0]]

        else: 
            cfpgrowth(tree,prefix,prefixSup,MISTable,support,frequent_itemsets,LMS)

    else:
        cfpgrowth(tree,prefix,prefixSup,MISTable,support,frequent_itemsets,LMS)

       
def cfpgrowth(tree,prefix,prefixSup,MISTable,support,frequent_itemsets,LMS):
    items = list(tree.header_table.keys())
    for item in items:
        #pdb.set_trace()
        print(item)
        pdb.set_trace()
        if support[item]<MISTable[item]:
            continue
                    
        betaSup = prefixSup if (prefixSup < support[item]) else support[item]
        if support[item]>=MISTable[item]:#unnecessary
            frequent_itemsets[item]= betaSup
        
        #add prefixPaths 
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
                        supportBeta[node.name] += pathCount

        #construct beta's conditional tree
        betaTree = MIStree()
        for prefixPath in prefixPaths:
            betaTree.AddPrefixPath(prefixPath,supportBeta,LMS)

        if (len(betaTree.root.children) > 0):
		# create beta
            #pdb.set_trace()

            beta = prefix.append(item)

            CFPGrowth(betaTree,beta,betaSup,MISTable,supportBeta,frequent_itemsets,LMS)


        



if __name__ == '__main__':
    dataset = 'retail'
    print('Dataset = ' ,dataset)
    T, n = ReadDataset(dataset)
    ep_1,ep_2,ep_3 = 0.05,0.5,1
    #T10I4D100K retail kosarak BMS1 BMS2 accidents BMS-POS
    truncatedT, items, truncated_length = TruncateDatabase(T,ep_1,n)
    sorted_MIS_table, support, LMS = MISTable(truncatedT,items,n,ep_2,truncated_length,0.01,0.25)
    final_sorted_transactions = SortTransactions(truncatedT,sorted_MIS_table)

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
    with open('mining_result.csv', 'w') as f:
        for key in frequent_itemsets.keys():
            f.write("%s,%s\n"%(key,frequent_itemsets[key]))
    time_used = time() - time_start
    print('Traversal Finished . Running time: {:.3f} seconds.'.format(time_used))
