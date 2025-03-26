from pymongo import MongoClient

# Najpierw tworzę validatory, a potem jest nałozę, zeby utrzymać czytelność kodu
authors_validation_schema = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['name'],
        'properties': {

            'name': {
                'bsonType': 'string',
                'description': 'Name must be a string',
            }

        }
    }
}

books_validation_schema = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['title', 'authorId', 'copies'],
        'properties': {

            'title': {
                'bsonType': 'string',
                'description': 'Title of the book, required and must be a string',
            },

            'authorId': {
                'bsonType': 'number',
                'description': 'ID of the author, required and must be number'
            },

            'copies': {
                'bsonType': 'array',
                'description': 'Array of book copies',
                'items': {
                    'bsonType': 'object',
                    'required': ['copyId', 'condition'],
                    'properties': {

                        'copyId': {
                            'bsonType': 'number',
                            'description': 'ID of the book copy, required and must be number',
                        },

                        'condition': {
                            'bsonType': 'string',
                            'description': 'Condition of the book copy, required and must be string'
                        }

                    }
                }
            }

        }
    }
}

readers_validation_schema = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['name', 'membershipDate'],
        'properties': {

            'name': {
                'bsonType': 'string',
                'description': 'Name of the library reader, required and must be string'
            },

            'membershipDate': {
                'bsonType': 'date',
                'description': 'Date of the membership, required and must be a date in format YYYY-MM-DD',
            }

        }
    }
}

borrowings_validation_schema = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['copyId', 'readerId', 'borrowDate', 'returnDate'],
        'properties': {

            'copyId': {
                'bsonType': 'number',
                'description': 'ID of the book copy, required and must be number'
            },

            'readerId': {
                'bsonType': 'number',
                'description': 'Id of the library reader, required and must be number'
            },

            'borrowDate': {
                'bsonType': 'date',
                'description': 'Date of the borrowed book, required and must be a date in format YYYY-MM-DD',
            },

            'returnDate': {
                'bsonType': ['date', 'null'],
                'description': 'Return date of the book copy, can be null or a valid date in format YYYY-MM-DD'
            }

        }
    }
}

# Łączenie się klienta
client = MongoClient('localhost', 27017)
library = client['library']

# Dodanie walidacji do istniejącej kolekcji
try:
    library.command({
        'collMod': 'authors',
        'validator': authors_validation_schema,
        'validationLevel': 'strict'  # Możliwe wartości: "strict", "moderate", lub "off"
    })

    library.command({
        'collMod': 'books',
        'validator': books_validation_schema,
        'validationLevel': 'strict'
    })

    library.command({
        'collMod': 'readers',
        'validator': readers_validation_schema,
        'validationLevel': 'strict'
    })

    library.command({
        'collMod': 'borrowings',
        'validator': borrowings_validation_schema,
        'validationLevel': 'strict'
    })

    print("Validation schemas applied to all collections in library instance")
except Exception as e:
    print("Error applying validation schemas:", e)


# Udane dodanie czytelnika Piotr Pijanowski
# Udane dodanie nowego wypozyczenia 
# Udane dodanie autora Roberta Makłowicza
try:
    library.authors.insert_one({'_id': 4, 'name': 'Robert Makłowicz'})
    print('Added new author: Robert Makłowicz')
except Exception as e:
    print(f'Adding Robert Makłowicz as author to collection authors failed. Erorr message: {e}')

# Nie udane dodanie autora
try:
    library.authors.insert_one({'_id': 5, 'name': None})
    print('Added new author: null')
except Exception as e:
    print(f'Adding new author failed. Erorr message: {e}')

# Udane dodanie ksiązki Kocham Gotować
try:
    library.books.insert_one({
        '_id': 3,
        'title': 'Kocham Gotować',
        'authorId': 4,
        'copies': [ {'copyId': 104, 'condition': 'Good'} ]
    })
    print('Added new book: Kocham Gotować')
except Exception as e:
    print(f'Adding new book failed. Error: message: {e}')

# Nie udane dodanie ksiązki Lubię Gotować 
try:
    library.books.insert_one({
        '_id': 4,
        'title': 'Lubię Gotować',
        'copies': [ {'copyId': 105, 'condition': 'Good'} ]
    })
    print('Added new book: Lubię Gotować')
except Exception as e:
    print(f'Adding new book failed. Error: message: {e}')

# Output:
# Validation schemas applied to all collections in library instance
# Added new author: Robert Makłowicz
# Adding new author failed. Erorr message: Document failed validation, full error: {'index': 0, 'code': 121, 'errmsg': 'Document failed validation', 'errInfo': {'failingDocumentId': 5, 'details': {'operatorName': '$jsonSchema', 'schemaRulesNotSatisfied': [{'operatorName': 'properties', 'propertiesNotSatisfied': [{'propertyName': 'name', 'description': 'Name must be a string', 'details': [{'operatorName': 'bsonType', 'specifiedAs': {'bsonType': 'string'}, 'reason': 'type did not match', 'consideredValue': None, 'consideredType': 'null'}]}]}]}}}
# Added new book: Kocham Gotować
# Adding new book failed. Error: message: Document failed validation, full error: {'index': 0, 'code': 121, 'errmsg': 'Document failed validation', 'errInfo': {'failingDocumentId': 4, 'details': {'operatorName': '$jsonSchema', 'schemaRulesNotSatisfied': [{'operatorName': 'required', 'specifiedAs': {'required': ['title', 'authorId', 'copies']}, 'missingProperties': ['authorId']}]}}}