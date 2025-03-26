DROP TRIGGER IF EXISTS SalesLT.trg_custoooom
GO

ALTER DATABASE [owczana-baza-danych]
SET RECURSIVE_TRIGGERS OFF;

SELECT name AS 'Database name', is_recursive_triggers_on AS 'Recursive Triggers Enabled'
FROM sys.databases
GO

CREATE TRIGGER SalesLT.trg_custoooom ON SalesLT.Customer AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON

    UPDATE SalesLT.Customer
    SET ModifiedDate = SYSDATETIME()
    FROM SalesLT.Customer AS c
    INNER JOIN Inserted AS i
    ON c.CustomerID = i.CustomerID
END
GO

UPDATE SalesLT.Customer
SET FirstName = 'Bartek'
WHERE CustomerID <= 1

SELECT * FROM SalesLT.Customer
Where CustomerID <= 3

SELECT * FROM SalesLT.Customer