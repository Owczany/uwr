DROP TABLE IF EXISTS dbo.CustomTable
DROP TABLE IF EXISTS dbo.CustomTable1NF
DROP TABLE IF EXISTS dbo.CustomTable2NF
DROP TABLE IF EXISTS dbo.CustomTable3NF
GO

CREATE TABLE [dbo].[CustomTable] (
    ID INT,
    Patient VARCHAR(255),
    [Patient Address] VARCHAR(255),
    [Appointment time and location] VARCHAR(255),
    Price MONEY,
    Physician VARCHAR(255),
    [Appointment cause] VARCHAR(255),
)
GO

INSERT INTO dbo.CustomTable (ID, Patient, [Patient Address], [Appointment time and location], Price, Physician, [Appointment cause])
VALUES 
(1, 'Jan Kot', '6 Dolna Street, 44-444 Bór', '2029-02-01 12:30 room 12', 300, 'Oleg Wyrwiząb', 'Dental: Denture fitting in (...)'),
(2, 'Maria Mysz', '9 Górna Street, 55-555 Las', '2030-01-04 11:45 room 7', 150, 'Ewa Ciarka', 'Dermatology: Bithmark inspection (...)')
GO

CREATE TABLE dbo.CustomTable1NF (
    ID INT,
    Patient VARCHAR(255),
    Street VARCHAR(255),
    [Postal code] VARCHAR(255),
    [Locality] VARCHAR(255),
    [Date] DATE,
    [Time] TIME,
    [Room number] INT,
    Price MONEY,
    Physician VARCHAR(255),
    [Appointment cause] VARCHAR(255),
)
GO
INSERT INTO dbo.CustomTable1NF(ID, Patient, Street, [Postal code], Locality, [Date], [Time], [Room number], Price, Physician, [Appointment cause])
VALUES 
(1, 'Jan Kot', '6 Dolna Street', '44-444', 'Bór', '2029-02-01', '12:30', 12, 300, 'Oleg Wyrwiząb', 'Dental: Denture fitting in (...)'),
(2, 'Maria Mysz','9 Górna Street',  '55-555', 'Las', '2030-01-04', '11:45', 7, 150, 'Ewa Ciarka', 'Dermatology: Bithmark inspection (...)')
GO

SELECT * FROM dbo.CustomTable
SELECT * FROM dbo.CustomTable1NF

CREATE TABLE dbo.CustomTable2NF (
    ID INT,
    Patient VARCHAR(255),
    Street VARCHAR(255),
    [Postal code] VARCHAR(255),
    [Locality] VARCHAR(255),
    [Date] DATE,
    [Time] TIME,
    [Room number] INT,
    Price MONEY,
    Physician VARCHAR(255),
    [Appointment cause] VARCHAR(255),
)
GO

-- INSERT INTO dbo.CustomTable2NF ( )
-- VALUES
-- (),
-- ()
-- GO

CREATE TABLE dbo.CustomTable3NF (
    ID int,
)
GO