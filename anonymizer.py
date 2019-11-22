"""
run clustering_based_k_anon with given parameters
"""

# !/usr/bin/env python
# coding=utf-8

from clustering_based_k_anon import clustering_based_k_anon
from utils.read_adult_data import read_data as read_adult
from utils.read_adult_data import read_tree as read_adult_tree
import sys
import copy
import pdb
import random
import cProfile

__DEBUG = True

def extend_result(val):
    """
    separated with ',' if it is a list
    """
    if isinstance(val, list):
        return ','.join(val)
    return val


def write_to_file(result):
    """
    write the anonymized result to anonymized.data
    """
    with open("result/anonymized.data", "w") as output:
        for r in result:
            output.write(';'.join(map(extend_result, r)) + '\n')


def get_result_one(att_trees, data, type_alg, k=10):
    "run clustering_based_k_anon for one time, with k=10"
    print("K=%d" % k)
    data_back = copy.deepcopy(data)
    result, eval_result = clustering_based_k_anon(att_trees, data, type_alg, k)
    write_to_file(result)
    data = copy.deepcopy(data_back)
    print("NCP %0.2f" % eval_result[0] + "%")
    print("Running time %0.2f" % eval_result[1] + "seconds")


def get_result_n(att_trees, data, type_alg, k=10, n=10):
    """
    run clustering_based_k_anon for n time, with k=10
    """
    print("K=%d" % k)
    data_back = copy.deepcopy(data)
    n_ncp = 0.0
    n_time = 0.0
    for i in range(n):
        _, eval_result = clustering_based_k_anon(att_trees, data, type_alg, k)
        data = copy.deepcopy(data_back)
        n_ncp += eval_result[0]
        n_time += eval_result[1]
    n_ncp = n_ncp / n
    n_time = n_ncp / n
    print("Run %d times" % n)
    print("NCP %0.2f" % n_ncp + "%")
    print("Running time %0.2f" % n_time + " seconds")


def get_result_k(att_trees, data, type_alg):
    """
    change k, whle fixing QD and size of dataset
    """
    data_back = copy.deepcopy(data)
    all_ncp = []
    all_rtime = []
    # for k in range(50,100,50):
    for k in [50,100,150,200,250,300,350,400,450,500]:
        print('#' * 30)
        print("K=%d" % k)
        _, eval_result = clustering_based_k_anon(att_trees, data, type_alg, k)
        data = copy.deepcopy(data_back)
        print("NCP %0.2f" % eval_result[0] + "%")
        all_ncp.append(round(eval_result[0], 2))
        print("Running time %0.2f" % eval_result[1] + "seconds")
        all_rtime.append(round(eval_result[1], 2))
    print("All NCP", all_ncp)
    print("All Running time", all_rtime)



if __name__ == '__main__':

    print("Using Adult Dataset")

    DATA = read_adult()
    ATT_TREES = read_adult_tree()
    TYPE_ALG = 'oka'
    FLAG = ''
    try:
        FLAG = sys.argv[1]
    except IndexError:
        pass

    if FLAG == 'k':
        get_result_k(ATT_TREES, DATA, TYPE_ALG)
    elif FLAG == 'n':
        get_result_n(ATT_TREES, DATA, TYPE_ALG)
    elif FLAG == '':
        if __DEBUG:
            cProfile.run('get_result_one(ATT_TREES, DATA, TYPE_ALG)')
        else:
            get_result_one(ATT_TREES, DATA, TYPE_ALG)
    else:
        try:
            INPUT_K = int(FLAG)
            get_result_one(ATT_TREES, DATA, TYPE_ALG, INPUT_K)
        except ValueError:
            print("Usage: python anonymizer [k | n] number of iterations")
            print("k: varying k")
            print("example: python anonymizer.py 200")
            print("example: python anonymizer.py n 10")
    # anonymized dataset is stored in result
    print('Anonymized data is stored at result/anonymized.data.')
    print("Finish Cluster based K-Anon!!")
