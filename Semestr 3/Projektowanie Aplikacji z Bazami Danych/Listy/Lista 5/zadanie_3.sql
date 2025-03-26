SET SHOWPLAN_TEXT ON;
GO
-- Twoje zapytanie
SELECT * FROM Czytelnik WHERE Nazwisko = 'Kowalski';
GO
SET SHOWPLAN_TEXT OFF;

SET STATISTICS IO ON;    
SET STATISTICS TIME ON;  
GO

SET STATISTICS IO OFF;    
SET STATISTICS TIME OFF;  
GO

DBCC DROPCLEANBUFFERS;
DBCC FREEPROCCACHE;

SELECT 
    k.Ksiazka_ID, 
    k.Tytul, 
    e.Egzemplarz_ID, 
    e.Sygnatura
FROM 
    Ksiazka k
JOIN 
    Egzemplarz e 
ON 
    k.Ksiazka_ID = e.Ksiazka_ID
WHERE 
    k.Cena > 50;

DROP INDEX IF EXISTS idx_Egzemplarz_Ksiazka ON Egzemplarz
DROP INDEX IF EXISTS idx_Ksiazka_Covering ON Ksiazka

-- CREATE CLUSTERED INDEX idx_Egzemplarz_Clustered 
-- ON Egzemplarz (Egzemplarz_ID)

CREATE NONCLUSTERED INDEX idx_Egzemplarz_Ksiazka
ON Egzemplarz (Ksiazka_ID)

CREATE NONCLUSTERED INDEX idx_Ksiazka_Covering
ON Ksiazka (Ksiazka_ID, Cena)
INCLUDE (Tytul)

DBCC SHOW_STATISTICS('Ksiazka', 'idx_Ksiazka_Covering')