from pymongo import MongoClient

client = MongoClient('localhost', 27017)
store = client['store'] # Baza danych store
orders_collection = store['orders'] # Kolekcja orders

# Przykładowe dane
# orders_collection.insert_many([
#     {'_id': 1, 'name': 'Piotr Pijanowski', 'total': 55, 'type': 'receipt'},
#     {'_id': 2, 'name': 'Robert Makłowicz', 'total': 20, 'type': 'invoice'},
#     {'_id': 3, 'name': 'Magda Gessler', 'total': 160, 'type': 'receipt'},
#     {'_id': 4, 'name': 'Magda Gessler', 'total': 320, 'type': 'invoice'},
#     {'_id': 5, 'name': 'Piotr Pijanowski', 'total': 70, 'type': 'invoice'},
#     {'_id': 6, 'name': 'Robert Lewandowski', 'total': 30, 'type': 'receipt'},
#     {'_id': 7, 'name': 'Mariusz Kowalski', 'total': 25, 'type': 'invoice'},
#     {'_id': 8, 'name': 'Robert Makłowicz', 'total': 150, 'type': 'invoice'},
# ])

pipeline = [
    {
        "$match": {'type': 'invoice'}
    },
    {
        "$group": {
            "_id": "$name",  # Grupowanie po polu 'name'
            "totalAmount": {"$sum": "$total"},  # Sumowanie wartości wydanej
            "type": {"$first": "$type"}
        },
    },
    {
        "$sort": {"totalAmount": -1}  # Sortowanie malejąco po sumie zamówień
    },
]

# Plus wypisuje je w kolejności malejące
print('Wypisuje dokumenty z sumowaną wartością wdana w sklepie dla danych osób, które wzięły fakturę!')
for doc in orders_collection.aggregate(pipeline):
    print(doc)

# Output
# Wypisuje dokumenty z sumowaną wartością wdana w sklepie dla danych osób, które wzięły fakturę!
# {'_id': 'Magda Gessler', 'totalAmount': 320, 'type': 'invoice'}
# {'_id': 'Robert Makłowicz', 'totalAmount': 170, 'type': 'invoice'}
# {'_id': 'Piotr Pijanowski', 'totalAmount': 70, 'type': 'invoice'}
# {'_id': 'Mariusz Kowalski', 'totalAmount': 25, 'type': 'invoice'}
