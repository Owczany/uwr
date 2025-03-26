SELECT M.Name, SUM(O.OrderQty) AS IloscProduktow FROM [SalesLT].[Product] AS P
INNER JOIN [SalesLT].[ProductModel] AS M ON M.ProductModelID = P.ProductModelID
INNER JOIN [SalesLT].[SalesOrderDetail] AS O ON P.ProductID = O.ProductID
GROUP BY M.Name
HAVING SUM(O.OrderQty) > 1
ORDER BY M.Name ASC;
