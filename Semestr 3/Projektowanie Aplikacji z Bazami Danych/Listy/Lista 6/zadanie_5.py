# To zadanie jest bardziej ciezkie konfiguracyjnie
# Po pierwsze w naszej ściezce musimy zrobić 3 dodatkowe foldery
# Przejdzmy do tego, ze jest ściezka i foldery nazywają się: db1, db2, db3
# Odpalamy serwery tak jak na prezentacji z odpowiednio ściezkami do folderów db_
# Komendy w terminalu, ale kazda z komend w osobnym okienku lub zakładce:
# mongod --dbpath ~/Data/db1 --port 10000 --replSet "demo"
# mongod --dbpath ~/Data/db2 --port 20000 --replSet "demo"
# mongod --dbpath ~/Data/db3 --port 30000 --replSet "demo"

# Łaczymy się z pierwszym wezłem
# mongosh --port 10000

# Tworzymy obiekt Replica Set
# var rsConfig = {
#     _id: "demo",
#     members: [
#         { _id: 0, host: "localhost:10000", priority: 10 }, 
#         { _id: 1, host: "localhost:20000" },            
#         { _id: 2, host: "localhost:30000", arbiterOnly: true }
#     ]
# };

# Wpisz 'rsConfig', zeby upenic się, ze wszytsko się zgadza
# rsConfig
# Output tej komendy jest jak wartośc rsConfig, po upownienieniu się, ze. nie ma błedu idziemy dalej
# Wpisujemy / rs.initiate(rsConfig) / ustawia to konfiguracje replication seta
# wpisujemy use test
# db.books.insertOne({_id: 1, title: 'Mistrz i Małgorzata'})
# db.books.find()
# Po tych operacjach wstawilismy z wezła primary jeden dokument do kolekcji books oraz sprawdziliśmy, czy się zapisał
# Output: [ { _id: 1, title: 'Mistrz i Małgorzata' } ]
# Tworzymy połączenie mongosh --port 20000
# Próbujemy insertować dokumennt do kolekcji books 
# db.books.insertOne({_id: 2, title: "Wyznania gejszy"})
# Nie udaje się zinsertować, pojawia się komunikat o tym, ze jesteśmy wezłem secondary, a nie primary
# Wpisujemy db.books.find()
# Mi wypisuje: [ { _id: 1, title: 'Mistrz i Małgorzata' } ]
# Nie wiem czy ma to oznaczać, ze nie powinno tego wypisać, ale wynika z tego, ze domyślnie secondary moze odczytywac dane,
# ale nie moze ich modyfikować, wydaje mi sie ze wykładowaca chciał pokazać cos innego, ale wiele rzeczy z tych prezentacji, 
# albo juz nie działa albo jest przestarzała
# Później wpisujemy komende / rs.secondaryOk() / pojawia się komunikat, ze podana metoda is depracated, czyli właśnie przestarzała.
# Dlatego propnuje mi wpisanie .setReadPref("primaryPreferred"), ale tez to mało zmienia, ale lecimy dalej
# db.books.find() działa jak nalezy
# zabijamy primary node'a i zauwazymy, ze nasze secondary staje sie primary i wteyd mozemy dokonywac wszytskich operacji
# Jak wznowimy mongod --dbpath ~/Data/db1 --port 10000 --replSet "demo", to dawny secondary, który był obecnie priamry wraca, do swojej szarości bycia secondary

# Wersja pythonowa

from pymongo import MongoClient

client = MongoClient('localhost', 27017)


