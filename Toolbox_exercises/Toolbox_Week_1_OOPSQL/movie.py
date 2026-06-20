from oopsql import OopSqlClass
import sys

oop = OopSqlClass("movies.db")
if not oop.is_valid():
    sys.exit("\nNo valid db connection\n")
else:
    print("\nConnected to db\n")

# db connection is valid


# Query one
query_1 = """SELECT movies.title, ratings.rating 
FROM movies 
JOIN ratings ON movies.id = ratings.movie_id 
WHERE ratings.votes >= ? 
ORDER BY ratings.rating DESC 
LIMIT 10"""

best_movies = oop.get_rows(query_1, placeholders=(10000,))


# Query two
born = int(input("What year was the actor / actrice born? "))
boundary_one = int(input("From which year? "))
boundary_two = int(input("To which year? "))

query_2 = """SELECT people.name, COUNT(movies.id)
FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE movies.year >= ?
AND movies.year <= ?
AND people.birth >= ?
GROUP BY people.id
ORDER BY COUNT(movies.id) DESC
LIMIT 1"""

active_actor = oop.get_rows(query_2, placeholders=(boundary_one, boundary_two, born,))

print("\n----TOP MOVIES---- \n")
for r in best_movies:
    print(r)

print("--------")
print()

if not best_movies or not active_actor:
    print(None)
else:
    print(f"Rows query one: {len(best_movies)}\n") 
    print(f"Rows query two: {len(active_actor)}")