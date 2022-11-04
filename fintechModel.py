# coding: utf-8
from __future__ import division
import os
import sys
import xgboost as xgb
import numpy as np
import pandas as pd


class Fintech():
    def __init__(self):
        

    def loadDvalidFromDict(self, data):
        # fPath = os.path.join(os.getcwd(),'iFlask/fintech','model/feature.pkl')
        feature_path = 'feature.pkl'
        feature = pd.read_pickle(feature_path)

        # fix feature
        feature['bc_open_to_buy'] = data['bc_open_to_buy']
        feature['total_il_high_credit_limit'] = data['total_il_high_credit_limit']
        feature['dti'] = data['dti']
        feature['annual_inc'] = data['annual_inc']
        feature['bc_util'] = data['bc_util']

        feature['int_rate'] = data['int_rate']/100
        # high wie
        if data['term'] == 36:
            feature['term_ 36 months'] = 1
            feature['term_ 60 months'] = 0
        else:
            feature['term_ 36 months'] = 0
            feature['term_ 60 months'] = 1

        feature['loan_amnt'] = data['loan_amnt']
        
        loan_rate = data['fund_rate']/100
        feature['funded_amnt'] = loan_rate * feature['loan_amnt']

        dtrain = xgb.DMatrix(feature, missing=np.NAN)

        return dtrain

