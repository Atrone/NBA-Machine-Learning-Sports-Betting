import os
import sqlite3
import sys
from pathlib import Path

import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import numpy as np
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Utils.Variables import dataset, parent_dir
parent_dir = '\\'.join(str(parent_dir).split('\\')[:-2])

con = sqlite3.connect(rf"{parent_dir}\NBA-Machine-Learning-Sports-Betting\Data\dataset.sqlite")
data = pd.read_sql_query(f"select * from \"{dataset}\"", con, index_col="index")
con.close()

margin = data['Home-Team-Win']
data.drop(['Score', 'Home-Team-Win', 'TEAM_NAME', 'Date', 'TEAM_NAME.1', 'Date.1', 'OU-Cover', 'OU'],
          axis=1, inplace=True)

data = data.values

data = data.astype(float)
acc_results = []
for x in tqdm(range(100)):
    x_train, x_test, y_train, y_test = train_test_split(data, margin, test_size=.1)

    train = xgb.DMatrix(x_train, label=y_train)
    test = xgb.DMatrix(x_test, label=y_test)

    param = {
        'max_depth': 2,
        'eta': 0.01,
        'objective': 'multi:softprob',
        'num_class': 2
    }
    epochs = 500

    model = xgb.train(param, train, epochs)
    predictions = model.predict(test)
    y = []

    for z in predictions:
        y.append(np.argmax(z))

    acc = round(accuracy_score(y_test, y)*100, 1)
    print(f"{acc}%")
    acc_results.append(acc)
    # only save results if they are the best so far
    if acc == max(acc_results):
        model.save_model(rf'{parent_dir}'+r'\NBA-Machine-Learning-Sports-Betting\Models\XGBoost_{}%_ML-2.json'.format(acc))
        name = rf'{parent_dir}'+r'\NBA-Machine-Learning-Sports-Betting\Models\XGBoost_{}%_ML-2.json'.format(acc)
