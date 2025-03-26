SELECT DISTINCT SOD.SalesOrderID, SOH.CustomerID FROM SalesLT.SalesOrderDetail AS SOD
LEFT JOIN SalesLT.SalesOrderHeader AS SOH ON SOD.SalesOrderID = SOH.SalesOrderID
WHERE SOH.CustomerID IS NOT NULL