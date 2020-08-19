import csv
import numpy as np
import sys
from collections import Counter
import pdb
    
def compare(dataset,eps):
    non_private = {}
    # NP_dataset='..\\reports\\ground_truth\\' + dataset + '_apriori_without_phi.csv'
    NP_dataset='..\\reports\\ground_truth\\single_threshold\\' + dataset + '.csv'

    with open(NP_dataset, "r") as f:
        result = csv.reader(f)
        for lines in result:
            non_private[lines[0]] = float(lines[1])
    
    sum_precision,sum_recall,sum_fscore,sum_number =0,0,0,0
    for i in range(0,10):
        private = {}
        if dataset == 'BMS1':
            P_dataset='..\\..\\PrivBasis_python3\\reports\\'+dataset+'_k100_eps'+str(eps)+'_'+str(i)+'.csv'
            minsup=59602/100
        elif  dataset == 'BMS2':
            P_dataset='..\\..\\PrivBasis_python3\\reports\\'+dataset+'_k100_eps'+str(eps)+'_'+str(i)+'.csv'
            minsup=77512/100
        elif dataset == 'kosarak':
            P_dataset='..\\..\\PrivBasis_python3\\reports\\'+dataset+'_k400_eps'+str(eps)+'_'+str(i)+'.csv'
            minsup=990002/100
        elif  dataset == 'BMS-POS':
            P_dataset='..\\..\\PrivBasis_python3\\reports\\'+dataset+'_k1200_eps'+str(eps)+'_'+str(i)+'.csv'
            minsup=515597/100
        elif  dataset == 'retail':
            P_dataset='..\\..\\PrivBasis_python3\\reports\\'+dataset+'_k180_eps'+str(eps)+'_'+str(i)+'.csv' 
            minsup=88162/100
        elif  dataset == 'T10I4D100K':
            P_dataset='..\\..\\PrivBasis_python3\\reports\\'+dataset+'_k400_eps'+str(eps)+'_'+str(i)+'.csv'   
            minsup=100000/100   

        with open(P_dataset, "r") as f:
            result = csv.reader(f)
            n=len(result)
            for lines in result:
                # print(lines)
                if float(lines[1])>minsup:
                    private[lines[0]] = float(lines[1])

        a = set(private).intersection(non_private)
        # print(a)
        precision = len(a)/len(n)
        recall = len(a)/len(non_private)
        if (precision+recall) != 0:
            F_score = 2*(precision*recall)/(precision+recall)
        else:
            F_score = 0

        sum_precision += precision
        sum_recall += recall
        sum_fscore += F_score
        sum_number += len(n)


    print('Dataset ===== ',dataset)
    print('Precision = ', sum_precision/10)
    print('Recall =', sum_recall/10)
    print('F-Score =', sum_fscore/10)

    # with open ('..\\..\\PrivBasis_python3\\reports\\' +dataset+'_eps_' + str(eps)+'.txt',  'w', newline='') as f:
    with open ('..\\..\\PrivBasis_python3\\reports\\single_threshold\\' +dataset+'_eps_' + str(eps)+'.txt',  'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['K         ','k'])
        writer.writerow(['Epsilons  ','{:.14f}'.format(eps)])
        writer.writerow(['Threshold ','threshold'])
        writer.writerow(['Number of ','{:.14f}'.format(sum_number/10)])
        writer.writerow(['Precision ','{:.14f}'.format(sum_precision/10)])
        writer.writerow(['Recall    ','{:.14f}'.format(sum_recall/10)])
        writer.writerow(['F-score   ','{:.14f}'.format(sum_fscore/10)])


if __name__ == '__main__':
    eps_list=[0.1,0.55,1.0,1.45,1.9,2.35]
    for eps in eps_list:
        compare('kosarak',eps)
        compare('BMS1',eps)
        compare('BMS2',eps)
        compare('retail',eps)
        compare('BMS-POS',eps)
        compare('T10I4D100K',eps)