-- DROP DATABASE IF EXISTS Gitcheck;
CREATE database Gitcheck;
use Gitcheck;

CREATE TABLE IF NOT EXISTS Commits(
	CommitHash VARCHAR(50) PRIMARY KEY,
    `Date` DATE NOT NULL,
    `Time` TIME NULL
);

CREATE TABLE IF NOT EXISTS Files(
	FileID INT PRIMARY KEY AUTO_INCREMENT,
    `Name` VARCHAR(50) NOT NULL,
    `Size` INT NULL
);

CREATE TABLE IF NOT EXISTS CommitFiles(
	CommitHash VARCHAR(50) NOT NULL,
    FileID INT NOT NULL,
    
    PRIMARY KEY pk_commitfiles (CommitHash, FileID),
    
    FOREIGN KEY fk_commitfiles_commit (CommitHash)
		REFERENCES Commits(CommitHash),
        
	FOREIGN KEY fk_commitfiles_files (FileID)
		REFERENCES Files(FileID)
);
