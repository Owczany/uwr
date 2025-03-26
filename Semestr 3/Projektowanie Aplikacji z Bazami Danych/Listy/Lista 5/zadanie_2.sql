-- Dodanie dannych

SELECT * FROM Czytelnik
-- SELECT * FROM Ksiazka
-- SELECT * FROM Wypozyczenie
-- SELECT * FROM Egzemplarz




DECLARE @i INT = 1;
WHILE @i <= 1000
BEGIN
    INSERT INTO Czytelnik (PESEL, Nazwisko)
    VALUES (RIGHT(CAST(1000000000 + @i AS VARCHAR), 10), 'LastName_' + CAST(@i AS VARCHAR));
    SET @i = @i + 1;
END;


-- INSERT INTO Wypozyczenie (Czytelnik_ID, Egzemplarz_ID)
-- VALUES
-- (20, 1),
-- (21, 2),
-- (22, 3),
-- (23, 4),
-- (25, 5)
-- GO

SET STATISTICS IO OFF;    -- Włącza statystyki odczytu danych
SET STATISTICS TIME ON;  -- Włącza pomiar czasu wykonania
GO

-- Wyczyść pamięć podręczną
DBCC DROPCLEANBUFFERS;
DBCC FREEPROCCACHE;

-- Measure time for Query 1
DECLARE @start_1 DATETIME2, @end_1 DATETIME2;
SET @start_1 = GETDATE();

SELECT DISTINCT c.PESEL, c.Nazwisko
FROM Egzemplarz e
JOIN Ksiazka k ON e.Ksiazka_ID = k.Ksiazka_ID
JOIN Wypozyczenie w ON e.Egzemplarz_ID = w.Egzemplarz_ID
JOIN Czytelnik c ON c.Czytelnik_ID = w.Czytelnik_ID;

SET @end_1 = GETDATE();
PRINT 'Query 1 Execution Time: ' + CAST(DATEDIFF(MILLISECOND, @start_1, @end_1) AS VARCHAR) + ' ms';
GO

-- DBCC SHOW_STATISTICS ('dbo.Czytelnik', 'Czytelnik_PK');

-- Wyczyść pamięć podręczną
DBCC DROPCLEANBUFFERS;
DBCC FREEPROCCACHE;

-- Measure time for Query 2
DECLARE @start_2 DATETIME2, @end_2 DATETIME2;
SET @start_2 = GETDATE();

SELECT c.PESEL, c.Nazwisko
FROM Czytelnik c
WHERE c.Czytelnik_ID IN (
    SELECT w.Czytelnik_ID
    FROM Wypozyczenie w
    JOIN Egzemplarz e ON e.Egzemplarz_ID = w.Egzemplarz_ID
    JOIN Ksiazka k ON e.Ksiazka_ID = k.Ksiazka_ID
);

SET @end_2 = GETDATE();
PRINT 'Query 2 Execution Time: ' + CAST(DATEDIFF(MILLISECOND, @start_2, @end_2) AS VARCHAR) + ' ms';
GO

-- Wyczyść pamięć podręczną
DBCC DROPCLEANBUFFERS;
DBCC FREEPROCCACHE;

-- Measure time for Query 3
DECLARE @start_3 DATETIME2, @end_3 DATETIME2;
SET @start_3 = GETDATE();

SELECT c.PESEL, c.Nazwisko
FROM Czytelnik c
WHERE c.Czytelnik_ID IN (
    SELECT w.Czytelnik_ID
    FROM Wypozyczenie w
    WHERE w.Egzemplarz_ID IN (
        SELECT e.Egzemplarz_ID
        FROM Egzemplarz e
        JOIN Ksiazka k ON e.Ksiazka_ID = k.Ksiazka_ID
    )
)

SET @end_3 = GETDATE();
PRINT 'Query 3 Execution Time: ' + CAST(DATEDIFF(MILLISECOND, @start_3, @end_3) AS VARCHAR) + ' ms';
GO