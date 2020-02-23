from collections import OrderedDict
from copy import deepcopy
from fractions import Fraction
import math
import numpy as np
from random import sample
from time import time
import csv
from pprint import pprint


def init_T(T_name):
    """Read the dataset and unify the format of T"""
    time_start = time()
    T =[]

    if (T_name == 'accidents') or (T_name == 'connect') or (T_name == 'kosarak') or (T_name == 'retail') or \
            (T_name == 'mushroom') or (T_name == 'chess'):
        with open('..\\dataset\\real_world\\{:s}\\{:s}.dat'.format(T_name, T_name), 'r') as raw:
            for transaction in raw.readlines():
                transaction = transaction.strip('\n')
                transaction = transaction.split(' ')
                if T_name != 'kosarak':
                    transaction.pop()
                if T_name != 'retail':
                    transaction = [int(item) for item in transaction]
                elif T_name == 'retail':
                    transaction = [int(item) + 1 for item in transaction]
                T.append(transaction)

    elif T_name == 'T10I4D100K':
        with open('..\\dataset\\simulation\\{:s}.dat'.format(T_name), 'r') as raw:
            for transaction in raw.readlines():
                transaction = transaction.strip('\n')
                transaction = transaction.split(' ')
                transaction.pop()
                transaction = [int(item) for item in transaction]
                T.append(transaction)

    elif T_name == 'ml-latest-small':
        T_dict = OrderedDict()
        movies = []
        # Filter movies with certain genre:
        # (Action, Adventure, Animation, Children, Comedy, Crime, Documentary, Drama, Fantasy, Film-Noir, Horror,
        # Musical, Mystery, Romance, Sci-Fi, Thriller, War, Western)
        with open('..\\dataset\\real_world\\{:s}\\movies.csv'.format(T_name), 'r', encoding='UTF-8') as raw:
            dr = csv.reader(raw)
            for row in dr:
                if row == ['movieId', 'title', 'genres']:
                    continue
                movie, genre = int(row[0]), row[2]
                if ('Action' in genre) or ('Romance' in genre):
                    movies.append(movie)
        with open('..\\dataset\\real_world\\{:s}\\ratings.csv'.format(T_name), 'r', encoding='UTF-8') as raw:
            dr = csv.reader(raw)
            for row in dr:
                if row == ['userId', 'movieId', 'rating', 'timestamp']:
                    continue
                user, movie, rating = row[0], int(row[1]), float(row[2])
                T_dict[user] = T_dict.get(user, [])
                if rating >= 5.0 and movie in movies:
                    T_dict[user].append(movie)
        T = list(T_dict.values())

    elif T_name == 'ml-1m' or T_name == 'ml-10M100K':
        T_dict = OrderedDict()
        movies = []
        # Filter movies with certain genre:
        # (Action, Adventure, Animation, Children, Comedy, Crime, Documentary, Drama, Fantasy, Film-Noir, Horror,
        # Musical, Mystery, Romance, Sci-Fi, Thriller, War, Western)
        with open('..\\dataset\\real_world\\{:s}\\movies.dat'.format(T_name), 'r', encoding = 'ISO-8859-1') as raw:
            for row in raw.readlines():
                row = row.split('::')
                movie, genre = int(row[0]), row[2]
                if ('Action' in genre):
                    movies.append(movie)
        with open('..\\dataset\\real_world\\{:s}\\ratings.dat'.format(T_name), 'r') as raw:
            for row in raw.readlines():
                row = row.split('::')
                user, movie, rating = row[0], int(row[1]), float(row[2])
                T_dict[user] = T_dict.get(user, [])
                if rating >= 5.0 and movie in movies:
                    T_dict[user].append(movie)
        T = list(T_dict.values())

    elif T_name == 'foodmart' or T_name == 'chainstore' or T_name == 'BMS1' or T_name == 'BMS2':
        with open('..\\dataset\\real_world\\{:s}.txt'.format(T_name), 'r') as raw:
            for transaction in raw.readlines():
                transaction = transaction.strip('\n')
                transaction = transaction.split(' ')
                transaction = [int(item) for item in transaction]
                T.append(transaction)

    elif T_name == 'BMS-POS':
        with open('..\\dataset\\real_world\\{:s}.dat'.format(T_name), 'r') as raw:
            T_dict = OrderedDict()
            for row in raw.readlines():
                row = row.strip('\n')
                row = row.split('\t')

                if row[0] in T_dict.keys():
                    T_dict[row[0]].append(int(row[1]) + 1)
                elif row[0] not in T_dict.keys():
                    T_dict[row[0]] = [int(row[1]) + 1]

        T = list(T_dict.values())

    n = len(T)
    time_used = time() - time_start
    print('Read the {:s} dataset containing {:d} transactions. Running time: {:.3f} seconds.'.format(T_name, n, time_used))

    return T, n


def split_T(T, r=0.1):
    """
    Split T into two parts. The small part Ts is used for assign_MIS(), and the larger part Tl is used for ms_apriori().
    Let r/(1-r) denotes the split rate. Note that r may affect both the MAE and the SNR.
    """
    time_start = time()

    T_dict = OrderedDict()  # T_dict contains transactions grouped by length
    for transaction in T:
        length = len(transaction)
        if length not in T_dict.keys():
            T_dict[length] = [transaction]
        else:
            T_dict[length].append(transaction)

    Ts = []
    Tl = deepcopy(T)  # Not necessary if T is not used
    for same_length_transactions in T_dict.values():
        sampled_same_length_transactions = sample(same_length_transactions, int(r * len(same_length_transactions)))
        for transaction in sampled_same_length_transactions:
            Ts.append(transaction)
            Tl.remove(transaction)
    n_s = len(Ts)
    n_l = len(Tl)

    time_used = time() - time_start
    print('Split the dataset according to {:d}:{:d}. Running time: {:.3f} seconds.'
          .format(Fraction(str(r/(1-r))).limit_denominator(100).numerator, Fraction(str(r/(1-r))).limit_denominator(100).denominator, time_used))
    # TODO: come up with a name of this split action, which is similar to k-fold cross validation

    return Ts, Tl, n_s, n_l


def rand_truncate_T(T, theta=None, ep=1):
    """
    Randomly truncate T. Let theta denotes the length of truncation.
    If theta is none, then return an optimal theta corresponding to the truncated T, and remaining privacy budget for assigning MIS.
    If theta already exists, then only return the truncated T.
    """
    if not theta:
        I_count = OrderedDict()
        transaction_lengths = []
        for transaction in T:
            for item in transaction:
                I_count[frozenset([item])] = I_count.get(frozenset([item]), 0) + 1
            transaction_lengths.append(len(transaction))

        max_length = max(transaction_lengths)
        I = list(I_count.keys())
        m = len(I)

        ep_f = 0.05 * ep  # Privacy budget for finding theta_opt
        ep_a = ep - ep_f  # Privacy budget for assigning MIS

        average_counts = np.zeros(max_length)
        thetas = np.array([index + 1 for index in range(max_length)])
        T_thetas = OrderedDict()
        for theta in thetas:
            T_thetas[theta] = rand_truncate_T(T, theta)  # No need to pass ep.
            I_count_theta = OrderedDict()
            for transaction in T_thetas[theta]:
                for item in transaction:
                    I_count_theta[frozenset([item])] = I_count_theta.get(frozenset([item]), 0) + 1

            average_counts[theta - 1] = 1/m * sum(I_count_theta.values())  # TODO: m?

        qualities = average_counts - (thetas / ep_a)
        probs = np.exp(ep_f * qualities)
        probs = probs / probs.sum()

        theta_opt = np.random.choice(thetas, 1, False, probs)[0]
        T_theta_opt = T_thetas[theta_opt]

        return T_theta_opt, theta_opt, ep_a

    elif theta:
        T_theta = []
        for transaction in T:
            truncated_transaction = sample(transaction, min(len(transaction), theta))
            T_theta.append(truncated_transaction)

        return T_theta


def rand_truncate_T_2(T, n, ep=0.05, pr=0.85):
    I_count = OrderedDict()
    for transaction in T:
        for item in transaction:
            I_count[frozenset([item])] = I_count.get(frozenset([item]), 0) + 1
    I = list(I_count.keys())
    m = len(I)

    length_distribution = [0] * m
    for transaction in T:
        length = len(transaction)
        length_distribution[length-1] += 1  # index = length - 1

    noisy_length_distribution = []
    summation = 0
    theta = 0
    for index, count in enumerate(length_distribution):
        noisy_count = max(int(count + np.random.laplace(0, 1 / ep)), 0)  # after thresholding
        noisy_length_distribution.append(noisy_count)
        summation += noisy_count
        if summation >= int(pr * n):
            theta += index + 1  # length = index + 1
            break

    # For test
    # summation_real = 0
    # theta_real = 0
    # for index, count in enumerate(length_distribution):
    #     summation_real += count
    #     if summation_real >= int(pr * n):
    #         theta_real += index + 1
    #         break
    # print(theta_real, theta)

    T_theta = []
    for transaction in T:
        truncated_transaction = sample(transaction, min(len(transaction), theta))
        T_theta.append(truncated_transaction)

    return theta, T_theta, noisy_length_distribution


if __name__ == '__main__':
    T_name = 'ml-1m'
    T, n = init_T(T_name)

    print(n)
    print(T)
