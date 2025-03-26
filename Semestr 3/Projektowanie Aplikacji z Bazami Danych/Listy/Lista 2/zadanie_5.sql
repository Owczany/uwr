SELECT ProductID, DiscontinuedDate
FROM SalesLT.Product
WHERE DiscontinuedDate IS NOT NULL

CREATE TYPE ProductList AS TABLE (
    ProductID INT PRIMARY KEY
);
GO

DROP PROCEDURE IF EXISTS ChangeProducts;
GO

CREATE PROCEDURE ChangeProducts 
    @ProductList ProductList READONLY,
    @Date DATE
AS
BEGIN
    IF TRY_CONVERT(date, @Date, 102) IS NULL
    BEGIN
        ; THROW 52001, 'Zła data', 1;
    END

    UPDATE SalesLT.Product
    SET DiscontinuedDate = @Date
    WHERE ProductID IN (SELECT ProductID FROM @ProductList) AND DiscontinuedDate IS NULL
END
GO

DECLARE @Products ProductList
INSERT INTO @Products (ProductID)
VALUES (680), (723), (722)

EXEC ChangeProducts @Products, '2024-01-03'
Go