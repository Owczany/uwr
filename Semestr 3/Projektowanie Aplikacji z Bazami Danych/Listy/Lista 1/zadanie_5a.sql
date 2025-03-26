CREATE VIEW OrderTotals AS 
SELECT  SOH.SalesOrderID,
        SOH.SalesOrderNumber,
        SOH.PurchaseOrderNumber,
        SUM(SOD.LineTotal) AS TotalWithDiscount,
        SUM(SOD.UnitPrice * SOD.OrderQty) AS TotalWithoutDiscount,
        SUM(SOD.OrderQty) As NumberOfProducts
FROM SalesLT.SalesOrderHeader AS SOH
INNER JOIN SalesLT.SalesOrderDetail AS SOD ON SOH.SalesOrderID = SOD.SalesOrderID
GROUP BY SOH.SalesOrderID, SOH.SalesOrderNumber, SOH.PurchaseOrderNumber
GO

-- Podpunkt A
SELECT TOP 100 * FROM OrderTotals;

-- Podpunkt b
SELECT TOP 1 * FROM OrderTotals
ORDER BY NumberOfProducts DESC;