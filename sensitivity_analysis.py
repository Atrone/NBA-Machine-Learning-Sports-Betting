from statistics import mean


def moneyline_to_decimal(moneyline):
    if abs(moneyline) < 100:
        return moneyline
    if moneyline > 0:
        return 1 + (moneyline / 100)
    elif moneyline < 0:
        return 1 - (100 / moneyline)
    else:
        return 1  # Assuming even odds are represented as 0


# 2022-23
odds = [1.2, 4.5, 3.45, 3.7, 4.85, 2.06, 5.2, 3.05, 3.9, 1.89, 3.9, 3.95, 2.68, 3.15, 3.45, 2.88, 3.75, 2.84, 2.72,
        1.83, 3.45, 3.20, 2.52, 3.95, 2.64, 7.1, 4.85, 6.7, 1.56, 5.8, 2.08, 3.45, 3.5, 1.8, 1.625, 1.625, 1.9, 1.625,
        4.85, 3.35, 1.1, 3.7, 3.25, 1.5, 1.9, 1.76, 1.78, 1.1, 1.7, 3.5, 3.6, 2.36, 3.0, 3.3, 3.9, 1.3, 4.6, 2.94, 2.36,
        2, 3.6, 3.45, 3.9, 3.75, 3.85]

outcomes = [0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0,
            0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0]
evs = [6, 48, 34, 8, 57, 22, 20, 18, 52, 36, 27, 23, 23, 29, 81, 20, 100, 27, 41, 4, 41, 40, 11, 82, 36, 69, 49, 170,
       14, 76, 31, 42, 54, 45, 10, 4, 10, 7, 73, 16, 6, 43, 21, 21, 16, 18, 10, 31, 5, 24, 30, 30, 60, 20, 15, 4, 30,
       70, 26, 20, 12, 12, 40, 25, 30]

# 2023-24
odds = [114, 205, 154, -162, 330, 550, 220, 124, 130, 215, 330, 114, 270, 200, 145, 136, 140, 330, 260, 130, 140,
        102,
        470, 120, 225, 285, 180, 145, -135, 124, 180, 350, 150, 500, 310, 110, 260, 114, 136, 295, 470, -135,
        164, 125,
        142, 260, 225, -170, 360, 205, 235, 150, 370, 320, 310, 124, 164, 380, 205, 124, 210, 240, 124, 145, 310,
        120,
        425, 150, 142, 124, -148, 225, 285]
evs = [12, 20, 17, 19, 35, 150, 90, 27, 30, 20, 53, 24, 70, 45, 30, 27, 42, 110, 20, 36, 40, 25, 80, 50, 43, 60,
       60,
       20, 20, 20, 35, 60, 60, 70, 25, 35, 40, 30, 27, 35, 80, 20, 12, 40, 15, 15, 10, 60, 10, 35, 30, 100, 45,
       30, 30,
       30, 40, 50, 17, 35, 50, 25, 12, 40, 27, 57, 20, 35, 25, 12, 15, 45, ]
outcomes = [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0,
            1, 0, 1, 0,
            1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
            0,
            0, ]  # r1
print(f"Live test of {len(outcomes)} games.")

# new sensitivity = 35
# old sensitivity = 10

odds = [moneyline_to_decimal(ml) for ml in odds]

base_bet = 100

# Initialize variables
best_profit_to_drawdown = -1
best_ev_threshold = None

profit = 0
mdd = 0
avg_odd = []
outcomes2 = 0
games = 0
games2 = 0
# Loop through potential EV thresholds

# GOODNESS (EV)
# HIGHER EV, BETTER BET
# THE MORE YOU BET, THE MORE YOU CAN MAKE (AND LOSE)
#

for ev_threshold in range(36, 37):
    balance = 0
    balances = [0]

    # Iterate over each game
    for outcome, ev, odd in zip(outcomes, evs, odds):
        # Only bet if the expected value is above the threshold
        if ev > ev_threshold:
            games += 1
            avg_odd.append(odd)
            outcomes2 += outcome
            if outcome == 1:  # win
                balance += (base_bet * odd) - base_bet
            else:  # lose
                balance -= base_bet
            balances.append(balance)
        if ev > ev_threshold * 2:
            games2 += 1
            avg_odd.append(odd)
            outcomes2 += outcome
            if outcome == 1:  # win
                balance += (base_bet * odd) - base_bet
            else:  # lose
                balance -= base_bet
            balances.append(balance)
        if ev > ev_threshold * 2:
            games2 += 1
            avg_odd.append(odd)
            outcomes2 += outcome
            if outcome == 1:  # win
                balance += (base_bet * odd) - base_bet
            else:  # lose
                balance -= base_bet
            balances.append(balance)

    # Calculate drawdown
    max_drawdown = max([balances[i] - balances[j] for i in range(len(balances)) for j in range(i + 1, len(balances))])

    # Compute profit to drawdown ratio, if drawdown is not zero
    profit_to_drawdown = balance  # / max_drawdown if max_drawdown else 'Infinity'

    # Check if this EV threshold is the best so far
    if profit_to_drawdown != 'Infinity' and profit_to_drawdown > best_profit_to_drawdown:
        best_profit_to_drawdown = profit_to_drawdown
        best_ev_threshold = ev_threshold
        profit = balance
        mdd = max_drawdown
print(balances)
print(f" PROFIT ECULS: {profit}")
print(mean(avg_odd))
print(outcomes2)
print(games)
print(games2)
print(games + games2)
print(
    f'Assuming same bet amount every time... the best EV threshold is: {best_ev_threshold} with profit of {profit / base_bet} times unit size. The most you would lose is {mdd / base_bet - 0.5} times unit size.')


# ALL: the best EV threshold is: 31 with profit of 47.71 times unit size. The most you would lose is 15.8 times unit size.
# 2023: the best EV threshold is: 36 with profit of 9.65 times unit size. The most you would lose is 12.1 times unit size.
# 2022: the best EV threshold is: 31 with profit of 47.26 times unit size. The most you would lose is 9.61 times unit size.
