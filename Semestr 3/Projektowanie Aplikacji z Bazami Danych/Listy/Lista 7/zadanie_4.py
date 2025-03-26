from neo4j import GraphDatabase
from private import URI, USER_NAME, PASSWORD # Prywatne dane do logowania do serwera/instancji

URI = URI
AUTH = (USER_NAME, PASSWORD)

# Zapytanie wypisujące wszykise osoby z naszej bazy danych w formie tabelki
query = '''
MATCH (p:Person)
RETURN p
'''

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    # Sprawdzamy, czy połączlismy się z serwerem
    driver.verify_connectivity()
    print("Connection established.")

    # Wyciągamy nasze dane z serwera
    records, summary, keys = driver.execute_query(
    query,
    database_="neo4j",
    )

    # Loop through results and do something with them
    for record in records:
        print(record.data())

    # Summary information
    print("The query: {query} \nreturned {records_count} records in {time} ms.".format(
        query=summary.query, records_count=len(records),
        time=summary.result_available_after,
    ))

# OUTPUT:
# Connection established.
# {'p': {'name': 'Charlie Sheen'}}
# {'p': {'name': 'Martin Sheen'}}
# {'p': {'name': 'Michael Douglas'}}
# {'p': {'name': 'Oliver Stone'}}
# {'p': {'name': 'Rob Reiner'}}
# {'p': {'name': 'Cezary Pazura'}}
# {'p': {'name': 'Katarzyna Figura'}}
# The query: 
# MATCH (p:Person)
# RETURN p
 
# returned 7 records in 2 ms.
