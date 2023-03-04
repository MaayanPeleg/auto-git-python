import schedule
import time
from datetime import datetime
from git import Repo

repo = Repo(".")

assert not repo.bare

def job():
    with open(f'cmd-{datetime.now().strftime("%d%m%y")}.log', 'a') as log:
        if repo.is_dirty():
            print(repo.untracked_files)
        log.write(f'Ran Command Job At {datetime.now().strftime("%H-%M-%S")}\n')

schedule.every(0.1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
