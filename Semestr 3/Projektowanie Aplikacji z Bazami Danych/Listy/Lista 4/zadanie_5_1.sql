drop table if exists liczby1;
drop table if exists liczby2;
create table liczby1 ( liczba int )
create table liczby2 ( liczba int )
go

insert into liczby1 values (0);
insert into liczby2 values (0);
GO


-- set transaction isolation level serializable;
-- set transaction isolation level repeatable read;
-- set transaction isolation level read COMMITTED;
set transaction isolation level read UNCOMMITTED;
begin TRANSACTION
insert liczby1 values ( 1 )

update liczby2 set liczba=10

SELECT * FROM liczby1
SELECT * FROM liczby2

COMMIT
