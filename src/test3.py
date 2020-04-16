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
                # next_node = MISTreeNode(item,np.random.laplace(0, length/epsilon/n))
                next_node = MISTreeNode(item,0) #0328
                next_node.parent = node
                self.UpdateHeaderTable(next_node)

            node = next_node
        node.sup += 1/n
    
    def addPrefixPath(self,prefixPath,supportBeta,LMS):
        # the last element of the prefixpath contains the path support
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
            else:
                next_node.sup += pathCount
            
            node = next_node

    #node-link    
    def UpdateHeaderTable(self,node):
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
            if support[items[0]] >= MISTable[prefix[-1]]:
                i = []
                i.append(items)
                frequent_itemsets[str(prefix+i)]= support[items[0]]

        else: 
            cfpgrowth(tree,prefix,prefixSup,MISTable,support,frequent_itemsets,LMS)

    else:
        cfpgrowth(tree,prefix,prefixSup,MISTable,support,frequent_itemsets,LMS)

       
def cfpgrowth(tree,prefix,prefixSup,MISTable,support,frequent_itemsets,LMS):
    items = list(tree.header_table.keys())
    for item in items:
        
        print(item)
        MIS = MISTable[item] if(len(prefix))==0 else MISTable[prefix[-1]]
        #pdb.set_trace()

        if support[item]<MIS:
            continue
                    
        betaSup = prefixSup if prefixSup < support[item] else support[item]
        if support[item]>=MIS:
            #pdb.set_trace()
            i = []
            i.append(item)
            frequent_itemsets[str(prefix+i)]= betaSup
        
        #add beta's prefixPaths a.k.a conditional pattern base
        prefixPaths = []#list of path tuples
        for node in tree.header_table[item]:
            prefixPaths.append(node.path[1:])#tuple of nodes # neglect the null root
        #pdb.set_trace()

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
        for prefixPath in prefixPaths:
            betaTree.addPrefixPath(prefixPath,supportBeta,LMS)

        for pre, _, node in RenderTree(betaTree.root):
            treestr = u"%s%s , %s" % (pre, node.name ,node.sup)
            print(treestr.ljust(8))
        
        pdb.set_trace()
        
        #print(len(betaTree.root.children))
        #beta = []
        if len(betaTree.root.children) > 0:
		# create beta
            #pdb.set_trace()
            print('prefix=', prefix)
            prefix.append(item)
            beta = list(prefix)
            print("beta=",beta)
            CFPGrowth(betaTree,beta,betaSup,MISTable,supportBeta,frequent_itemsets,LMS)
            print('yoyoyo')


        



if __name__ == '__main__':
    # dataset = 'retail'
    # print('Dataset = ' ,dataset)
    # T, n = ReadDataset(dataset)
    # ep_1,ep_2,ep_3 = 0.05,0.5,1
    # #T10I4D100K retail kosarak BMS1 BMS2 accidents BMS-POS
    # truncatedT, items, truncated_length = TruncateDatabase(T,ep_1,n)
    # sorted_MIS_table, support, LMS = MISTable(truncatedT,items,n,ep_2,truncated_length,0.01,0.25)
    # final_sorted_transactions = SortTransactions(truncatedT,sorted_MIS_table)

    a = [[1,2],[1,5,6],[3,4],[1,2,8],[3,4],[1,3],[1,2],[5,6],[3,4,7],[1,2],[1,2],[1,3],[1,2],[2,5,6,7],[3,4],[1,2,4],[3,4],[1,3],[1,2,5],[3,4]]
    sorted_MIS_table = {1:10,3:10,2:8,4:6,5:3,6:3,7:3,8:2}
    support = {1:12,3:9,2:9,4:7,5:4,6:3,7:2,8:1}

    time_start = time()
    master = MIStree()
    for transaction in a:
        master.AddTransaction(transaction,20,0,0)
    
    time_used = time() - time_start
    print('FPMISTree Constructed. Running time: {:.3f} seconds.'.format(time_used))
    
    time_start = time()
    Update(master.root)
    # for pre, _, node in RenderTree(master.root):
    #     treestr = u"%s%s , %s" % (pre, node.name ,node.sup)
    #     print(treestr.ljust(8))
    time_used = time() - time_start
    print('FPMISTree Updated. Running time: {:.3f} seconds.'.format(time_used))

    time_start = time()
    frequent_itemsets={}
    CFPGrowth(master, [], 20,sorted_MIS_table,support,frequent_itemsets,3/20)
    # test mining result
    with open('mining_result.csv', 'w') as f:
        for key in frequent_itemsets.keys():
            f.write("%s,%s\n"%(key,frequent_itemsets[key]))
    time_used = time() - time_start
    print('Traversal Finished . Running time: {:.3f} seconds.'.format(time_used))
