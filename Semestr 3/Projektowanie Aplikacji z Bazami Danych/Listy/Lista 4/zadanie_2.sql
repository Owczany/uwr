DROP PROCEDURE IF EXISTS SalesLT.SaveTrans
GO

CREATE PROCEDURE SalesLT.SaveTrans
    @ProductID INT 
AS 
    DECLARE @TranCounter INT;  
    SET @TranCounter = @@TRANCOUNT;  
    IF @TranCounter > 0  
        SAVE TRANSACTION ProcedureSave;  
    ELSE  
        BEGIN TRANSACTION;
    BEGIN TRY
        DELETE SalesLT.Product  
            WHERE ProductID = @ProductID;  
        IF @TranCounter = 0  
            COMMIT TRANSACTION; 
    END TRY  
    BEGIN CATCH  
        IF @TranCounter = 0  
            ROLLBACK TRANSACTION;  
        ELSE  
            IF XACT_STATE() <> -1  
                ROLLBACK TRANSACTION ProcedureSave;  
  
        -- After the appropriate rollback, echo error  
        -- information to the caller.  
        DECLARE @ErrorMessage NVARCHAR(4000);  
        DECLARE @ErrorSeverity INT;  
        DECLARE @ErrorState INT;  
  
        SELECT @ErrorMessage = ERROR_MESSAGE();  
        SELECT @ErrorSeverity = ERROR_SEVERITY();  
        SELECT @ErrorState = ERROR_STATE();  
  
        RAISERROR (@ErrorMessage, -- Message text.  
                   @ErrorSeverity, -- Severity.  
                   @ErrorState -- State.  
                   );  
    END CATCH  
GO  


-- SELECT TOP 10 * FROM SalesLT.Product
-- DELETE FROM SalesLT.Product WHERE ProductID = 680

EXEC SalesLT.SaveTrans 0;