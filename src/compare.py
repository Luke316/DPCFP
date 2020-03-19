from time import time
from dataset_processing import TruncateDatabase, ReadDataset
from preprocess_phase import MISTable, SortTransactions
import csv
import numpy as np
import copy 
import sys
from anytree import NodeMixin, RenderTree

def compare(NP,P):
    
    non_private = []
    private = []
    with open(NP, "r") as f:
        result = csv.reader(f)
        for lines in result:
            #print(lines[0])
            non_private.append(lines[0])
    
    with open(P, "r") as f:
        private_result = csv.reader(f)
        for lines in private_result:
            #print(lines[0])
            private.append(lines[0])
    
    a = set(private).intersection(non_private)

    print(a,len(a))
    precision = len(a)/len(set(private))
    recall = len(a)/len(set(non_private))
    print('Precision = ', precision)
    print('Recall =', recall)
    print('F-Score =', 2*(precision*recall)/(precision+recall))


if __name__ == '__main__':
    time_start = time()
    NP='apriori.csv'
    P='output.csv'
    compare(NP,P)
    print('Running time: {:.4f} seconds.'.format(time() - time_start))
