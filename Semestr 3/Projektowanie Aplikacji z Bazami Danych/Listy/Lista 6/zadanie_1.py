from pymongo import MongoClient

# Komenda uruchamiająca serwer w jawnej postaci (w sensie, ze nie w tle)
# W terminalu wpisujemy: mongod --dbpath ~/'sciezka docelowa'
# W moim przypadku komenda wygląda tak:
# mongod --dbpath ~/Data/db
# Po wpisaniu wyzej napisanej komendy odpala się lokalny serwer na porcie 27017

# Żeby połączył się klient wpisuje w nowej zakładce terminala komende:
# mongosh -> To jest odwołanie do shella MongoDB
# Potem wybieram baze dany za pomoca komendy: use nazwa_bazy_danych
# U mnie komenda wygląda nastepująco:
# use library

# W terminalu po połączeniu się do clienta wpisuje dane komendy
# Powodują one dodanie dokumentów testowy do kolekcji
# db.authors.insertOne({_id:1, name:"Golden"})
# db.authors.insertOne({_id:2, name:"Golding"})
# db.authors.insertOne({_id:3, name:"Bułhakow"})

# Komendą: show collections -  sprawdzamy jakie mamy kolekcje w naszej bazie danych

# Połączenie z serwerem MongoDB
client = MongoClient("localhost", 27017) # Łączenie się z klientem na porcie 27017 jest to domyślny port dla MongoDB
print(client.list_database_names()) # Tutaj moge sobie sprawdzić juz utworzone przeze mnie bazki <3
db = client['library'] # Ściągam dane o bazie danych o nazwie 'library'

# Prosta klasa reprezentująca kolekcję Author
class Author:
    def __init__(self, _id, name):
        self.id = _id
        self.name = name

# Uzyskanie dostępu kolekcji 'authors'
authors_collection = db["authors"]

# Pobranie wszystkich dokumentów z kolekcji 'authors'
items = authors_collection.find()

authors = [Author(_id=item.get("_id"), name=item.get("name")) for item in items] # Lista juz obiektów z kolekcji authors
for author in authors:
    print(author.name)

# Output:
# ['admin', 'config', 'library', 'local']
# Golden
# Golding
# Bułhakow