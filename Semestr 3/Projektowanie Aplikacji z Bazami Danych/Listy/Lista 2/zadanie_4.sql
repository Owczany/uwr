CREATE TYPE CzytelnikIDTable AS TABLE
(
    Czytelnik_ID INT
);

-- ZADANIE 2
DROP PROCEDURE IF EXISTS GetBorrowedDaysSum 
GO

CREATE PROCEDURE GetBorrowedDaysSum
    @Czytelnicy CzytelnikIDTable READONLY
AS
BEGIN
    SELECT
        c.Czytelnik_ID,
        SUM(w.Liczba_Dni)
    FROM 
        @Czytelnicy c
    JOIN
        Wypozyczenie w ON w.Czytelnik_ID = c.Czytelnik_ID
    GROUP BY
        c.Czytelnik_ID;
END;
GO

-- Deklaracja tabeli tymczasowej
DECLARE @Czytelnicy CzytelnikIDTable;

-- Dodajemy identyfikatory czytelników
INSERT INTO @Czytelnicy (Czytelnik_ID)
SELECT Czytelnik_ID FROM Czytelnik -- Przykładowe ID

-- Wywołanie procedury
EXEC GetBorrowedDaysSum @Czytelnicy;
