-- ALTER TABLE [SalesLT].[Customer]
-- ADD CreditCardNumber VARCHAR(20);

-- UPDATE [SalesLT].[SalesOrderHeader]
-- SET CreditCardApprovalCode = 'SomeRandomCode'
-- WHERE SalesOrderID IN
-- 	(SELECT TOP 3 SalesOrderID
-- 	 FROM [SalesLT].[SalesOrderHeader]
-- 	 ORDER BY SalesOrderID DESC);

-- wybrane pierwsze 3 zamowienia od konca

SELECT SalesOrderID, CreditCardApprovalCode
FROM [SalesLT].[SalesOrderHeader]
WHERE CreditCardApprovalCode LIKE '%Random%';
-- sa tylko 3 takie zamowienia


-- UPDATE [SalesLT].[Customer]
-- SET CreditCardNumber = 'X'
-- WHERE CustomerID IN
-- 	(SELECT c.CustomerID
-- 	 FROM [SalesLT].[Customer] AS c 
-- 	 JOIN [SalesLT].[SalesOrderHeader] AS soh 
-- 	 	ON (c.CustomerID = soh.CustomerID AND soh.CreditCardApprovalCode LIKE 'SomeRandomCode'));


SELECT c.CustomerID, soh.SalesOrderID, soh.CreditCardApprovalCode, c.CreditCardNumber
FROM [SalesLT].[Customer] AS c 
JOIN [SalesLT].[SalesOrderHeader] AS soh ON (c.CustomerID = soh.CustomerID);
-- tylko 3 klientow ma 'X' oraz 'SomeRandomCode'
