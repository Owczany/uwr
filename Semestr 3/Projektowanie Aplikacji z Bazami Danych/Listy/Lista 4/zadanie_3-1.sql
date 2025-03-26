-- Restarting 
DROP TABLE IF EXISTS dbo.Ucznie
GO

-- Tworzenie tabel przykładowych
CREATE TABLE dbo.Ucznie (
    ID INT NOT NULL PRIMARY KEY IDENTITY(1, 1),
    [First Name] VARCHAR(40),
    [Last Name] VARCHAR(40),

)
GO

INSERT INTO dbo.Ucznie ([First Name], [Last Name])
VALUES ('Piotr', 'Pijanowski'), ('Robert', 'Lewandowski'), ('Lionel', 'Messi')
GO

-- Dirty Reads
BEGIN TRANSACTION
INSERT INTO dbo.Ucznie ([First Name], [Last Name])
VALUES ('Bartek', 'Owczarzak'), ('Darek', 'Smykala')

ROLLBACK
GO

-- Unreapeatable reads
BEGIN TRANSACTION
UPDATE dbo.Ucznie 
SET [First Name] = 'Debil'
WHERE [First Name] = 'Piotr'
COMMIT
GO

-- Naprawa Non-repeatable reads
UPDATE dbo.Ucznie 
SET [First Name] = 'Piotr'
WHERE [First Name] = 'Debil'
GO

-- Phantom reads
BEGIN TRANSACTION
INSERT INTO dbo.Ucznie
VALUES ('Piotr', 'Wielki')
COMMIT
GO

DELETE FROM dbo.Ucznie WHERE [Last Name] = 'Wielki'
