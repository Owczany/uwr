DROP TABLE IF EXISTS SalesOrderHeaderCopy;

--CREATE TABLE SalesOrderHeaderCopy
SELECT *
INTO SalesOrderHeaderCopy
FROM [SalesLT].[SalesOrderHeader];


