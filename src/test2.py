import pdb
import itertools
from anytree import NodeMixin, RenderTree
from ordered_set import OrderedSet

list1=[1,5,9,6,8,2,4]
dict1 = {1:6, 3:8, 4:9, 5:1, 6:2, 7:3, 8:5, 9:2, 2:7}
print(sorted(list1,key = dict1.get))

# class FPMEtree:
#     def __init__(self):
#         self.root = FPMETreeNode([],0,0)

#     def add(self,transaction):
#         point = self.root
#         for item in transaction:
#             next_point = point.search(item)
#             if next_point:
#                 # There is already a node in this tree for the current
#                 # transaction item; reuse it.
#                 #next_point.increment()
#                 k=[]
#             else:
#                 # Create a new point and add it as a child of the point we're
#                 # currently looking at.
#                 next_point = FPMETreeNode(item,0,0)
#                 point.add(next_point)

#                 # Update the route of nodes that contain this item to include
#                 # our new node.
#                 #self._update_route(next_point)

#             point = next_point



# class FPMETreeNode():
#     def __init__(self,name,MIS,sup,children=None,parent=None):
#         self.name = name
#         self.MIS = MIS
#         self.sup = sup
#         self.parent = parent
#         self.children = {}


#     def add(self,child):
#         if not isinstance(child, FPMETreeNode):
#             raise TypeError("Can only add other FPMETreeNodes as children")

#         if child.name not in self.children:
#             self.children[child.name] = child
#             child.parent = self

#     def search(self,item):
#         try:
#             return self.children[item]
#         except KeyError:
#             return None

    
#     def __contains__(self, item):
#         return item in self.children

#     def increment(self):
#         """Increment the count associated with this node's item."""
#         if self.sup is None:
#             raise ValueError("Root nodes have no associated count.")
#         self.sup += 1

#     def leaf(self):
#         """True if this node is a leaf in the tree; false if otherwise."""
#         return len(self.children) == 0
    

# # def TreeConstruction(transactions):
# #     for transaction in transactions:
# #         point = 1
# #         for item in transaction:
# #             next_point = 

# #     return





# transactions=[[1,2,3],[1,4,6],[1,2,4],[2,5,6]]

# master = FPMEtree()
# for transaction in transactions:
#     master.add(transaction)

# # for pre, _, node in RenderTree(master.root):
# #     treestr = u"%s%s " % (pre, node.name,)
# #     # print(treestr.ljust(8), node.MIS, node.sup)
# #     print(treestr.ljust(8))

# def DFSTraversal(visited,graph,node):
#     if node not in visited:
#         print(node.name)
#         visited.append(node)
#         for neighbor in graph[node]:
#             DFSTraversal(visited, graph, neighbor)







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