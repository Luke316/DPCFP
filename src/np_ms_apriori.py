from collections import OrderedDict
from itertools import combinations
from dataset_processing import ReadDataset
from pprint import pprint
import sys
from time import time
import csv


def assign_MIS(T, n, rho=0.25, lam=0.01):
    """Assign MIS according to T"""
    time_start = time()
    I_count = OrderedDict()
    for transaction in T:
        for item in transaction:
            I_count[frozenset([item])] = I_count.get(frozenset([item]), 0) + 1

    MS = OrderedDict()
    for itemset in I_count.keys():  # E.g. itemset = frozenset({1}) rather than item = 1
        support = I_count[itemset] / n
        MS[itemset] = max(rho * support, lam)
    time_used = time() - time_start
    print('MS-Apriori: Assigned MIS. Running time: {:.3f} seconds.'.format(time_used))

    return MS


def first_scan_dataset(T, n, M, MS):
    """Scan T to get support of M, which is used to generate C1 and mine F1."""
    M_count = OrderedDict()
    M_sup = OrderedDict()
    for transaction in T:
        for item in transaction:
            M_count[frozenset([item])] = M_count.get(frozenset([item]), 0) + 1
    for itemset in M_count.keys():  # E.g. itemset = frozenset({1}) rather than item = 1
        M_sup[itemset] = M_count[itemset] / n

    C1 = []
    C1_sup = OrderedDict()
    C1_MS = OrderedDict()
    lowest_MIS = None
    for itemset in M:
        if lowest_MIS:
            if itemset in M_sup.keys() and M_sup[itemset] >= lowest_MIS:
                C1.append(itemset)
                C1_sup[itemset] = M_sup[itemset]
                C1_MS[itemset] = MS[itemset]
        else:
            if itemset in M_sup.keys() and M_sup[itemset] >= MS[itemset]:
                C1.append(itemset)
                C1_sup[itemset] = M_sup[itemset]
                C1_MS[itemset] = MS[itemset]
                lowest_MIS = MS[itemset]

    F1 = []
    F1_sup = OrderedDict()
    F1_MS = OrderedDict()
    for candidate in C1:
        if M_sup[candidate] >= MS[candidate]:
            F1.append(candidate)
            F1_sup[candidate] = M_sup[candidate]
            F1_MS[candidate] = MS[candidate]

    return C1, C1_sup, C1_MS, F1, F1_sup, F1_MS


def gen_candidate2(C1, C1_sup, C1_MS, phi):
    """Generate C2 from C1."""
    C2 =[]
    for index, itemset_i in enumerate(C1):
        if C1_sup[itemset_i] >= C1_MS[itemset_i]:
            for itemset_j in C1[index+1:]:
                if C1_sup[itemset_j] >= C1_MS[itemset_i] and abs(C1_sup[itemset_j] - C1_sup[itemset_i]) <= phi:
                    itemset_new = itemset_i | itemset_j

                    C2.append(itemset_new)

    return C2


def gen_candidate(k, Fk, Fk_sup, F_MS, phi):
    """Generate Ck from Fk-1. Note that the k here is slightly abused."""
    Ck = []
    delete = False
    for index, itemset_i in enumerate(Fk):
        fi = [item for _, item in sorted(zip(F_MS[itemset_i], list(itemset_i)))]
        for itemset_j in Fk[index+1:]:
            fj = [item for _, item in sorted(zip(F_MS[itemset_j], list(itemset_j)))]
            if fi[:k-2] == fj[:k-2] and abs(Fk_sup[frozenset([fj[k-2]])] - Fk_sup[frozenset([fi[k-2]])]) <= phi:
                # If the first k-2 elements are equal, set union. TODO: need to consider the print order.
                c = itemset_i | itemset_j
                for s in combinations(c, k-1):
                    if fi[0] in s or F_MS[frozenset([fi[1]])] == F_MS[frozenset([fi[0]])]:
                        if frozenset(list(s)) not in Fk:
                            delete = True
                if not delete:
                    Ck.append(c)

    return Ck


def scan_dataset(T, n, Ck, F_MS):
    """Scan T to get count of Ck and mine Fk."""
    Ck_count = OrderedDict()
    for transaction in T:
        # When k=1, for loop can be simplified, more details is in first_scan_dataset().
        for candidate in Ck:
            if candidate.issubset(transaction):
                Ck_count[candidate] = Ck_count.get(candidate, 0) + 1
                # Equivalent to:
                #   if candidate not in Ck_count: Ck_count[candidate]=1
                #   else: Ck_count[candidate] += 1

    Ck_MS = OrderedDict()
    # Due to frozenset is an unordered type, the first item in a candidate may not has the minimum MIS.
    # Ck_MS stores all MIS of items in each candidate. Ck_MIS stores the minimum MIS of each candidate.
    for candidate in Ck_count.keys():
        Ck_MS[candidate] = []
        for item in list(candidate):
            Ck_MS[candidate].append(F_MS[frozenset([item])])

    Fk = []
    Fk_sup = OrderedDict()
    Fk_MS = OrderedDict()
    for candidate in Ck_count.keys():
        # Note that some 0-support candidates in Ck will never be in Ck_count. Hence, using Ck_count.keys() rather than Ck.
        # When k=1, it is the only exception that C1==C1_count.keys(), more details is in first_scan_dataset().
        support = Ck_count[candidate]/n
        if support >= min(Ck_MS[candidate]):
            Fk.append(candidate)
            Fk_sup[candidate] = support
            Fk_MS[candidate] = Ck_MS[candidate]

    return Fk, Fk_sup, Fk_MS


def ms_apriori_FIM(T, n, MS, phi=0.4):
    """
    Step 1 of MS-Apriori algorithm.

    Notations:
    T: transactional dataset
    n:  number of transactions
    M: item universe after sorted by MIS
    MS: list of MIS
    Ck: candidate k-itemsets
    Fk: frequent k-itemsets
    rho: relativity between MIS and support, typical value = 0.25
    lam: lowest allowed MIS, typical value = 0.01
    phi: support difference constraint, typical value = 0.4

    When rho=0 and phi=1, MS-Apriori is equivalent to Apriori algorithm with minsup=lam.
    """
    print('MS-Apriori: Mining frequent itemsets with assigned MIS.')
    M = []
    for itemset, MIS in sorted(MS.items(), key=lambda x: (x[1], x[0])):  # TODO: MS.items() may not equivalent to I since different datasets are used
        M.append(itemset)

    time_start = time()
    C1, C1_sup, C1_MS, F1, F_sup, F_MS = first_scan_dataset(T, n, M, MS)
    F = [F1]
    time_used = time() - time_start
    info = [(len(F1), len(M), time_used)]
    print('MS-Apriori: Mined {:d} frequent 1-itemsets from {:d} candidates. Running time: {:.3f} seconds.'.format(info[0][0], info[0][1], info[0][2]))

    T = list(map(set, T))
    k = 2
    while F[k-2]:
        time_start = time()
        if k == 2:
            Ck = gen_candidate2(C1, C1_sup, C1_MS, phi)
        elif k > 2:
            Ck = gen_candidate(k, F[k-2], F_sup, F_MS, phi)
        Fk, Fk_sup, Fk_MS = scan_dataset(T, n, Ck, F_MS)
        F_sup.update(Fk_sup)
        F_MS.update(Fk_MS)
        F.append(Fk)
        time_used = time() - time_start
        info.append((len(Fk), len(Ck), time_used))
        print('MS-Apriori: Mined {:d} frequent {:d}-itemsets from {:d} candidates. Running time: {:.3f} seconds.'.format(info[k-1][0], k, info[k-1][1], info[k-1][2]))
        k += 1

    for index, Fk in enumerate(F):
        if index == 0:
            Fk.sort(reverse=True, key=lambda fk: F_sup[fk]/F_MS[fk])
        elif index > 0:
            Fk.sort(reverse=True, key=lambda fk: F_sup[fk]/min(F_MS[fk]))

    print('')

    return F, F_sup, info


if __name__ == '__main__':
    # T_name = 'retail'  # sys.argv[1]
    #T10I4D100K retail kosarak BMS1 BMS2 accidents BMS-POS
    T, n = ReadDataset(sys.argv[1])

    rho, lam, phi = 0.25, 0.01, 1
    MS = assign_MIS(T, n, rho, lam)
    F, F_sup, info = ms_apriori_FIM(T, n, MS, phi)
    
    #name = '..\\reports\\ground_truth\\'+ sys.argv[1] + '_apriori.csv'
    name = '..\\reports\\ground_truth\\'+ sys.argv[1] + '_apriori_without_phi.csv'

    with open(name, 'w',newline = '') as f:
        writer=csv.writer(f)

        for itemsets in F:
            for itemset in itemsets:
                a = list(itemset)
                a.sort()
                #print (a,F_sup[itemset])
                writer.writerow([a,F_sup[itemset]])

    #print(F_sup)

    #gen_ms_reports(T_name, rho, lam, phi, F, F_sup, info)
