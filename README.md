# Slam-Dunk-Streamline 🏀
A fork of a popular NBA machine learning project that adds depth to each module.

Complete with PowerShell scheduled jobs and the results sensitivity analyzed in a front-end, this fork aims to make it very easy to bet intelligently.

# See here: https://nba-predict-frontend.herokuapp.com

4 commands to get started:

BASH: ```grep -rl C:\Users\antho\PycharmProjects\nba_fantasy_trone\NBA-Machine-Learning-Sports-Betting ./ | xargs sed -i 's/C:\Users\antho\PycharmProjects\nba_fantasy_trone\NBA-Machine-Learning-Sports-Betting/YOUR_PARENT_DIRECTORY/g'```

BASH: ```grep -rl blockbits30@gmail.com ./ | xargs sed -i 's/blockbits30@gmail.com/YOUR_GMAIL/g'```

BASH: ```grep -rl SMTP_PASSWORD ./ | xargs sed -i 's/SMTP_APP_PASSWORD/YOUR_GMAIL_APP_PASSWORD/g'```

BASH: ```grep -rl draftkings ./main.py | xargs sed -i 's/draftkings/YOUR_FAVORITE_BETTING_APP/g'```


After changing things with your data, you can start a scheduled job (cron, task scheduler, etc) that simply runs ```run_and_email.py``` and everything else is handled because of absolute paths.

Or you can just run the file manually and wait for the email, that works too.
