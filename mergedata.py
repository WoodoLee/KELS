import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

from utils import *


# get_savs()
# preprocessing()
# get_sav_label6()

path_preprocessed = './preprocessed/preprocessed/'
path_merge = './preprocessed/merge/'
csv_files = sorted(os.listdir(path_preprocessed))
input_sig, label_sig = False, False

for file_name in csv_files:
    df_ = pd.read_csv(os.path.join(path_preprocessed, file_name))
    df_ = df_.set_index('L2SID', drop=True)
    
    if file_name.endswith('input.csv'):
        df_ = df_.drop('Unnamed', axis=1)
        if not input_sig:
            input_merge = df_
            input_sig = True
        elif input_sig:
            input_merge = pd.merge(input_merge, df_, left_index=True, right_index=True, how='inner')

    if file_name.endswith('label.csv'):
        target_label = [_ for _ in df_.columns.tolist() if _.endswith('_CS')]
        df_ = df_[target_label]
        if not label_sig:
            label_merge = df_
            label_sig = True
        elif label_sig:
            label_merge = pd.merge(label_merge, df_, left_index=True, right_index=True, how='inner')
        
        

input_merge = input_merge.sort_index(axis=1)
input_index = set(input_merge.index.tolist())
label_index = set(label_merge.index.tolist())
idx_nan = [index for index, row in label_merge.iterrows() if row.isnull().any()]
idx = list(input_index & label_index - set(idx_nan))

input_merge = pd.DataFrame(input_merge, index=idx)
input_merge = input_merge.set_index(map(int, list(input_merge.index)))
input_merge = input_merge.sort_index()

label_merge = pd.DataFrame(label_merge, index=idx)
label_merge = label_merge.set_index(map(int, list(label_merge.index)))
label_merge = label_merge.sort_index()

input_merge.to_csv(os.path.join(path_merge, 'input_merge.csv'), index_label='L2SID')
label_merge.to_csv(os.path.join(path_merge, 'label_merge.csv'), index_label='L2SID')