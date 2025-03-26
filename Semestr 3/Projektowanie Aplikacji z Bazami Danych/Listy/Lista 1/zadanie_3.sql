SELECT A.City, 
       COUNT(DISTINCT C.CustomerID) AS CustomerCount,
       COUNT(DISTINCT C.SalesPerson) AS SalesPersonCount
FROM [SalesLT].[CustomerAddress] AS CA
INNER JOIN [SalesLT].[Address] AS A ON CA.AddressID = A.AddressID
INNER JOIN [SalesLT].[Customer] AS C ON CA.CustomerID = C.CustomerID
GROUP BY A.City;
