-- DROP VIEW CustomerDicount
GO

CREATE VIEW CustomerDiscount AS 
    SELECT SOH.CustomerID, SUM(SOD.UnitPriceDiscount * SOD.OrderQty) AS [TotalDiscount]
    FROM SalesLT.SalesOrderDetail AS SOD
    INNER JOIN SalesLT.SalesOrderHeader AS SOH ON SOD.SalesOrderID = SOh.SalesOrderID
    GROUP BY SOH.CustomerID
GO

SELECT MAX(TotalDiscount) FROM CustomerDiscount

-- SELECT CD.CustomerID
SELECT C.CustomerID, C.LastName, C.FirstName, SUM(SOD.UnitPriceDiscount * SOD.OrderQty) AS TotalDiscount
FROM [SalesLT].[SalesOrderDetail] AS SOD
LEFT JOIN [SalesLT].[SalesOrderHeader] AS SOH ON SOD.SalesOrderID = SOH.SalesOrderID
INNER JOIN [SalesLT].[Customer] AS C ON C.CustomerID = SOH.CustomerID
GROUP BY C.CustomerID, C.LastName, C.FirstName
HAVING SUM(SOD.UnitPriceDiscount * SOD.OrderQty) > 0
ORDER BY SUM(SOD.UnitPriceDiscount * SOD.OrderQty) DESC
