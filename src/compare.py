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
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
<<<<<<< HEAD
import re
=======
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf

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
# top-K    
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


    with open ('..\\reports\\'+dataset+'_privacy_vs_utility_all.txt', 'w', newline='') as f:
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
                            sum_precision, sum_recall, sum_F_score, sum_RE = metrics(dataset,ep_1 /100,ep_2 /10,ep_3 /10,times,non_private,k,threshold/1000)
                            # epsilons.append('({:.2f}/{:.1f}/{:.1f})'.format(ep_1 /100,ep_2 /10,ep_3 /10))
                            # precisions.append('{:.12f}'.format(sum_precision/times))
                            # recalls.append('{:.12f}'.format(sum_recall/times))
                            # f_scores.append('{:.12f}'.format(sum_F_score/times))
                            # RE.append('{:.12f}'.format(sum_RE/times))
                            # Threshold.append('{:.12f}'.format(threshold/1000))

                            writer.writerow(['K         ',k])
                            writer.writerow(['Epsilons  ','({:.2f}/{:.1f}/{:.1f})'.format(ep_1 /100,ep_2 /10,ep_3 /10)])
                            writer.writerow(['Threshold ','{:.12f}'.format(threshold/1000)])
                            writer.writerow(['Precision ','{:.12f}'.format(sum_precision/times)])
                            writer.writerow(['Recall    ','{:.12f}'.format(sum_recall/times)])
                            writer.writerow(['F-score   ','{:.12f}'.format(sum_F_score/times)])
                            writer.writerow(['RE        ','{:.12f}'.format(sum_RE/times)])
                        


def compare3(dataset,times,eps=1,k=0):
    non_private = {}
    NP_dataset='..\\reports\\ground_truth\\' + dataset + '_apriori_without_phi.csv'
<<<<<<< HEAD
    # NP_dataset='..\\reports\\ground_truth\\' + dataset + '_apriori.csv'
    # NP_dataset='..\\reports\\ground_truth\\single_threshold\\' + dataset + '.csv'

=======
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf
    with open(NP_dataset, "r") as f:
        result = csv.reader(f)
        for lines in result:
            non_private[lines[0]] = float(lines[1])

<<<<<<< HEAD
    ep_1  = min(0.05,eps/10)
    ep_2, ep_3 = 0.4*(eps-ep_1),0.6*(eps-ep_1)
=======
    ep_1, ep_2, ep_3 = 0.05,0.4*(eps-0.05),0.6*(eps-0.05)
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf
    threshold = 0.01

    sum_precision, sum_recall, sum_F_score, sum_number = metrics(dataset,ep_1,ep_2,ep_3,times,non_private,k,threshold)

<<<<<<< HEAD
    with open ('..\\reports\\mine_all\\0.95_new_eps1\\'+dataset+'_privacy_vs_utility_eps'+ str(eps) +'.txt', 'w', newline='') as f:
=======
    with open ('..\\reports\\mine_all\\0.95_2\\'+dataset+'_privacy_vs_utility_eps'+ str(eps) +'.txt', 'w', newline='') as f:
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf
        writer = csv.writer(f)
        writer.writerow(['K         ',k])
        writer.writerow(['Epsilons  ','({:.2f}/{:.2f}/{:.2f})'.format(ep_1,ep_2,ep_3)])
        writer.writerow(['Threshold ','{:.14f}'.format(threshold)])
        writer.writerow(['Number of ','{:.14f}'.format(sum_number/times)])
        writer.writerow(['Precision ','{:.14f}'.format(sum_precision/times)])
        writer.writerow(['Recall    ','{:.14f}'.format(sum_recall/times)])
        writer.writerow(['F-score   ','{:.14f}'.format(sum_F_score/times)])

def plot(exp,dataset,):
    mpl.rcParams['font.family'] = 'Times New Roman'
    mpl.rcParams['font.size'] = 16
    plt.figure(figsize=(8,8),dpi=100,linewidth = 2)
    
    if exp == 'beta':
        x = np.linspace(0,1,10)
        plt.subplot(2,3,1)
        plt.plot()
        plt.show()
    elif exp == 'F-score':

        x = [0.1,0.55,1.0,1.45,1.9,2.35]
        y1 = []
        y2 = []
        y3 = []
        for eps in x:
<<<<<<< HEAD
            for i, row in enumerate(open('..\\reports\\mine_all\\0.95_new_eps1\\'+dataset+'_privacy_vs_utility_eps'+ str(eps) +'.txt')):
                if i ==6:
                    row = row.strip('\n')                                 
                    y1.append(float(row.split(',')[1]))
            for i, row in enumerate(open('..\\reports\\mine_all\\0.85_0.99\\'+dataset+'_privacy_vs_utility_eps'+ str(eps) +'.txt')):
=======
            for i, row in enumerate(open('..\\reports\\mine_all\\0.85\\'+dataset+'_privacy_vs_utility_eps'+ str(eps) +'.txt')):
                if i ==6:
                    row = row.strip('\n')                                 
                    y1.append(float(row.split(',')[1]))
            for i, row in enumerate(open('..\\reports\\mine_all\\0.95\\'+dataset+'_privacy_vs_utility_eps'+ str(eps) +'.txt')):
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf
                if i ==6:
                    row = row.strip('\n')                                 
                    y3.append(float(row.split(',')[1]))
            for i, row in enumerate(open('..\\..\\PrivBasis_python3\\reports\\'+dataset+'_eps_'+ str(eps) +'.txt')):
                if i ==6:
                    row = row.strip('\n')                                 
                    y2.append(float(row.split(',')[1]))
<<<<<<< HEAD
        plt.plot(x,y1,'o-',color = 'r', label="DPCFP++ 0.95")
        plt.plot(x,y2,'2--',color = 'b', label="PrivBasis")
        # plt.plot(x,y3,'s-',color = 'r', label="0.85_0.99")
=======
        plt.plot(x,y1,'o-',color = 'k', label="DPCFP++ 0.85")
        plt.plot(x,y2,'2--',color = 'b', label="PrivBasis")
        plt.plot(x,y3,'s-',color = 'r', label="DPCFP++ 0.95")
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf

        plt.xlim(0.1,2.35)
        plt.ylim(0,1)
        plt.xticks(x,fontsize=20)
        plt.yticks(fontsize=20)
        plt.ylabel('F-score',fontsize=20, labelpad = 10)
        plt.xlabel('privacy budget',fontsize=20, labelpad = 10)
        plt.title(dataset)
        plt.legend(loc = "lower right", fontsize=20)
        plt.grid(True, ls='--')


    elif exp == 'Recall':
        x = [0.1,0.55,1.0,1.45,1.9,2.35]
        y1 = []
        y2 = []
        y3 = []
        for eps in x:
<<<<<<< HEAD
            for i, row in enumerate(open('..\\reports\\mine_all\\0.95_new_eps1\\'+dataset+'_privacy_vs_utility_eps'+ str(eps) +'.txt')):
                if i ==5:
                    row = row.strip('\n')                                 
                    y1.append(float(row.split(',')[1]))
            for i, row in enumerate(open('..\\reports\\mine_all\\0.85_0.99\\'+dataset+'_privacy_vs_utility_eps'+ str(eps) +'.txt')):
=======
            for i, row in enumerate(open('..\\reports\\mine_all\\0.85\\'+dataset+'_privacy_vs_utility_eps'+ str(eps) +'.txt')):
                if i ==5:
                    row = row.strip('\n')                                 
                    y1.append(float(row.split(',')[1]))
            for i, row in enumerate(open('..\\reports\\mine_all\\0.95\\'+dataset+'_privacy_vs_utility_eps'+ str(eps) +'.txt')):
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf
                if i ==5:
                    row = row.strip('\n')                                 
                    y3.append(float(row.split(',')[1]))
            for i, row in enumerate(open('..\\..\\PrivBasis_python3\\reports\\'+dataset+'_eps_'+ str(eps) +'.txt')):
                if i ==5:
                    row = row.strip('\n')                                 
                    y2.append(float(row.split(',')[1]))
<<<<<<< HEAD
        plt.plot(x,y1,'o-',color = 'r', label="DPCFP++ 0.95")
        plt.plot(x,y2,'2--',color = 'b', label="PrivBasis")
        # plt.plot(x,y3,'s-',color = 'r', label="0.85_0.99")
=======
        plt.plot(x,y1,'o-',color = 'k', label="DPCFP++ 0.85")
        plt.plot(x,y2,'2--',color = 'b', label="PrivBasis")
        plt.plot(x,y3,'s-',color = 'r', label="DPCFP++ 0.95")
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf

        plt.xlim(0.1,2.35)
        plt.ylim(0,1)
        plt.xticks(x,fontsize=20)
        plt.yticks(fontsize=20)
        plt.ylabel('Recall',fontsize=20, labelpad = 10)
        plt.xlabel('privacy budget',fontsize=20, labelpad = 10)
        plt.title(dataset)
        plt.legend(loc = "lower right", fontsize=20)
        plt.grid(True, ls='--')


    elif exp == 'Precision':
        x = [0.1,0.55,1.0,1.45,1.9,2.35]
        y1 = []
        y2 = []
        y3 = []
        for eps in x:
<<<<<<< HEAD
            for i, row in enumerate(open('..\\reports\\mine_all\\0.95_new_eps1\\'+dataset+'_privacy_vs_utility_eps'+ str(eps) +'.txt')):
                if i ==4:
                    row = row.strip('\n')                                 
                    y1.append(float(row.split(',')[1]))
            for i, row in enumerate(open('..\\reports\\mine_all\\0.85_0.99\\'+dataset+'_privacy_vs_utility_eps'+ str(eps) +'.txt')):
=======
            for i, row in enumerate(open('..\\reports\\mine_all\\0.85\\'+dataset+'_privacy_vs_utility_eps'+ str(eps) +'.txt')):
                if i ==4:
                    row = row.strip('\n')                                 
                    y1.append(float(row.split(',')[1]))
            for i, row in enumerate(open('..\\reports\\mine_all\\0.95\\'+dataset+'_privacy_vs_utility_eps'+ str(eps) +'.txt')):
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf
                if i ==4:
                    row = row.strip('\n')                                 
                    y3.append(float(row.split(',')[1]))
            for i, row in enumerate(open('..\\..\\PrivBasis_python3\\reports\\'+dataset+'_eps_'+ str(eps) +'.txt')):
                if i ==4:
                    row = row.strip('\n')                                 
                    y2.append(float(row.split(',')[1]))
<<<<<<< HEAD
        plt.plot(x,y1,'o-',color = 'r', label="DPCFP++ 0.95")
        plt.plot(x,y2,'2--',color = 'b', label="PrivBasis")
        # plt.plot(x,y3,'s-',color = 'r', label="0.85_0.99")
=======
        plt.plot(x,y1,'o-',color = 'k', label="DPCFP++ 0.85")
        plt.plot(x,y2,'2--',color = 'b', label="PrivBasis")
        plt.plot(x,y3,'s-',color = 'r', label="DPCFP++ 0.95")
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf

        plt.xlim(0.1,2.35)
        plt.ylim(0,1)
        plt.xticks(x,fontsize=20)
        plt.yticks(fontsize=20)
        plt.ylabel('Precision',fontsize=20, labelpad = 10)
        plt.xlabel('privacy budget',fontsize=20, labelpad = 10)
        plt.title(dataset)
        plt.legend(loc = "lower right", fontsize=20)
        plt.grid(True, ls='--')


    elif exp == 'Runtime':
        x = [0.1,0.55,1.0,1.45,1.9,2.35]
        if dataset == 'retail':
            y1=[10.707,3.193,3.172,3.123,3.063,3.028]
            y2=[3.853,4.188,4.451,4.503,4.613,4.837]
            plt.ylim(0,20)
        elif dataset == 'BMS1':
            y1=[0.906,0.831,0.844,0.835,0.863,0.834]
            y2=[3.886,3.964,3.899,3.812,3.917,4.429]
            plt.ylim(0,10)
        elif dataset == 'BMS2':
            y1=[2.010,1.393,1.378,1.406,1.426,1.388]
            y2=[3.497,3.557,3.676,3.680,3.831,3.723]
            plt.ylim(0,10)
        elif dataset == 'BMS-POS':
            y1=[57.426,36.708,35.985,36.209,35.617,35.857]
            y2=[186.885,222.435,469.197,2474.838,7129.583,16272.668]
            plt.ylim(0,18000)
        elif dataset == 'kosarak':
            y1=[32.832,32.466,32.276,32.612,32.343,32.323]
            y2=[55.691,124.489,107.668,107.376,95.644,109.498]
<<<<<<< HEAD
            plt.ylim(0,180)
=======
            plt.ylim(0,150)
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf
        elif dataset == 'T10I4D100K':
            y1=[30.619,19.691,19.458,19.273,19.085,19.237]
            y2=[37.919,38.940,39.984,39.480,38.819,39.889]
            plt.ylim(0,60)
        
        plt.plot(x,y1,'s-',color = 'r', label="DPCFP++")
        plt.plot(x,y2,'2--',color = 'b', label="PrivBasis")
        plt.xlim(0.1,2.35)

        plt.xticks(x,fontsize=20)
        plt.yticks(fontsize=20)
        plt.ylabel('Time(sec)',fontsize=20, labelpad = 10)
        plt.xlabel('privacy budget',fontsize=20, labelpad = 10)
        plt.title(dataset)
<<<<<<< HEAD
        plt.legend(loc = "upper left", fontsize=20)
        plt.grid(True, ls='--')
        # plt.show()
    
    elif exp == 'MAE':
        x = [0.1,0.55,1.0,1.45,1.9,2.35]
        y1 = []
        y2 = []
        # y3 = []
        MAE1 = 0
        MAE2 = 0
        # MRE = 0 
        non_private = {}
        NP_dataset='..\\reports\\ground_truth\\' + dataset + '_apriori_without_phi.csv'
        with open(NP_dataset, "r") as f:
            result = csv.reader(f)
            for lines in result:
                non_private[lines[0]] = float(lines[1])

        for eps in x:
            for i in range(0,10):
                dpcfp = {}
                z=0
                for  index, row in enumerate(open('..\\reports\\mine_all\\0.95_new_eps1\\'+dataset+'_privacy'+str(eps)+'_vs_utility_'+ str(i) +'.csv')):
                    *others, last =row.split(',')
                    # print(str(re.findall(r'\[(.*?)\]', row)))
                    # print(last)
                    a =str(re.findall(r'\[(.*?)\]', row)).replace("'","")
                    # print(a)
                    dpcfp[a]=float(last)
                    
                for itemset in list(non_private.keys()):
                    # print(itemset)
                    if itemset in list(dpcfp.keys()):
                        z+=1
                        MAE1 += abs(dpcfp[itemset]-non_private[itemset])
                    else:
                        MAE1 += non_private[itemset]

                if dataset == 'retail':
                    pb={}
                    with open('..\\..\\PrivBasis_python3\\reports\\retail_k180_eps'+ str(eps) + '_' +str(i)+'.csv') as F:
                        noisy_result = csv.reader(F)
                        for lines in noisy_result:
                            pb[lines[0]]=float(lines[1])/88162
                        for itemset in list(non_private.keys()):
                            if itemset in list(pb.keys()):
                                MAE2 += abs(pb[itemset]-non_private[itemset])
                            else:
                                MAE2 += non_private[itemset]
                elif dataset == 'BMS1':
                    pb={}
                    with open('..\\..\\PrivBasis_python3\\reports\\BMS1_k100_eps'+ str(eps) + '_' +str(i)+'.csv') as F:
                        noisy_result = csv.reader(F)
                        for lines in noisy_result:
                            pb[lines[0]]=float(lines[1])/59602
                        for itemset in list(non_private.keys()):
                            if itemset in list(pb.keys()):

                                MAE2 += abs(pb[itemset]-non_private[itemset])
                            else:
                                MAE2 += non_private[itemset]
                elif dataset == 'BMS2':
                    pb={}
                    with open('..\\..\\PrivBasis_python3\\reports\\BMS2_k100_eps'+ str(eps) + '_' +str(i)+'.csv') as F:
                        noisy_result = csv.reader(F)
                        for lines in noisy_result:
                            pb[lines[0]]=float(lines[1])/77512
                        for itemset in list(non_private.keys()):
                            if itemset in list(pb.keys()):
                                MAE2 += abs(pb[itemset]-non_private[itemset])
                            else:
                                MAE2 += non_private[itemset]
                elif dataset == 'BMS-POS':
                    pb={}
                    with open('..\\..\\PrivBasis_python3\\reports\\BMS-POS_k1200_eps'+ str(eps) + '_' +str(i)+'.csv') as F:
                        noisy_result = csv.reader(F)
                        for lines in noisy_result:
                            pb[lines[0]]=float(lines[1])/515597
                        for itemset in list(non_private.keys()):
                            if itemset in list(pb.keys()):
                                MAE2 += abs(pb[itemset]-non_private[itemset])
                            else:
                                MAE2 += non_private[itemset]
                elif dataset == 'T10I4D100K':
                    pb={}
                    with open('..\\..\\PrivBasis_python3\\reports\\T10I4D100K_k400_eps'+ str(eps) + '_' +str(i)+'.csv') as F:
                        noisy_result = csv.reader(F)
                        for lines in noisy_result:
                            pb[lines[0]]=float(lines[1])/100000
                        for itemset in list(non_private.keys()):
                            if itemset in list(pb.keys()):
                                MAE2 += abs(pb[itemset]-non_private[itemset])
                            else:
                                MAE2 += non_private[itemset]
                elif dataset == 'kosarak':
                    pb={}
                    with open('..\\..\\PrivBasis_python3\\reports\\kosarak_k400_eps'+ str(eps) + '_' +str(i)+'.csv') as F:
                        noisy_result = csv.reader(F)
                        for lines in noisy_result:
                            pb[lines[0]]=float(lines[1])/990002
                        for itemset in list(non_private.keys()):
                            if itemset in list(pb.keys()):
                                MAE2 += abs(pb[itemset]-non_private[itemset])
                            else:
                                MAE2 += non_private[itemset]
                # print(z)
            MAE1 = MAE1/len(non_private.keys())/10
            MAE2 = MAE2/len(non_private.keys())/10
            # MRE = MRE/len(non_private.keys())/10
            y1.append(MAE1)
            y2.append(MAE2)
            MAE1 ,MAE2 =0,0
        # print(y1)
        # print(y2)
        plt.plot(x,y1,'o-',color = 'r', label="DPCFP++ 0.95")
        plt.plot(x,y2,'2--',color = 'b', label="PrivBasis")
        # plt.plot(x,y3,'s-',color = 'r', label="0.85_0.99")

        plt.xlim(0.1,2.35)
        plt.ylim(0,0.04)
        plt.xticks(x,fontsize=20)
        plt.yticks(fontsize=20)
        plt.ylabel('MAE',fontsize=20, labelpad = 10)
        plt.xlabel('privacy budget',fontsize=20, labelpad = 10)
        plt.title(dataset)
        plt.legend(loc = "upper right", fontsize=20)
        plt.grid(True, ls='--')

    plt.savefig('..\\reports\\mine_all\\0.95_new_eps1\\figure\\'+exp+'_'+dataset+'.png',bbox_inches = "tight")
    plt.savefig('..\\reports\\mine_all\\0.95_new_eps1\\figure\\'+exp+'_'+dataset+'.eps',format = 'eps',bbox_inches = "tight")
=======
        plt.legend(loc = "lower right", fontsize=20)
        plt.grid(True, ls='--')
        # plt.show()
    
    plt.savefig('..\\reports\\mine_all\\0.95\\figure\\'+exp+'_'+dataset+'.png')
    plt.savefig('..\\reports\\mine_all\\0.95\\figure\\'+exp+'_'+dataset+'.eps',format = 'eps')
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf


        


def metrics(dataset,ep_1,ep_2,ep_3,times,non_private,k,threshold,beta=0.25):
    sum_precision = 0
    sum_recall = 0
    sum_F_score = 0
    sum_RE = 0
    sum_number= 0

    for i in range(0,times):
        private_topk = []
        T, n = ReadDataset(dataset)
<<<<<<< HEAD
        truncatedT, truncatedT2, items, truncated_length = TruncateDatabase(T,ep_1,n)
=======
        truncatedT, items, truncated_length = TruncateDatabase(T,ep_1,n)
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf
        sorted_MIS_table, support, LMS = MISTable(truncatedT,items,n,ep_2,truncated_length,threshold,beta)
        final_sorted_transactions = SortTransactions(truncatedT,sorted_MIS_table)

        # ep_1,ep_2,ep_3 = 0,0,0
        # number_of_diff_items, items = DifferentItemsCount(T)
        # truncated_length = 100
        # print('truncated length =',truncated_length)
        # sorted_MIS_table, support, LMS = MISTable(T,items,n,ep_2,truncated_length,0.01,0.25)
        # final_sorted_transactions = SortTransactions(T,sorted_MIS_table)
    
    
        master = MIStree()
        for transaction in final_sorted_transactions:
<<<<<<< HEAD
            master.AddTransaction(transaction,n,ep_3)
        Update(master.root)
        frequent_itemsets={}
        CFPGrowth(master, [], n,sorted_MIS_table,support,frequent_itemsets,LMS)
        with open('..\\reports\\mine_all\\0.95_new_eps1\\'+dataset+'_privacy'+str(ep_1+ep_2+ep_3)+'_vs_utility_'+str(i)+'.csv', 'w',) as f:
            for key in frequent_itemsets.keys():
                f.write("%s,%s\n"%(key,frequent_itemsets[key]))
        # pdb.set_trace()
=======
            master.AddTransaction(transaction,n,ep_3,truncated_length)
        Update(master.root)
        frequent_itemsets={}
        CFPGrowth(master, [], n,sorted_MIS_table,support,frequent_itemsets,LMS)
        with open('..\\reports\\mine_all\\0.95_2\\'+dataset+'_privacy_vs_utility_'+str(i)+'.csv', 'w',) as f:
            for key in frequent_itemsets.keys():
                f.write("%s,%s\n"%(key,frequent_itemsets[key]))
        
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf
        topk_private = Counter(frequent_itemsets)
        topk_non_private = Counter(non_private)

        if k == 0:
            a = set(frequent_itemsets).intersection(non_private)
            precision = len(a)/len(frequent_itemsets)
            recall = len(a)/len(non_private)
        else:
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
        print('Dataset ===== ',dataset)
        print('Precision = ', precision)
        print('Recall =', recall)
        print('F-Score =', F_score)
        sum_precision +=precision
        sum_recall += recall
        sum_F_score += F_score
        sum_number += len(frequent_itemsets)
        # if (len(private_topk)%2) == 0:
        #     keys = list(private_topk)
        #     # print(len(private_topk))
        #     # print(len(keys))
        #     # print(len(private_topk)//2 + 1)
        #     # print(ep_1,ep_2,ep_3,k,threshold)
        #     itemsetA = keys[len(private_topk)//2 ]
        #     itemsetB = keys[len(private_topk)//2 + 1]
        #     if itemsetA in non_private:
        #         if itemsetB in non_private:
        #             RE = (abs(private_topk[itemsetA]-non_private[itemsetA])/non_private[itemsetA] + abs(private_topk[itemsetB]-non_private[itemsetB])/non_private[itemsetB])/2
        #             #print(private_topk[itemsetA],non_private[itemsetA],private_topk[itemsetB],non_private[itemsetB])
        #         else:
        #             RE = (abs(private_topk[itemsetA]-non_private[itemsetA])/non_private[itemsetA]+1)/2
        #     else:
        #         if itemsetB in non_private:
        #             RE = (1 + abs(private_topk[itemsetB]-non_private[itemsetB])/non_private[itemsetB])/2
        #             #print(private_topk[itemsetA],non_private[itemsetA],private_topk[itemsetB],non_private[itemsetB])
        #         else:
        #             RE = 1
            
        # else: 
        #     keys = list(private_topk)
        #     itemset = keys[len(private_topk)//2+1]
        #     if itemset in non_private:
        #         RE = abs(private_topk[itemset]-non_private[itemset])/non_private[itemset]
        #     else :
        #         RE = 1

        # print('RE =', RE)
        # sum_RE += RE


    #print('Avg. Precision = ', avg_precision/times)
    #print('Avg. Recall =', avg_recall/times)
    #print('Avg. F-Score =', avg_F_score/times)
    return sum_precision, sum_recall, sum_F_score, sum_number #sum_RE

if __name__ == '__main__':
    #time_start = time()
    #print('Dataset = ' ,sys.argv[1])
    #compare (sys.argv[1],5)
    #T10I4D100K retail kosarak BMS1 BMS2 accidents BMS-POS 
    # accidents is too big

<<<<<<< HEAD
    # for ep in range(10,236,45):
=======
    # for ep in range(10,281,45):
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf
    #     compare3('BMS2',10,ep/100,0) 
    #     compare3('BMS1',10,ep/100,0)
    #     compare3('retail',10,ep/100,0)
    #     compare3('T10I4D100K',10,ep/100,0)
    #     compare3('kosarak',10,ep/100,0)
    #     compare3('BMS-POS',10,ep/100,0)
    
<<<<<<< HEAD
    # compare3('BMS2',1,0,0) 
    # compare3('BMS1',1,0,0) 
    # compare3('kosarak',1,0,0) 
    # compare3('BMS-POS',1,0,0)
    # compare3('retail',1,0,0)
    # compare3('T10I4D100K',1,0,0)
=======
    # compare3('BMS2',10,1,0) 
    # compare3('BMS1',10,1,0) 
    # compare3('kosarak',10,1,0) 
    # compare3('BMS-POS',10,1,0)
    # compare3('retail',10,1,0)
    # compare3('T10I4D100K',10,1,0)

>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf

    #NP_dataset='..\\reports\\ground_truth\\' + sys.argv[1] + '_apriori.csv'
    #P_datasaet = 'output.csv'
    #compare2(NP_dataset,P_datasaet)
    #print('Running time: {:.4f} seconds.'.format(time() - time_start))

    datasets = ['BMS1', 'BMS2','retail','kosarak','BMS-POS','T10I4D100K']
    for dataset in datasets:
        # plot('F-score',dataset)
        # plot('Precision',dataset)
        # plot('Recall',dataset)
        plot('Runtime',dataset)
<<<<<<< HEAD
        # plot('MAE',dataset)
    # plot('MAE','retail')
=======
>>>>>>> 70814a6519b741909892267185ca3b08daa35fbf

