DROP TABLE IF EXISTS dbo.Products;
DROP TABLE IF EXISTS dbo.Prices;
DROP TABLE IF EXISTS dbo.Rates;
GO

CREATE TABLE dbo.Products(
    ID INT NOT NULL PRIMARY KEY,
    ProductName VARCHAR(40)
)
GO

CREATE TABLE dbo.Rates(
    Currency VARCHAR(3) NOT NULL PRIMARY KEY,
    PricePLN MONEY
) 
GO

CREATE TABLE dbo.Prices(
    ProductID INT NOT NULL,
    Currency VARCHAR(3),
    Price MONEY,
    UNIQUE (ProductID, Currency)
)
GO

INSERT INTO dbo.Products (ID, ProductName)
VALUES 
(1, 'MacBook Air M1'),
(2, 'MacBook Pro M2'),
(3, 'iPhone 16 Pro'),
(4, 'iPad 12')
GO

INSERT INTO dbo.Rates (Currency, PricePLN) 
VALUES
('USD', 4.02),
('GBP', 5.22),
('PLN', 1.00)
GO

INSERT INTO dbo.Prices (ProductID, Currency, Price)
VALUES
(1, 'USD', 4999),
(1, 'GBP', 4999),
(2, 'PLN', 6999),
(2, 'CZK', 6999),
(3, 'USD', 3999),
(3, 'CZK', 3999),
(4, 'USD', 3299),
(4, 'GBP', 3299)
GO

-- Podglądnięcie tabel
SELECT * FROM dbo.Products
SELECT * FROM dbo.Prices
SELECT * FROM dbo.Rates
GO

DECLARE c CURSOR FOR SELECT ProductID, Currency FROM dbo.Prices
OPEN c

DECLARE @ID INT, @Currency VARCHAR(3), @PricePLN MONEY
FETCH NEXT FROM c INTO @ID, @Currency
WHILE (@@FETCH_STATUS = 0)
BEGIN   
    IF (@Currency NOT IN (SELECT Currency FROM dbo.Rates))
    BEGIN
        PRINT 'Nie ma przelicznika dla waluty: ' + @Currency
        DELETE FROM dbo.Prices WHERE Currency = @Currency
    END
    ELSE
    BEGIN
        SELECT @PricePLN = PricePLN FROM dbo.Rates WHERE @Currency = Currency
        UPDATE dbo.Prices
        SET Price = ROUND(Price / @PricePLN, 2)
        WHERE @ID = ProductID AND @Currency = Currency
        PRINT 'Zmiana wartości z PLN na ' + @Currency
    END
    FETCH NEXT FROM c INTO @ID, @Currency
END

CLOSE c
DEALLOCATE c

SELECT * FROM dbo. Products
SELECT * FROM dbo.Prices
SELECT * FROM dbo.Rates
GO