from pymongo import MongoClient

# Rutynowa procedura łączenia się klietna z bazą danych
client = MongoClient('localhost', 27017)
library = client['library']

# W taki sposób w pythonie mozemy podjerzeć jakie mamy kolekcje w library
print("Kolekcje w bazie danych 'library':")
print(library.list_collection_names())

# Przy pierwszym wywołaniu pokazuje tylko ['authors']

# Wstawianie ksiązek do naszej bazy danych, która ma w sobie subcollection copies
library.books.insert_many([
    {
        "_id": 1,
        "title": "How to be nice to strangers",
        "authorId": 1,
        "copies": [
            { "copyId": 101, "condition": "Good" },
            { "copyId": 102, "condition": "Bad" }
        ]
    },
    {
        "_id": 2,
        "title": "Why so serious?",
        "authorId": 2,
        "copies": [
            { "copyId": 103, "condition": "Excellent" }
        ]
    }
])

# Wstawianie danych do kolekcji readers
library.readers.insert_many([
    { "_id": 1, "name": "Peter Griffin", "membershipDate": "2024-10-22" },
    { "_id": 2, "name": "John Smith", "membershipDate": "2024-11-15" },
])

# Wstawianie danych do kolekcji borrowings
library.borrowings.insert_many([
    { "_id": 1, "copyId": 101, "readerId": 1, "borrowDate": "2024-10-22", "returnDate": "2024-11-10" },
    { "_id": 2, "copyId": 103, "readerId": 1, "borrowDate": "2024-11-10", "returnDate": None },
    { "_id": 3, "copyId": 101, "readerId": 2, "borrowDate": "2024-11-15", "returnDate": None },
    { "_id": 4, "copyId": 102, "readerId": 2, "borrowDate": "2024-11-15", "returnDate": None }
])

# W taki sposób w pythonie mozemy podjerzeć jakie mamy kolekcje w library
# Przy pierwszym wykonaniu kodu wypisuje [authors, borrowings, books, readers]
print("Kolekcje w bazie danych 'library':")
print(library.list_collection_names())

for doc in library['authors'].find():
    print(doc)

for doc in library['books'].find():
    print(doc)

for doc in library['readers'].find():
    print(doc)

for doc in library['borrowings'].find():
    print(doc)

# Output:
# Kolekcje w bazie danych 'library':
# ['authors']
# Kolekcje w bazie danych 'library':
# ['authors', 'borrowings', 'books', 'readers']
# {'_id': 1, 'name': 'Golden'}
# {'_id': 2, 'name': 'Golding'}
# {'_id': 3, 'name': 'Bułhakow'}
# {'_id': 1, 'title': 'How to be nice to strangers', 'authorId': 1, 'copies': [{'copyId': 101, 'condition': 'Good'}, {'copyId': 102, 'condition': 'Bad'}]}
# {'_id': 2, 'title': 'Why so serious?', 'authorId': 2, 'copies': [{'copyId': 103, 'condition': 'Excellent'}]}
# {'_id': 1, 'name': 'Peter Griffin', 'membershipDate': '2024-10-22'}
# {'_id': 2, 'name': 'John Smith', 'membershipDate': '2024-11-15'}
# {'_id': 1, 'copyId': 101, 'readerId': 1, 'borrowDate': '2024-10-22', 'returnDate': '2024-11-10'}
# {'_id': 2, 'copyId': 103, 'readerId': 1, 'borrowDate': '2024-11-10', 'returnDate': None}
# {'_id': 3, 'copyId': 101, 'readerId': 2, 'borrowDate': '2024-11-15', 'returnDate': None}
# {'_id': 4, 'copyId': 102, 'readerId': 2, 'borrowDate': '2024-11-15', 'returnDate': None}
