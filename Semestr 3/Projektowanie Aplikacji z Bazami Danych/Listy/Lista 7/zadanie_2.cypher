// add 2 new actors and 2 new movies
CREATE 
(cezary:Person {name: 'Cezary Pazura'}), 
(katarzyna:Person {name: 'Katarzyna Figura'}), 
(killer:Movie {title: 'Killer'}), 
(hollywood:Movie {title: 'Pociąg do Hollywood'})

// add 2 new properties to 1 movie,
MATCH (m:Movie {title: 'Killer'})
SET m.rating = 8.2
SET m.genre = 'Comedy'
RETURN m.title, m.rating, m.genre

// add 2 new acted in relations to the existing nodes
// Wersja 1 działa, ale jest niebezpieczna
MATCH 
(cezary:Person {name: 'Cezary Pazura'}),
(katarzyna:Person {name: 'Katarzyna Figura'}),
(killer:Movie {title: 'Killer'}),
(hollywood:Movie {title: 'Pociąg do Hollywood'})
CREATE
(cezary)-[:ACTED_IN {role: 'Killer Gangster'}]->(killer),
(katarzyna)-[:ACTED_IN {role: 'Mariola Wafelek Merlin'}]->(hollywood)

// Wersja 2 lepsza, ale tez jest mniej niebezpieczna
MATCH 
(cezary:Person {name: 'Cezary Pazura'}),
(katarzyna:Person {name: 'Katarzyna Figura'}),
(killer:Movie {title: 'Killer'}),
(hollywood:Movie {title: 'Pociąg do Hollywood'})
MERGE (cezary)-[:ACTED_IN {role: 'Killer Gangster'}]->(killer) 
MERGE (katarzyna)-[:ACTED_IN {role: 'Mariola Wafelek Merlin'}]->(hollywood)

// update 1 movie property
MATCH
(m:Movie {title: 'Killer'})
SET m.rating = 9.3

// remove 1 acted in relation
MATCH
(p:Person {name: 'Michael Douglas'})-[r:ACTED_IN]->(m:Movie {title: 'Wall Street'})
DELETE r