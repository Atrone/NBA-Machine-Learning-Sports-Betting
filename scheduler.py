import time
import schedule
from run_and_email import main

schedule.every(24).hours.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
