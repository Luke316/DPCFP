from time import time
from dataset_processing import TruncateDatabase, ReadDataset, DifferentItemsCount
from preprocess_phase import MISTable, SortTransactions
from DPCFPgrowth import MIStree, MISTreeNode, Update, CFPGrowth, cfpgrowth
import csv
import numpy as np
import sys
from anytree import NodeMixin, RenderTree
from collections import Counter
import pdb

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

    non_private = {}
    NP_dataset='..\\reports\\ground_truth\\' + dataset + '_apriori_without_phi.csv'
    with open(NP_dataset, "r") as f:
        result = csv.reader(f)
        for lines in result:
            non_private[lines[0]] = float(lines[1])
 
    epsilons =   ['Epsilon   ']
    Threshold =  ['Threshold ']
    K =          ['K         ']
    precisions = ['Precision ']
    recalls =    ['Recall    ']
    f_scores =   ['F Score   ']
    RE =         ['RE        ']


    with open ('..\\reports\\'+dataset+'privacy_vs_utility.txt', 'w', newline='') as f:
        writer = csv.writer(f)
        f.write(dataset)
        f.write('\n')

        '''
        ep_1: for truncate
        ep_2: for collecting support and MIS
        ep_3: for MIS tree node
        '''
        for ep_1 in range(5,6):#5-8
            for ep_2 in range(6,11,4):#2,11,4
                for ep_3 in range(6,19,4):#2,19,4
                    for threshold in range(10,11):#10,31,5 # BMS2 threshold cannot surpass 0.02
                        for k in range(100,151,50):#50,201,50
                        #sum_precision, sum_recall, sum_F_score = metrics(dataset,0,0,0,times,non_private)
                            time_start = time()
                            sum_precision, sum_recall, sum_F_score, sum_RE = metrics(dataset,ep_1 /100,ep_2 /10,ep_3 /10,times,non_private,k,threshold/1000)
                            # epsilons.append('({:.2f}/{:.1f}/{:.1f})'.format(ep_1 /100,ep_2 /10,ep_3 /10))
                            # precisions.append('{:.12f}'.format(sum_precision/times))
                            # recalls.append('{:.12f}'.format(sum_recall/times))
                            # f_scores.append('{:.12f}'.format(sum_F_score/times))
                            # RE.append('{:.12f}'.format(sum_RE/times))
                            # Threshold.append('{:.12f}'.format(threshold/1000))
                            print('Running time: {:.4f} seconds.'.format(time() - time_start))

                            writer.writerow(['K         ',k])
                            writer.writerow(['Epsilons  ','({:.2f}/{:.1f}/{:.1f})'.format(ep_1 /100,ep_2 /10,ep_3 /10)])
                            writer.writerow(['Threshold ','{:.12f}'.format(threshold/1000)])
                            writer.writerow(['Precision ','{:.12f}'.format(sum_precision/times)])
                            writer.writerow(['Recall    ','{:.12f}'.format(sum_recall/times)])
                            writer.writerow(['F-score   ','{:.12f}'.format(sum_F_score/times)])
                            writer.writerow(['RE        ','{:.12f}'.format(sum_RE/times)])
                        

def metrics(dataset,ep_1,ep_2,ep_3,times,non_private,k,threshold):
    sum_precision = 0
    sum_recall = 0
    sum_F_score = 0
    sum_RE = 0
    # print(ep_1,ep_2,ep_3)
    topk_non_private = Counter(non_private)


    for i in range(times):
        private_topk = []
        T, n = ReadDataset(dataset)
        truncatedT, items, truncated_length = TruncateDatabase(T,ep_1,n)
        sorted_MIS_table, support, LMS = MISTable(truncatedT,items,n,ep_2,truncated_length,threshold,0.25)
        final_sorted_transactions = SortTransactions(truncatedT,sorted_MIS_table)

        # ep_1,ep_2,ep_3 = 0,0,0
        # number_of_diff_items, items = DifferentItemsCount(T)
        # truncated_length = 100
        # print('truncated length =',truncated_length)
        # sorted_MIS_table, support, LMS = MISTable(T,items,n,ep_2,truncated_length,0.01,0.25)
        # final_sorted_transactions = SortTransactions(T,sorted_MIS_table)
    
    
        master = MIStree()
        for transaction in final_sorted_transactions:
            master.AddTransaction(transaction,n,ep_3,truncated_length)
        Update(master.root)
        frequent_itemsets={}
        CFPGrowth(master, [], n,sorted_MIS_table,support,frequent_itemsets,LMS)
        # with open('mining_result.csv', 'w') as f:
        #     for key in frequent_itemsets.keys():
        #         f.write("%s,%s\n"%(key,frequent_itemsets[key]))
        
        topk_private = Counter(frequent_itemsets)

        private_topk = {}
        for key,value in topk_private.most_common(k):
            private_topk[key] = value
        
        non_private_topk = {}
        for key,value in topk_non_private.most_common(len(private_topk)):
            non_private_topk[key] = value
        
        a = set(private_topk).intersection(non_private_topk)
        precision = len(a)/len(private_topk)
        recall = len(a)/len(non_private_topk)
        F_score = 2*(precision*recall)/(precision+recall)
        print('Dataset = ',dataset)
        print('Precision = ', precision)
        print('Recall =', recall)
        print('F-Score =', F_score)
        sum_precision +=precision
        sum_recall += recall
        sum_F_score += F_score


        if (len(private_topk)%2) == 0:
            keys = list(private_topk)
            # print(len(private_topk))
            # print(len(keys))
            # print(len(private_topk)//2 + 1)
            # print(ep_1,ep_2,ep_3,k,threshold)
            itemsetA = keys[len(private_topk)//2 ]
            itemsetB = keys[len(private_topk)//2 + 1]
            if itemsetA in non_private:
                if itemsetB in non_private:
                    RE = (abs(private_topk[itemsetA]-non_private[itemsetA])/non_private[itemsetA] + abs(private_topk[itemsetB]-non_private[itemsetB])/non_private[itemsetB])/2
                    #print(private_topk[itemsetA],non_private[itemsetA],private_topk[itemsetB],non_private[itemsetB])
                else:
                    RE = (abs(private_topk[itemsetA]-non_private[itemsetA])/non_private[itemsetA]+1)/2
            else:
                if itemsetB in non_private:
                    RE = (1 + abs(private_topk[itemsetB]-non_private[itemsetB])/non_private[itemsetB])/2
                    #print(private_topk[itemsetA],non_private[itemsetA],private_topk[itemsetB],non_private[itemsetB])
                else:
                    RE = 1
            
        else: 
            keys = list(private_topk)
            itemset = keys[len(private_topk)//2+1]
            if itemset in non_private:
                RE = abs(private_topk[itemset]-non_private[itemset])/non_private[itemset]
            else :
                RE = 1

        print('RE =', RE)
        sum_RE += RE


    #print('Avg. Precision = ', avg_precision/times)
    #print('Avg. Recall =', avg_recall/times)
    #print('Avg. F-Score =', avg_F_score/times)
    return sum_precision, sum_recall, sum_F_score, sum_RE

if __name__ == '__main__':
    #time_start = time()
    #print('Dataset = ' ,sys.argv[1])
    #compare (sys.argv[1],5)
    #T10I4D100K retail kosarak BMS1 BMS2 accidents BMS-POS 
    # accidents is too big
    # compare('BMS2',10) 
    # compare('BMS1',10)
    # compare('retail',2)
    compare('T10I4D100K',3)
    compare('kosarak',3)
    compare('BMS-POS',3)

    #NP_dataset='..\\reports\\ground_truth\\' + sys.argv[1] + '_apriori.csv'
    #P_datasaet = 'output.csv'
    #compare2(NP_dataset,P_datasaet)
    #print('Running time: {:.4f} seconds.'.format(time() - time_start))
