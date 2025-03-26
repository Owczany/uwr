SELECT DISTINCT City FROM [SalesLT].[Address]
INNER JOIN [SalesLT].[SalesOrderHeader] 
ON [SalesLT].[Address].AddressID = [SalesLT].[SalesOrderHeader].ShipToAddressID
