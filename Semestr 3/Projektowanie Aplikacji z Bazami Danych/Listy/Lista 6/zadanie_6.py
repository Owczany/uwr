from pymongo import MongoClient

# Konfiguracja shardingu w MongoDB

# Krok 1: Uruchom serwery shardów i serwery konfiguracyjne
# - Uruchom instancje MongoDB jako shardy (każdy shard musi być częścią repliki): 
#   mongod --shardsvr --replSet shard1 --dbpath /data/shard1 --port 27018
#   mongod --shardsvr --replSet shard2 --dbpath /data/shard2 --port 27019
#
# - Uruchom serwer konfiguracyjny:
#   mongod --configsvr --replSet configReplSet --dbpath /data/config --port 27017

# Krok 2: Utwórz replikę serwera konfiguracyjnego
# - Połącz się z serwerem konfiguracyjnym w powłoce mongo:
#   mongosh --port 27017
# - Skonfiguruj replikę serwera konfiguracyjnego:
#   rs.initiate({ _id: "configReplSet", configsvr: true, members: [{ _id: 0, host: "localhost:27017" }] })

# Krok 3: Inicjalizacja replik shardów
# - Połącz się z każdym shardem i zainicjuj replikację:
#   mongosh --port 27018
#   rs.initiate({ _id: "shard1", members: [{ _id: 0, host: "localhost:27018" }] })
#
#   mongosh --port 27019
#   rs.initiate({ _id: "shard2", members: [{ _id: 0, host: "localhost:27019" }] })

# Krok 4: Uruchom mongos (router shardingowy)
# - Uruchom mongos, aby połączyć serwery shardów z serwerem konfiguracyjnym:
#   mongos --configdb configReplSet/localhost:27017 --port 27020

# Krok 5: Połącz się z mongos
#   mongosh --port 27020

# Krok 6: Dodaj shardy do klastra
# - Dodaj shardy do klastra:
#   sh.addShard("shard1/localhost:27018")
#   sh.addShard("shard2/localhost:27019")

# Krok 7: Włącz sharding dla bazy danych i skonfiguruj shard key
# - Włącz sharding
#   sh.enableSharding('store')
#   db.products.createIndex({ category: 1 })
#   sh.shardCollection('store.products', { category: 1 })


# Krok 8: Odpal ponizszy kod

# Łączenie z routerem
client = MongoClient('localhost', 27020)

store = client['store']
products_collection = store['products']

# Przykładowe dane do kolekcji 'products'
products_collection.insert_many([
    {'_id': 1, 'name': 'Laptop', 'category': 'Electronics', 'price': 1000},
    {'_id': 2, 'name': 'Smartphone', 'category': 'Electronics', 'price': 500},
    {'_id': 3, 'name': 'Headphones', 'category': 'Accessories', 'price': 100},
    {'_id': 4, 'name': 'Shoes', 'category': 'Fashion', 'price': 80},
    {'_id': 5, 'name': 'T-shirt', 'category': 'Fashion', 'price': 20},
    {'_id': 6, 'name': 'Watch', 'category': 'Accessories', 'price': 200},
])

# Krok 9: Odpala ponizszą komendę w terminalu, zeby sprawdzic rozmieszczenie danych
# db.products.getShardDistribution()