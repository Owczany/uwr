EXEC sys.sp_who; -- Sprawdza, kto ma z nim sesję

SELECT @@SPID

CREATE TABLE #LocalTempTable (
    id INT,
    text VARCHAR(30),
);

CREATE TABLE ##GlobalTempTable(
    id INT,
    text VARCHAR(30)
);

INSERT INTO #LocalTempTable (id, text)
VALUES (1, 'some text'), (2, 'other text'), (3, 'idk')

INSERT INTO ##GlobalTempTable (id, text)
VALUES (1, 'some global text'), (2, 'other nglobal text'), (3, 'global idk')

SELECT * FROM #LocalTempTable
SELECT * FROM ##GlobalTempTable
GO

SELECT * FROM #LocalTempTable
SELECT * FROM ##GlobalTempTable
GO

SELECT * FROM tempdb.INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME LIKE '#%' OR  TABLE_NAME LIKE '##%'


-----
/*
TABLE VARIABLE -> Dostępny w sesji 1 wszej tylko zyje do konca batcha (wsadu)
TABLE LOCAL TEMP -> Dostępny cały czas w ciągu pierwszej sesji
TABLE GLOBAL TEMP -> Dostępny w kazdej sejsji zyje do ostatniego uzycia
*/