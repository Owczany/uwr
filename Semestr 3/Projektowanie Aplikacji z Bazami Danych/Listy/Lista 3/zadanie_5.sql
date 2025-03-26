-- CREATE VIEW dbo.TempViewTest
-- AS
-- SELECT ProductID, StandardCost, ListPrice, P.Size
-- FROM SalesLT.Product P 
-- GO

DROP TABLE IF EXISTS SalesLT.ProductPriceHistory
DROP TRIGGER IF EXISTS trg_ProductPriceHistoryUpdate
DROP TRIGGER IF EXISTS trg_ProductPriceHistoryDelete
GO

CREATE TABLE SalesLT.ProductPriceHistory (
    ProductID INT NOT NULL,
    StandardCost MONEY NOT NULL,
    ListPrice MONEY NOT NULL,
    EffectiveStartDate DATETIME NOT NULL DEFAULT SYSDATETIME(),
    EffectiveEndDate DATETIME,
    -- CONSTRAINT FK_ProductPriceHistory_Product FOREIGN KEY (ProductID)
    --     REFERENCES SalesLT.Product (ProductID)
);
GO

CREATE TRIGGER trg_ProductPriceHistoryUpdate
ON SalesLT.Product
AFTER UPDATE
AS
BEGIN
    -- SET NOCOUNT ON; -- Na razie nie potrzebna, ale dobra prakty programistyczna

    -- Wstawianie nowych danych do hisotrii
    INSERT INTO SalesLT.ProductPriceHistory (ProductID, StandardCost, ListPrice, EffectiveStartDate)
    SELECT i.ProductID, i.StandardCost, i.ListPrice, SYSDATETIME()
    FROM inserted i
    INNER JOIN deleted d ON i.ProductID = d.ProductID
    WHERE i.StandardCost <> d.StandardCost
       OR i.ListPrice <> d.ListPrice;

    -- Modyfikowanie danych whistorii rekordów zmienionych
    UPDATE SalesLT.ProductPriceHistory
    SET EffectiveEndDate = SYSDATETIME()
    FROM SalesLT.ProductPriceHistory h
    INNER JOIN deleted d ON h.ProductID = d.ProductID
    WHERE h.EffectiveEndDate IS NULL
      AND (h.StandardCost <> d.StandardCost OR h.ListPrice <> d.ListPrice);
END;
GO

CREATE TRIGGER trg_ProductPriceHistoryDelete
ON SalesLT.Product
AFTER DELETE
AS
BEGIN
    -- SET NOCOUNT ON; -- Na razie nie potrzebne, ale dobra praktyka programistyczna

    -- Wstawianie danych do hisotrii 
    UPDATE SalesLT.ProductPriceHistory
    SET EffectiveEndDate = SYSDATETIME()
    FROM SalesLT.ProductPriceHistory h
    INNER JOIN deleted d ON h.ProductID = d.ProductID
    WHERE h.EffectiveEndDate IS NULL
END 
GO


SELECT * FROM SalesLT.ProductPriceHistory
SELECT * FROM dbo.TempViewTest
-- UPDATE SalesLT.Product dobrze
UPDATE SalesLT.Product
SET StandardCost = StandardCost + 1
WHERE ProductID IN (706, 707)
SELECT * FROM SalesLT.ProductPriceHistory

-- UPDATE SalesLT.Product źle
UPDATE SalesLT.Product
SET [Size] = 'XL'
WHERE ProductID = 708
SELECT * FROM SalesLT.ProductPriceHistory

-- DELETE SalesLT.Product
DELETE FROM SalesLT.Product
WHERE ProductID = 706
SELECT * FROM SalesLT.ProductPriceHistory
SELECT ProductID, StandardCost, ListPrice, P.Size
FROM SalesLT.Product P 
GO