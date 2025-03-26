WITH OrderTotals AS (
SELECT  SOH.SalesOrderID,
        SOH.SalesOrderNumber,
        SOH.PurchaseOrderNumber,
        SUM(SOD.LineTotal) AS TotalWithDiscount,
        SUM(SOD.UnitPrice * SOD.OrderQty) AS TotalWithoutDiscount,
        SUM(SOD.OrderQty) As NumberOfProducts
FROM SalesLT.SalesOrderHeader AS SOH
INNER JOIN SalesLT.SalesOrderDetail AS SOD ON SOH.SalesOrderID = SOD.SalesOrderID
GROUP BY SOH.SalesOrderID, SOH.SalesOrderNumber, SOH.PurchaseOrderNumber
)


SELECT SalesOrderID, SalesOrderNumber, PurchaseOrderNumber, TotalWithDiscount, TotalWithoutDiscount, NumberOfProducts
FROM OrderTotals
WHERE (TotalWithoutDiscount - TotalWithDiscount) = (SELECT MAX(TotalWithoutDiscount - TotalWithDiscount) FROM OrderTotals);
