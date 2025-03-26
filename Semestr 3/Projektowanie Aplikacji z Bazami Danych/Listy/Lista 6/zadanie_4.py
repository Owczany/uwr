from pymongo import MongoClient

client = MongoClient('localhost', 27017)
library = client['library']

# Pierwsza część zadania

# Zdobywam informacje o całej kolekcji 'authors'
collection_authors = library.get_collection('authors')

# Wyciągam informacje o dokumentach w danej kolekcji i sortuje je rosnąco po ID-kach
# Pomijam pierwsze dwa dokumenty i ograniczam do 2 wystąpień
documents = collection_authors.find().sort("_id", 1).skip(2).limit(2)  

# Sprawdzam wynik tego zapytania
print(type(documents))
for doc in documents:
    print(doc)

# Output:
# {'_id': 3, 'name': 'Bułhakow'}
# {'_id': 4, 'name': 'Robert Makłowicz'}

# Druga część zadania

# Wydobywam informacje o kolekcji books, poniewaz ma ona u mnie subcollection copies
collection_books = library.get_collection('books')

# Wyciągam informacje o dokumentach w danej kolekcji i filtruje ją po filtrze działającym na jego pod kolekcji
documents = collection_books.find({'copies.condition': 'Good'})

for doc in documents:
    print(doc)

# Output:
# {'_id': 1, 'title': 'How to be nice to strangers', 'authorId': 1, 'copies': [{'copyId': 101, 'condition': 'Good'}, {'copyId': 102, 'condition': 'Bad'}]}
# {'_id': 3, 'title': 'Kocham Gotować', 'authorId': 4, 'copies': [{'copyId': 104, 'condition': 'Good'}]}
