import os
from datetime import date

if date.today().month in range(8,13):
    dataset = f"dataset_2012-{str(date.today().year + 1)[-2:]}"

else:
    dataset = f"dataset_2012-{str(date.today().year)[-2:]}"

datasets = []

for i in range(2007,date.today().year+1):
    datasets.append("odds_"+f"{i}-{str(i + 1)[-2:]}")

if date.today().month in range(8,12):
    year = [date.today().year, date.today().year + 1]
    season = [f"{date.today().year}-{str(date.today().year + 1)[-2:]}"]

else:
    year = [date.today().year-1, date.today().year]
    season = [f"{date.today().year-1}-{str(date.today().year)[-2:]}"]

season_array = []
print(year)
print(season)
for i in range(2012,date.today().year+1):
    season_array.append(f"{i}-{str(i + 1)[-2:]}")
if date.today().month in range(8,12):
    pass
else:
    season_array = season_array[:-1]
print(season_array)

current_dir = os.getcwd()  # Get current directory
parent_dir = os.path.dirname(current_dir)  # Get parent directory
