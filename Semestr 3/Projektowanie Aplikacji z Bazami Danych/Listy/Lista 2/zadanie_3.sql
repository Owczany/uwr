CREATE TYPE NewReaders AS TABLE (
    PESEL CHAR(11),
    Nazwisko VARCHAR(30),
    Miasto VARCHAR(30),
    Data_Urodzenia DATE
);
GO

DROP PROCEDURE IF EXISTS IntroduceNewReader;
GO

DROP PROCEDURE IF EXISTS IntroduceNewReaders;
GO

CREATE PROCEDURE IntroduceNewReader @PESEL CHAR(11), @Nazwisko VARCHAR(30), @Miasto VARCHAR(30), @DataUrodzenia DATE
AS
BEGIN
    -- Sprawdzenie PESELU
    IF LEN(@PESEL) != 11 OR @PESEL NOT LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
    BEGIN
        ; THROW 51000, 'Błędny PESEL', 1;
    END

    IF LEN(@Nazwisko) < 3 OR @Nazwisko COLLATE Polish_BIN NOT LIKE '[A-Z]%'
    BEGIN
        ; THROW 51001, 'Błędne nazwisko czytelnika', 1;
    END

    IF TRY_CONVERT(DATE, @DataUrodzenia, 102) IS NULL
    BEGIN
        ; THROW 51002, 'Błędna data urodzenia', 1;
    END

    -- Wstawianie wartości
    INSERT INTO Czytelnik (PESEL, Nazwisko, Miasto, Data_Urodzenia)
    VALUES (@PESEL, @Nazwisko, @Miasto, @DataUrodzenia)

    PRINT 'Nowy czytelnik zawitał w naszej bibliotece (' + @Nazwisko + ')'
END
GO

CREATE PROCEDURE IntroduceNewReaders @Czytelnicy NewReaders READONLY
AS
BEGIN
    DECLARE c CURSOR FOR SELECT * FROM @Czytelnicy;
END
GO

DECLARE @Czytelnicy NewReaders
INSERT INTO @Czytelnicy (PESEL, Nazwisko, Miasto, Data_Urodzenia)
VALUES 
('321321', 'Pijanowski', 'Wroclaw', '2004-02-21'),
('32131', 'Rajba', 'Warszawa', '1999-01-13'),
('2321', 'Garncarek', 'Gdansk', '1987-06-14');

EXEC IntroduceNewReader '12345678910', 'Lewandowski', 'Barcelona', '1987-01-16'; -- Dobry rekord
GO
EXEC IntroduceNewReader '1234567A910', 'Lewandowski', 'Barcelona', '1987-01-16'; -- Błąd peselu
GO
EXEC IntroduceNewReader '12345678910', 'zleNazwisko', 'Wroclaw', '2004-01-01'; -- Błąd nazwiska
GO
EXEC IntroduceNewReader '12345678910', 'Lewandowski', 'Barcelona', '1987-13-16';
GO
-- EXEC IntroduceNewReaders @Czytelnicy;
-- GO

SELECT * FROM dbo.Czytelnik
-- DELETE Czytelnik WHERE PESEL = '12345678910'
