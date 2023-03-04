import schedule
import time
from datetime import datetime


def job():
    with open(f'cmd-{datetime.now().strftime("%d%m%y")}.log', 'a') as log:
        log.write(f'Ran Command Job At {datetime.now().strftime("%H%M%S")}\n')

schedule.every(0.1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
