DROP TABLE IF EXISTS Test
GO

CREATE TABLE Test (
    ID INT IDENTITY(1000, 10) PRIMARY KEY,
    ColumnName VARCHAR(100)
)
GO

INSERT INTO Test (ColumnName)
VALUES 
('First Sample Data'),
('Second Sample Data'),
('Third Sample Data');

-- Select All
INSERT INTO Test (ColumnName)
VALUES ('Next Sample Data');

EXEC sp_rename 'dbo.Test.ColumnName', 'Data', 'COLUMN';
GO

SELECT * FROM Test;

INSERT INTO Test (Data) VALUES ('Alicja');
SELECT @@IDENTITY AS LastIdentityValue;

SELECT IDENT_CURRENT('Test') AS CurrentIdentityValue;
