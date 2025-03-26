DROP TRIGGER IF EXISTS trg_MaxSpecimensPerBook
GO

-- SELECT * FROM dbo.Egzemplarz
-- SELECT * FROM dbo.Ksiazka
-- GO

CREATE TRIGGER trg_MaxSpecimensPerBook
ON dbo.Egzemplarz 
AFTER INSERT
AS
BEGIN
    DECLARE @BookID INT

    SELECT TOP 1 @BookID = Ksiazka_ID from inserted

    IF (SELECT COUNT(*) FROM dbo.Egzemplarz WHERE Ksiazka_ID = @BookID) > 5
    BEGIN
        ROLLBACK TRANSACTION
        RAISERROR('Ksiązka nie moze mieć mieć więcej ni 5 egzemplarzy', 16, 1)
    END
END
GO

-- Tego nie damy rady wstawić, bo przekroczymy ilość
INSERT INTO Egzemplarz (Sygnatura, Ksiazka_ID)
VALUES ('S1', 3), ('S2', 3), ('S3', 3), ('S4', 3)
GO

INSERT INTO Egzemplarz (Sygnatura, Ksiazka_ID)
VALUES ('S420', 3)

SELECT * FROM dbo.Egzemplarz WHERE Ksiazka_ID = 3

DELETE FROM dbo.Egzemplarz WHERE Ksiazka_ID = 3 AND Sygnatura = 'S420'


