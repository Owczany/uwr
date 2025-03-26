DROP TABLE IF EXISTS SalesOrderDetail_Backup

SELECT TOP 0 SalesORderID, OrderQty INTO SalesOrderDetail_Backup
FROM SalesLT.SalesOrderDetail

DECLARE @startTime DATETIME2, @endTime DATETIME2
SET @startTime = GETDATE()

INSERT INTO SalesOrderDetail_Backup
SELECT SalesOrderID, OrderQty 
FROM SalesLT.SalesOrderDetail

SET @endTime = GETDATE()

PRINT 'Wersja SQL: ' + CAST(DATEDIFF(MILLISECOND, @startTime, @endTime) AS VARCHAR) + ' ms'

SELECT * FROM SalesOrderDetail_Backup
GO

TRUNCATE TABLE SalesOrderDetail_Backup

DECLARE c CURSOR FOR SELECT SalesORderID, OrderQty FROM SalesLT.SalesOrderDetail

OPEN c

DECLARE @start DATETIME2, @end DATETIME2
DECLARE @id INT, @order SMALLINT

SET @start = SYSDATETIME()
FETCH NEXT FROM c INTO @id, @order

WHILE ( @@fetch_status=0 )
begin
  INSERT INTO SalesOrderDetail_Backup
  VALUES (@id, @order)
  FETCH NEXT FROM c INTO @id, @order
end
close c
deallocate c
SET @end = SYSDATETIME()
PRINT 'Wersja z kursorami: ' + CAST(DATEDIFF(MILLISECOND, @start, @end) AS VARCHAR) + ' ms'

SELECT * FROM SalesOrderDetail_Backup
GO
