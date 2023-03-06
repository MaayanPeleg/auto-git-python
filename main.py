import schedule
import time
import re
from datetime import datetime
from git import Repo, Actor

path = "C:\\Users\\maaya\\OneDrive\\Wiley-Edge-Training\\GitTest"

author = Actor('Python', 'Python@Python.com')

def untracked_files(repo):
    out = list()
    proc = repo.git.status(porcelain=True, untracked_files=True, as_process=True)
    for line in proc.stdout:
        line = line.decode()
        filename = line.rstrip("\n")
        if re.search(r'^ M ', filename):
            out.append(filename.replace(' M ', ''))
    
    return out

with Repo(path) as repo:
    assert not repo.bare

def job():
    with Repo(path) as repo:
        if repo.is_dirty():
            with open(f'cmd-{datetime.now().strftime("%d%m%y")}.log', 'a') as log:
                filesToCom = untracked_files(repo)
                for file in filesToCom:
                    repo.git.add(f'{path}\\{file}')
                repo.git.commit('-m', 'Auto Update Python', author="Python <Python@Python.com>")
                log.write(f'Ran Command Job At {datetime.now().strftime("%H-%M-%S")}\n')

'''def job():
    repo = Repo("C:\\Users\\maaya\\OneDrive\\Wiley-Edge-Training\\GitTest")
    if repo.is_dirty():'''
        
schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

