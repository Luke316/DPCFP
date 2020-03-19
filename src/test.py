import pdb
import itertools
from anytree import NodeMixin, RenderTree
from ordered_set import OrderedSet
import numpy as np
import copy
import csv


class FPMEtree:
    def __init__(self):
        self.root = FPMETreeNode([],0,0)

    def add(self,transaction,MISTable):
        node = self.root
        
        for item in transaction:
            next_point = node.search(item)
            MIS = MISTable.get(transaction[0])
            
            if not next_point:
                #next_point = FPMETreeNode(item,MIS,np.random.laplace(0, 5/6))
                next_point = FPMETreeNode(item,MIS,0)
                next_point.parent = node

            node = next_point
        node.sup += 1

    # def update(self):
    #     # for child in self.root.children:
    #     #     print('child name = ', child.name)
    #     #     for child_child in child.children:
    #     #         print('child_child.name',child_child.name)
    #     #         child.sup = child.sup + child_child.sup
    #     #         self.update
    #     node = self.root 
    #     node.update()
    #     # for descendant in node.descendants:
    #     #     node.sup = node.sup + descendant.sup




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
    
    # def update(self):
    #     # for child in self.children:
    #     #     print('child name = ', child.name)
    #     #     for child_child in child.children
    #     #     child.sup = child.sup + child.children.sup
    #     #     self.update(child.children)
    #     for descendant in self.descendants:
    #         self.sup = self.sup + descendant.sup

    
def Update(treenode):
    for child in treenode.children:
        Update(child)
        treenode.sup += child.sup


def Traversal(node):
    with open('output2.csv','a+',newline='') as f:
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
                #print(frequent_itemsets2)
                #with open('output.csv', 'w') as w:
                writer.writerow([frequent_itemsets1,child.sup])
                #writer.writerow([frequent_itemsets1,support[frequent_itemsets1]])



transactions=[[1,2,3],[1,4,6],[1,2,4],[2,5,6],[1,2,3],[3,4,6],[1,2],[1,2,4,6,7]]
dict1={1:1,2:1,3:2,4:2,5:3,6:3}

master = FPMEtree()
for transaction in transactions:
    master.add(transaction,dict1)

#master.update()
Update(master.root)


for pre, _, node in RenderTree(master.root):
    treestr = u"%s%s ,%s, %s" % (pre, node.name , node.MIS ,node.sup)
    print(treestr.ljust(8))

Traversal(master.root)






# itemset is a list, extension is a list of list
# def FPMETree(itemset,extension,maxlength,MISTable):
#     if type(itemset) != FPMEtreeNode:
#         itemset = FPMEtreeNode(itemset,0,0)
#         print('kkkkk')
    
#     FPSpanning(itemset,extension,maxlength,MISTable)
#     for pre, _, node in RenderTree(itemset):
#         treestr = u"%s%s%s" % (pre, node.name, node.MIS)
#         # print(treestr.ljust(8), node.MIS, node.sup)

#         print(treestr.ljust(8))
    
#     return
    

# def FPSpanning(itemset,extension,maxlength,MISTable):

#     #extension2 = list(set(itertools.chain.from_iterable(extension)))
#     extension2 = list(OrderedSet(itertools.chain.from_iterable(extension)))
#     print('extension2',extension2)
#     for ext in extension:
#         #print('ext=',ext)
#         MIS=MISTable.get(ext[0])
#         newnode=FPMEtreeNode(ext,MIS,0,parent=itemset)
#         length = len(ext)
#         if(length<maxlength):
#             newcomb = []
#             b = ext.copy()
#             print('b=',b)
#             i = extension2.index(b.pop())
#             extension2 = extension2[i+1:]
#             for item in extension2:
#                 a=[]
#                 a.append(item)
#                 newcomb.append(ext + a)
#             FPSpanning(newnode,newcomb,maxlength,MISTable)
#     return

# dict1={1:0.1,2:0.2,3:0.3,4:0.4,5:0.5}

# FPMETree([],[[1],[2],[3],[4],[5]],4,dict1)


# graph = {
#     '1':['1,2','1,3','1,4'],
#     '2':['2,3','2,4'],
#     '3':['3,4'],
#     '4':[],
#     '1,2':['1,2,3','1,2,4'],
#     '1,3':['1,3,4'],
#     '1,4':[],
#     '2,3':['2,3,4'],
#     '2,4':[],
#     '3,4':[],
#     '1,2,3':['1,2,3,4'],
#     '1,2,4':[],
#     '1,3,4':[],
#     '2,3,4':[],
#     '1,2,3,4':[]
# }

# visited = [] # Array to keep track of visited nodes.

# def dfs(visited, graph, node):
#     if node not in visited:
#         print(node)
#         visited.append(node)
#         for neighbour in graph[node]:
#             dfs(visited, graph, neighbour)

# # Driver Code
# dfs(visited, graph, '1')




























# a = [[1,2,4,6,3],[3,2,8,1],[8,6]]
# dict1 = {1:5,2:3,3:9}
# b=[]
# c=[]
# for transaction in a:
#     for index, item in enumerate(transaction):
#         print('item=',item)
#         if item not in dict1:
#             print('item not in dict1', item)
#             continue
#         c.append(item)
#         print(c)
#     d = c.copy()
#     b.append(d)
#     c.clear()


# print (b)

# for index in b:
#     c.append(sorted(index,key=dict1.get))

# print(c)


# print(b)

# a = [[1,2,4,6,2],[2,8,1],[8,6]]
# dict1 = {1:5,2:8,3:9}

# for transaction in a:
#     print(transaction)

#     for index, item in enumerate(transaction):
#         print('item=',item)
#         if item not in dict1:
#             print('item not in dict1', item)
#             print(item)
#             pdb.set_trace()
#             transaction.remove(item)
#             pdb.set_trace()
#             #continue
#         # else:
#         #     #transaction.remove(item)
#         #     continue
       
# print(a)

# for transaction in a:
#     print(transaction)
#     for item in transaction:
#         while (item not in dict1):
#             transaction.remove(item)

# print(a)