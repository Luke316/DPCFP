from collections import OrderedDict
from random import sample
import numpy as np
from dataset_processing import DifferentItemsCount, TruncateDatabase

#from dataset_processing import init_T

# Assign MIS not finished
# def MISAssign(D, beta, threshold, epsilon, total_items):
#     items = DifferentItemsCount(D)
#     for transaction in D:
#         for item in transaction:
#             if 



#     I_truncated_counts = OrderedDict()
#     for transaction in T_theta:
#         for item in transaction:
#             I_truncated_counts[frozenset([item])] = I_truncated_counts.get(frozenset([item]), 0) + 1

#     MS = OrderedDict()
#     sensitivity = theta / n
#     for itemset in I_truncated_counts.keys():  # E.g. itemset = frozenset({1}) rather than item = 1
#         truncated_support = 1/n * I_truncated_counts[itemset]
#         noisy_truncated_support = truncated_support + np.random.laplace(0, sensitivity / ep_a)
#         noisy_truncated_support = threshold(noisy_truncated_support)
#         MS[itemset] = max(rho * noisy_truncated_support, lam)
#     time_used = time() - time_start
#     print('DPARM: Assigned MIS. Running time: {:.3f} seconds.'.format(time_used))

#     return MS

def SupportCount(T, items):
    support = dict.fromkeys(items, 0) 

    for transaction in T:
        for item in transaction:
            if item in items:
                support[item]=support.get(item) + 1
    print (support)
    return support

if __name__ == '__main__': #if file wasn't imported.
    truncatedT, items = TruncateDatabase('T10I4D100K',0.05)
    SupportCount(truncatedT,items)
    print('preprocess')