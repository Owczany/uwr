-- Nie rozumiem do końca
-- Teraz zwracam nazwę kategorii i nazwę produktu
SELECT PC.ParentProductCategoryName, P.Name FROM SalesLT.Product AS P
INNER JOIN SalesLT.vGetAllCategories AS PC ON P.ProductCategoryID = PC.ProductCategoryID

SELECT * FROM SalesLT.vGetAllCategories
