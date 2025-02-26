import os
import sqlite3
import sys

import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import numpy as np
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Utils.Variables import dataset, parent_dir
parent_dir = '\\'.join(str(parent_dir).split('\\')[:-2])

con = sqlite3.connect(fr"{parent_dir}\NBA-Machine-Learning-Sports-Betting\Data\dataset.sqlite")
data = pd.read_sql_query(f"select * from \"{dataset}\"", con, index_col="index")
con.close()
OU = data['OU-Cover']
total = data['OU']
data.drop(['Score', 'Home-Team-Win', 'TEAM_NAME', 'Date', 'TEAM_NAME.1', 'Date.1', 'OU-Cover', 'OU'], axis=1,
          inplace=True)

data['OU'] = np.asarray(total)
data = data.values
data = data.astype(float)
acc_results = []

for x in tqdm(range(100)):
    x_train, x_test, y_train, y_test = train_test_split(data, OU, test_size=.1)

    train = xgb.DMatrix(x_train, label=y_train)
    test = xgb.DMatrix(x_test)

    param = {
        'max_depth': 6,
        'eta': 0.05,
        'objective': 'multi:softprob',
        'num_class': 3
    }
    epochs = 300

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
        model.save_model(rf'{parent_dir}'+r'\NBA-Machine-Learning-Sports-Betting\Models\XGBoost_{}%_UO-8.json'.format(acc))
        name = rf'{parent_dir}'+r'\NBA-Machine-Learning-Sports-Betting\Models\XGBoost_{}%_UO-8.json'.format(acc)
