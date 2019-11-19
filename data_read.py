#!/usr/bin/python3
# coding=utf-8

import pickle
from utils.utility import cmp_str

ATTRIBUTE_NAMES = ['age', 'workclass', 'final_weight', 'education',
             'education_num', 'marital_status', 'occupation', 'relationship',
             'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week',
             'native_country', 'class']

# 8 attributes are chose as QI attributes
# age and education levels are treated as numeric attributes
# only matrial_status and workclass has well defined generalization hierarchies.
# other categorical attributes only have 2-level generalization hierarchies.

QI_INDEX = [0, 1, 4, 5, 6, 8, 9, 13]
IS_CATEGORICAL = [False, True, False, True, True, True, True, True]
SA_INDEX = -1

def read_data():
    """
    read microda for *.txt and return read data
    """
    QI_num = len(QI_INDEX)
    data = []
    numeric_dict = []
    for i in range(QI_num):
        numeric_dict.append(dict())
    # order categorical attributes in intuitive order
    # here, we use the appear number
    data_file = open('adult.data', 'rU')
    for line in data_file:
        line = line.strip()
        # remove empty and incomplete lines
        # only 30162 records will be kept
        if len(line) == 0 or '?' in line:
            continue
        # remove double spaces
        line = line.replace(' ', '')
        temp = line.split(',')
        ltemp = []
        for i in range(QI_num):
            index = QI_INDEX[i]
            if IS_CATEGORICAL[i] is False:
                try:
                    numeric_dict[i][temp[index]] += 1
                except:
                    numeric_dict[i][temp[index]] = 1
            ltemp.append(temp[index])
        ltemp.append(temp[SA_INDEX])
        data.append(ltemp)
    # pickle numeric attributes and get NumRange
    for i in range(QI_num):
        if IS_CATEGORICAL[i] is False:
            static_file = open('adult_' + ATTRIBUTE_NAMES[QI_INDEX[i]] + '_static.pickle', 'wb')
            sort_value = list(numeric_dict[i].keys())
            sort_value.sort(cmp=cmp_str)
            pickle.dump((numeric_dict[i], sort_value), static_file)
            static_file.close()
    return data

read_data()
