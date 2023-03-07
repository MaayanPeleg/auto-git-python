import schedule, os, time, re
from datetime import datetime
from git import Repo
import mysql.connector as mysql

pathtorepo = "C:\\Users\\maaya\\OneDrive\\Wiley-Edge-Training\\GitTest"

pathtorepo = os.path.abspath(pathtorepo)

#This is the information to connect to the DB
config = {
    'user': 'root',
    'password': 'abc123',
    'host': 'localhost',
    'database': 'Gitcheck'
}

class Commit():
    def __init__(self, files) -> None:
        self.files = files
    
    def add_files(self):
        insertFiles = [(file,file) for file in self.files]
        with mysql.connect(**config) as conn:
            cursor = conn.cursor()
            cursor.executemany('''
                INSERT INTO Files(Name)
                SELECT * FROM(SELECT %s) AS tmp
                WHERE NOT EXISTS(
                    SELECT Name FROM Files WHERE Name = %s
                ) LIMIT 1
            ''',insertFiles)
            conn.commit()
    
    def add_commit(self, hash):
        with mysql.connect(**config) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Commits(CommitHash, Date)
                VALUES(%s, %s)
            ''',(hash, datetime.now().strftime("%y-%m-%d")))
            cursor.close()

            recToInsert = [(hash, file) for file in self.files]

            cursor = conn.cursor()
            cursor.executemany('''INSERT INTO CommitFiles(CommitHash, FileID)
                SELECT %s as CommitHash, FileID AS FileID
                FROM Files
                WHERE Name = %s
                ''', recToInsert)
            
            conn.commit()

def untracked_files(repo):
    out = list()
    proc = repo.git.status(porcelain=True, untracked_files=True, as_process=True)
    for i, line in enumerate(proc.stdout):
        if i == 0:
            line = line.decode()
            filename = line.rstrip("\n")
            if re.search(r'^ M ', filename):
                out.append(filename.replace(' M ', ''))
        else:
            line = line.decode()
            filename = line.rstrip("\n")
            out.append(filename.replace('?? ', '').replace(' M ', ''))
    
    return out

with Repo(pathtorepo) as repo:
    assert not repo.bare

def job():
    files = []
    with Repo(pathtorepo) as repo:
        if repo.is_dirty():
            with open(f'cmd-{datetime.now().strftime("%d%m%y")}.log', 'a') as log:
                filesToCom = untracked_files(repo)
                for file in filesToCom:
                    files.append(file)
                    repo.git.add(f'{pathtorepo}\\{file}')

                commit = Commit(files)
                commit.add_files()

                repo.git.commit('-m', 'Auto Update Python', author="Python <Python@Python.com>")
                commit.add_commit(repo.head.object.hexsha)
                log.write(f'Ran Command Job At {datetime.now().strftime("%H-%M-%S")}\n')

        
schedule.every(0.1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

