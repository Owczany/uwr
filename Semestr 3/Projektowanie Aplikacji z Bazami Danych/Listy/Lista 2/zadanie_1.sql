CREATE FUNCTION GetReadersWithSpecimenOverDays (
    @Days INT
)
RETURNS @ResultTable TABLE (
    PESEL NVARCHAR(11),
    SpecimensCount INT
)
AS
BEGIN
    INSERT INTO @ResultTable (PESEL, SpecimensCount)
    SELECT
        Cz.PESEL,
        COUNT(Wy.Egzemplarz_ID)
    FROM
        Czytelnik Cz
    JOIN
        Wypozyczenie Wy ON Wy.Czytelnik_ID = Cz.Czytelnik_ID
    WHERE
        Wy.Liczba_Dni > @Days
    GROUP BY
        Cz.PESEL

    RETURN;
END
GO

SELECT * FROM dbo.GetReadersWithSpecimenOverDays(10)
GO
