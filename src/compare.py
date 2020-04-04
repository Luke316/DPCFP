from time import time
from dataset_processing import TruncateDatabase, ReadDataset
from preprocess_phase import MISTable, SortTransactions
from DPFPME import FPMEtree, FPMETreeNode, Update
import csv
import numpy as np
import copy 
import sys
from anytree import NodeMixin, RenderTree
from np_ms_apriori import assign_MIS, ms_apriori_FIM

# input 2 files and compare
def compare2(NP,P):
    
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

    #print(a,len(a))
    precision = len(a)/len(set(private))
    recall = len(a)/len(set(non_private))
    print('Precision = ', precision)
    print('Recall =', recall)
    print('F-Score =', 2*(precision*recall)/(precision+recall))
    
def compare(dataset, times):
    
    non_private = []    
    NP_dataset='..\\reports\\ground_truth\\' + dataset + '_apriori.csv'
    with open(NP_dataset, "r") as f:
        result = csv.reader(f)
        for lines in result:
            non_private.append(lines[0])
    #print(non_private)

    epsilons =   ['Epsilon   ']
    precisions = ['Precision ']
    recalls =    ['Recall    ']
    f_scores =   ['F Score   ']

    for ep_1 in range(5,6):#5-11
        for ep_2 in range(5,6):#2-6
            for ep_3 in range(15,16):#10-16
                sum_precision, sum_recall, sum_F_score = metrics(dataset,ep_1 /100,ep_2 /10,ep_3 /10,times,non_private)
                epsilons.append('({:.2f}/{:.1f}/{:.1f})'.format(ep_1 /100,ep_2 /10,ep_3 /10))
                precisions.append('{:.12f}'.format(sum_precision/times))
                recalls.append('{:.12f}'.format(sum_recall/times))
                f_scores.append('{:.12f}'.format(sum_F_score/times))
    
    with open ('..\\reports\\'+dataset+'privacy_vs_utility2.txt', 'w', newline='') as f:
        writer = csv.writer(f)
        f.write(dataset)
        f.write('\n')
        writer.writerow(epsilons)
        writer.writerow(precisions)
        writer.writerow(recalls)
        writer.writerow(f_scores)

def metrics(dataset,ep_1,ep_2,ep_3,times,non_private):
    sum_precision = 0
    sum_recall = 0
    sum_F_score = 0
    # print(ep_1,ep_2,ep_3)
    

    for i in range(times):
        private = []
        T, n = ReadDataset(dataset)
        #ep_1,ep_2,ep_3 = 0.05,1,1
        truncatedT, items, truncated_length = TruncateDatabase(T,ep_1,n)
        print(truncated_length)
        sorted_frequent_items, MIS_table = MISTable(truncatedT,items,n,ep_2,truncated_length,0.01,0.25)
        final_sorted_transactions = SortTransactions(truncatedT,sorted_frequent_items,MIS_table)

        # rho, lam, phi = 0.25, 0.01, 0.4
        # MS = assign_MIS(final_sorted_transactions, n, rho, lam)
        # F, F_sup, info = ms_apriori_FIM(final_sorted_transactions, n, MS, phi)
    
        # name = dataset + 'final_transactions_apriori.csv'
        # with open(name, 'a',newline = '') as f:
        #     writer=csv.writer(f)

        #     for itemsets in F:
        #         for itemset in itemsets:
        #             a = list(itemset)
        #             writer.writerow([a,F_sup[itemset]])

    
        master = FPMEtree()
        for transaction in final_sorted_transactions:
            master.add(transaction,MIS_table,n,ep_3,truncated_length)
        Update(master.root)
        final_output = master.root.Traverse()
        private = list(final_output.keys())
        #print(private)
        
        a = set(private).intersection(non_private)
        precision = len(a)/len(set(private))
        recall = len(a)/len(set(non_private))
        F_score = 2*(precision*recall)/(precision+recall)
        print('Precision = ', precision)
        print('Recall =', recall)
        print('F-Score =', F_score)
        sum_precision +=precision
        sum_recall += recall
        sum_F_score += F_score
        master.root.frequent_itemsets.clear()
               
    
    #print('Avg. Precision = ', avg_precision/times)
    #print('Avg. Recall =', avg_recall/times)
    #print('Avg. F-Score =', avg_F_score/times)
    return sum_precision, sum_recall, sum_F_score

if __name__ == '__main__':
    time_start = time()
    #print('Dataset = ' ,sys.argv[1])
    #compare (sys.argv[1],5)
    #T10I4D100K retail kosarak BMS1 BMS2 accidents BMS-POS

    #compare('BMS2',1)
    compare('BMS1',1)
    #compare('retail',10)
    #compare('accidents',10)
    # compare('T10I4D100K',10)
    # compare('kosarak',10)
    # compare('BMS-POS',10)

    #NP_dataset='..\\reports\\ground_truth\\' + sys.argv[1] + '_apriori.csv'
    #P_datasaet = 'output.csv'
    #compare2(NP_dataset,P_datasaet)
    print('Running time: {:.4f} seconds.'.format(time() - time_start))
