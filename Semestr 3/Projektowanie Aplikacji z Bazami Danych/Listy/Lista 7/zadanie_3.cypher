// return the movies where person A acted in
MATCH (:Person {name: 'Person A'})-[:ACTED_IN]->(m:Movie)
RETURN m

// return the movies where person A was both the actor and the director
MATCH (p:Person {name: 'Person A'})-[:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(p)
RETURN m

// return actors who didn’t play in any movie
MATCH (a:Person)
WHERE NOT (a)-[:ACTED_IN]->(:Movie)
RETURN a

// return actors who played in more than 2 movies
MATCH (a:Person)-[:ACTED_IN]->(m:Movie)
WITH a, count(m) AS count
WHERE count > 2
RETURN a

// return movies with the larger number of actors
// Załózmy, ze powyzej 2 to duza liczba aktorow
MATCH (a:Person)-[:ACTED_IN]->(m:Movie)
WITH m, count(a) AS count
WHERE count > 2
RETURN m
