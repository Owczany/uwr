SELECT 
    definition 
FROM 
    sys.check_constraints 
WHERE 
    name = 'CK_SalesOrderHeader_ShipDate';
-- ([ShipDate]>=[OrderDate] OR [ShipDate] IS NULL)

-- Insert a row that violates the constraint
INSERT INTO SalesLT.SalesOrderHeader (OrderDate, ShipDate)
VALUES ('2024-10-10', '2024-10-05');  -- ShipDate is earlier than OrderDate
GO

-- Disable the check constraint
ALTER TABLE SalesLT.SalesOrderHeader NOCHECK CONSTRAINT CK_SalesOrderHeader_ShipDate;
GO 

-- Insert a row without the constraint being enforced
UPDATE SalesLT.SalesOrderHeader
SET OrderDate = ShipDate + 1
WHERE SalesOrderID = 71783
GO

-- Enable the constraint
ALTER TABLE SalesLT.SalesOrderHeader WITH CHECK CHECK CONSTRAINT CK_SalesOrderHeader_ShipDate;
GO

-- Włączenie constraint bez sprawdzania istniejących danych
ALTER TABLE SalesLT.SalesOrderHeader WITH NOCHECK CHECK CONSTRAINT CK_SalesOrderHeader_ShipDate;
GO

-- Query to find rows violating the constraint
SELECT * 
FROM SalesLt.SalesOrderHeader
WHERE ShipDate < OrderDate;
