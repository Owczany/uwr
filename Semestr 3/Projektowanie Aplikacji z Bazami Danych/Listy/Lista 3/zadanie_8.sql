SELECT name AS 'Database name', is_recursive_triggers_on AS 'Recursive Triggers Enabled'
FROM sys.databases
GO

ALTER DATABASE [owczana-baza-danych]
SET RECURSIVE_TRIGGERS ON;

drop table if exists budzet;
go
create table budzet
(
  nazwa_wydzialu varchar(30) not null,
  nazwa_wydzialu_nadrzednego varchar(30) null,
  budzet_miesieczny int not null
)
go

delete from budzet
insert budzet values( 'Szkolenia krajowe', 'Szkolenia', 10 )
insert budzet values( 'Szkolenia', 'Us�ugi edukacyjne', 100 )
insert budzet values( 'Us�ugi edukacyjne', 'Us�ugi', 500 )
insert budzet values( 'Us�ugi', null, 1200 )
go

drop trigger if exists update_budzet
go
create trigger update_budzet on budzet after update as
begin
  declare @rows int
  set @rows=@@rowcount
  if ( @rows=0 ) return
  if ( @rows>1 ) begin
    print 'Mo�na modyfikowa� tylko jeden wiersz jednocze�nie'
    rollback transaction
    return
  end
  if ( ( select nazwa_wydzialu_nadrzednego from inserted ) is null ) return
  update budzet set budzet_miesieczny=budzet_miesieczny +
    ( select budzet_miesieczny from inserted ) -
    ( select budzet_miesieczny from deleted )
    where nazwa_wydzialu=( select nazwa_wydzialu_nadrzednego from deleted )
end
go

select * from budzet

update budzet set budzet_miesieczny=30 where nazwa_wydzialu = 'Szkolenia krajowe'

select * from budzet
