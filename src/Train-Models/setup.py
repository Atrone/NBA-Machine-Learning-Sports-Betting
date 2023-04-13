import Train_Model
current_time = Train_Model.current_time
with open(rf'C:\Users\antho\PycharmProjects\nba_fantasy_trone\NBA-Machine-Learning-Sports-Betting\models.txt', 'a') as the_file:
    the_file.write(f'{current_time}\n')

import XGBoost_Model_ML
name = XGBoost_Model_ML.name
with open(rf'C:\Users\antho\PycharmProjects\nba_fantasy_trone\NBA-Machine-Learning-Sports-Betting\models.txt', 'a') as the_file:
    the_file.write(f'{name}\n')


import Train_Model_UO
current_time_uo = Train_Model_UO.current_time
with open(rf'C:\Users\antho\PycharmProjects\nba_fantasy_trone\NBA-Machine-Learning-Sports-Betting\models.txt', 'a') as the_file:
    the_file.write(f'{current_time_uo}\n')


import XGBoost_Model_UO
name_uo = XGBoost_Model_UO.name
with open(rf'C:\Users\antho\PycharmProjects\nba_fantasy_trone\NBA-Machine-Learning-Sports-Betting\models.txt', 'a') as the_file:
    the_file.write(f'{name_uo}\n')
