@echo off
del C:\Users\antho\PycharmProjects\nba_fantasy_trone\NBA-Machine-Learning-Sports-Betting\models.txt

python C:\Users\antho\PycharmProjects\nba_fantasy_trone\NBA-Machine-Learning-Sports-Betting\src\Process-Data\setup.py

python C:\Users\antho\PycharmProjects\nba_fantasy_trone\NBA-Machine-Learning-Sports-Betting\src\Train-Models\setup.py

python C:\Users\antho\PycharmProjects\nba_fantasy_trone\NBA-Machine-Learning-Sports-Betting\main.py -A -odds=fanduel > output.txt
