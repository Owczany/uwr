-- set transaction isolation level serializable;
-- set transaction isolation level repeatable read;
-- set transaction isolation level read COMMITTED;
set transaction isolation level read UNCOMMITTED;
begin TRANSACTION
insert liczby2 values ( 1 )

update liczby1 set liczba=10

SELECT * FROM liczby1
SELECT * FROM liczby2

commit
