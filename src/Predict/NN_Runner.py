import copy

import numpy as np
import tensorflow as tf
from colorama import Fore, Style, init, deinit
from tensorflow.keras.models import load_model
from src.Utils import Expected_Value, Variables

init()
t1 = ""
t2 = ""
with open(rf'{Variables.parent_dir}\NBA-Machine-Learning-Sports-Betting\models.txt') as fp:
    for i, line in enumerate(fp):
        print(line)
        if i == 0:
            t1 = line.strip()
        if i == 2:
            t2 = line.strip()
model = load_model(rf"{Variables.parent_dir}\NBA-Machine-Learning-Sports-Betting\Models\Trained-Model-ML-{t1}")
ou_model = load_model(rf"{Variables.parent_dir}\NBA-Machine-Learning-Sports-Betting\Models\Trained-Model-OU-{t2}")


def nn_runner(data, todays_games_uo, frame_ml, games, home_team_odds, away_team_odds):
    ml_predictions_array = []

    for row in data:
        ml_predictions_array.append(model.predict(np.array([row])))

    frame_uo = copy.deepcopy(frame_ml)
    frame_uo['OU'] = np.asarray(todays_games_uo)
    data = frame_uo.values
    data = data.astype(float)
    data = tf.keras.utils.normalize(data, axis=1)

    ou_predictions_array = []

    for row in data:
        ou_predictions_array.append(ou_model.predict(np.array([row])))

    count = 0
    for game in games:
        home_team = game[0]
        away_team = game[1]
        winner = int(np.argmax(ml_predictions_array[count]))
        under_over = int(np.argmax(ou_predictions_array[count]))
        winner_confidence = ml_predictions_array[count]
        un_confidence = ou_predictions_array[count]
        if winner == 1:
            winner_confidence = round(winner_confidence[0][1] * 100, 1)
            if under_over == 0:
                un_confidence = round(ou_predictions_array[count][0][0] * 100, 1)
                print(Fore.GREEN + home_team + Style.RESET_ALL + Fore.CYAN + f" ({winner_confidence}%)" + Style.RESET_ALL + ' vs ' + Fore.RED + away_team + Style.RESET_ALL + ': ' +
                      Fore.MAGENTA + 'UNDER ' + Style.RESET_ALL + str(todays_games_uo[count]) + Style.RESET_ALL + Fore.CYAN + f" ({un_confidence}%)" + Style.RESET_ALL)
            else:
                un_confidence = round(ou_predictions_array[count][0][1] * 100, 1)
                print(Fore.GREEN + home_team + Style.RESET_ALL + Fore.CYAN + f" ({winner_confidence}%)" + Style.RESET_ALL + ' vs ' + Fore.RED + away_team + Style.RESET_ALL + ': ' +
                      Fore.BLUE + 'OVER ' + Style.RESET_ALL + str(todays_games_uo[count]) + Style.RESET_ALL + Fore.CYAN + f" ({un_confidence}%)" + Style.RESET_ALL)
        else:
            winner_confidence = round(winner_confidence[0][0] * 100, 1)
            if under_over == 0:
                un_confidence = round(ou_predictions_array[count][0][0] * 100, 1)
                print(Fore.RED + home_team + Style.RESET_ALL + ' vs ' + Fore.GREEN + away_team + Style.RESET_ALL + Fore.CYAN + f" ({winner_confidence}%)" + Style.RESET_ALL + ': ' +
                      Fore.MAGENTA + 'UNDER ' + Style.RESET_ALL + str(todays_games_uo[count]) + Style.RESET_ALL + Fore.CYAN + f" ({un_confidence}%)" + Style.RESET_ALL)
            else:
                un_confidence = round(ou_predictions_array[count][0][1] * 100, 1)
                print(Fore.RED + home_team + Style.RESET_ALL + ' vs ' + Fore.GREEN + away_team + Style.RESET_ALL + Fore.CYAN + f" ({winner_confidence}%)" + Style.RESET_ALL + ': ' +
                      Fore.BLUE + 'OVER ' + Style.RESET_ALL + str(todays_games_uo[count]) + Style.RESET_ALL + Fore.CYAN + f" ({un_confidence}%)" + Style.RESET_ALL)
        count += 1

    print("--------------------Expected Value---------------------")
    count = 0
    for game in games:
        home_team = game[0]
        away_team = game[1]
        ev_home = float(Expected_Value.expected_value(ml_predictions_array[count][0][1], int(home_team_odds[count])))
        ev_away = float(Expected_Value.expected_value(ml_predictions_array[count][0][0], int(away_team_odds[count])))
        if ev_home > 0:
            print(home_team + ' EV: ' + Fore.GREEN + str(ev_home) + Style.RESET_ALL)
        else:
            print(home_team + ' EV: ' + Fore.RED + str(ev_home) + Style.RESET_ALL)

        if ev_away > 0:
            print(away_team + ' EV: ' + Fore.GREEN + str(ev_away) + Style.RESET_ALL)
        else:
            print(away_team + ' EV: ' + Fore.RED + str(ev_away) + Style.RESET_ALL)
        count += 1

    deinit()
