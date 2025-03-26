DROP TABLE IF EXISTS firstnames
DROP TABLE IF EXISTS lastnames
DROP TABLE IF EXISTS fldata

CREATE TABLE firstnames(
    id INT PRIMARY KEY IDENTITY(1, 1),
    firstname NVARCHAR(20), -- NVARCHAR zajmuje więcej miejsca niz VARCHAR ale umozliwia przechowywanie rozne znaki
);

CREATE TABLE lastnames(
    id INT PRIMARY KEY IDENTITY(1, 1),
    lastname NVARCHAR(30),
);

CREATE TABLE fldata(
    firstname NVARCHAR(20),
    lastname NVARCHAR(30),
    PRIMARY KEY (firstname, lastname),
);

INSERT INTO firstnames (firstname)
VALUES ('Adam'), ('Piotr'), ('Robert'), ('Krzyś');

INSERT INTO lastnames (lastname)
VALUES ('Nowak'), ('Pijanowski'), ('Kowalski'), ('Palikot')
GO

------------------------

DROP PROCEDURE IF EXISTS GenerateRandomPairs
GO

CREATE PROCEDURE GenerateRandomPairs @n INT
AS
BEGIN
    -- Wyczyśćmy tablicę fldata
    DELETE fldata

    -- Sprawdzanie, czy n nie jest za duze
    DECLARE @TotalPairs INT;
    SELECT @TotalPairs = COUNT(*) -- Uzywamy select, zamiast set
    FROM firstnames, lastnames;

    IF @n > @TotalPairs
    BEGIN
       ; THROW 50001, 'Nie ma tylu kombinacji', 1
    END

    DECLARE @first NVARCHAR(20), @last NVARCHAR(30);

    WHILE @n > 0
    BEGIN
        SELECT TOP 1 @first = firstname FROM firstnames ORDER BY NEWID();
        SELECT TOP 1 @last = lastname FROM lastnames ORDER BY NEWID();

        IF NOT EXISTS (SELECT * FROM fldata WHERE firstname = @first AND lastname = @last)
        BEGIN
            INSERT INTO fldata (firstname, lastname)
            VALUES (@first, @last)

            SET @n = @n - 1
        END
    END
END
GO

-- Wywołanie procedury
EXEC GenerateRandomPairs 8;

-- Wyniki
SELECT * FROM fldata

-- Wywołanie błednej procedury
EXEC GenerateRandomPairs 17
GO
