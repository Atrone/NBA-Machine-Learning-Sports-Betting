import os
main_dir = ("\\".join(os.getcwd().split("\\")[:-2]))
print(f"Main directory is: {main_dir}")

import Train_Model
current_time = Train_Model.current_time
with open(rf'{main_dir}\models.txt', 'a') as the_file:
    the_file.write(f'{current_time}\n')

import XGBoost_Model_ML
name = XGBoost_Model_ML.name
with open(rf'{main_dir}\models.txt', 'a') as the_file:
    the_file.write(f'{name}\n')


import Train_Model_UO
current_time_uo = Train_Model_UO.current_time
with open(rf'{main_dir}\models.txt', 'a') as the_file:
    the_file.write(f'{current_time_uo}\n')


import XGBoost_Model_UO
name_uo = XGBoost_Model_UO.name
with open(rf'{main_dir}\models.txt', 'a') as the_file:
    the_file.write(f'{name_uo}\n')
