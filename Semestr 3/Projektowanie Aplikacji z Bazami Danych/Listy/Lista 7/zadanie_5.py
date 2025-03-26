from neo4j import GraphDatabase
from private import URI, USER_NAME, PASSWORD # Prywatne dane do logowania do serwera/instancji

# Klasa Person
class Person:
    # Konstuktor 
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'Person(name = {self.name})'

# Klasa obsługująca połączenie i zapytania
class NeoService:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # CREATE
    def create_person(self, person):
        query = "CREATE (p:Person {name: $name}) RETURN p"
        with self.driver.session() as session:
            records = session.run(query, name=person.name)
            record = records.single()
            return self._map_person(record['p'])

    # READ
    def get_all_persons(self):
        query = 'MATCH (p:Person) RETURN p'
        with self.driver.session() as session:
            records = session.run(query)
            return [self._map_person(record['p']) for record in records]

    # UPDATE
    def update_person(self, person, new_name):
        query = 'MATCH (p:Person {name: $name}) SET p.name = $new_name RETURN p '
        with self.driver.session() as session:
            records = session.run(query, name=person.name, new_name=new_name)
            record = records.single()
            return self._map_person(record["p"])

    # DELETE
    def delete_person(self, person):
        query = """
        MATCH (p:Person {name: $name})
        DETACH DELETE p
        """
        with self.driver.session() as session:
            session.run(query, name=person.name)
            return f"Person with name '{person.name}' deleted."

    # Converter z danych na obiekt Person
    def _map_person(self, node):
        return Person(name=node["name"])

if __name__ == "__main__":
    # Inicjalizacja serwisu Neo4j
    service = NeoService(URI, USER_NAME, PASSWORD)

    try:
        # Tworzenie nowego node'a
        keanu = Person(name="Keanu Reeves")
        created_person = service.create_person(keanu)
        print("Created:", created_person)

        # Pobranie wszystkich node'ow
        all_persons = service.get_all_persons()
        print("All Persons:", all_persons)

        # Modyfikowanie node'a
        updated_person = service.update_person(person=keanu, new_name='Tom Hanks')
        print("Updated:", repr(updated_person))


        # Usunięcie node'a
        deletion_message = service.delete_person(updated_person)
        print(deletion_message)

    finally:
        # Trzeba pamiętać, zeby zamknąć serwis
        service.close()

# OUTPUT:
# Created: Keanu Reeves
# All Persons: [Person(name = Charlie Sheen), Person(name = Martin Sheen), Person(name = Michael Douglas), Person(name = Oliver Stone), Person(name = Rob Reiner), Person(name = Cezary Pazura), Person(name = Keanu Reeves), Person(name = Katarzyna Figura)]
# Updated: Person(name = Tom Hanks)
# Person with name 'Tom Hanks' deleted.
