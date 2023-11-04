import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from Utils.Variables import parent_dir
parent_dir = '\\'.join(str(parent_dir).split('\\')[:-2])
print(parent_dir)

import Train_Model
current_time = Train_Model.current_time
with open(rf'{parent_dir}\NBA-Machine-Learning-Sports-Betting\models.txt', 'a') as the_file:
    the_file.write(f'{current_time}\n')

import XGBoost_Model_ML
name = XGBoost_Model_ML.name
with open(rf'{parent_dir}\NBA-Machine-Learning-Sports-Betting\models.txt', 'a') as the_file:
    the_file.write(f'{name}\n')


import Train_Model_UO
current_time_uo = Train_Model_UO.current_time
with open(rf'{parent_dir}\NBA-Machine-Learning-Sports-Betting\models.txt', 'a') as the_file:
    the_file.write(f'{current_time_uo}\n')


import XGBoost_Model_UO
name_uo = XGBoost_Model_UO.name
with open(rf'{parent_dir}\NBA-Machine-Learning-Sports-Betting\models.txt', 'a') as the_file:
    the_file.write(f'{name_uo}\n')
