"""
Description:
 Creates the relationships table in the Social Network database
 and populates it with 100 fake relationships.

Usage:
 python create_relationships.py
 python -c "import sys; print(sys.executable)"
"""


import os

import sqlite3
from random import randint, choice
from faker import Faker

con = sqlite3.connect('social_network.db')
curs = con.cursor()

# Determine the path of the database
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'social_network.db')

    # TODO: Function body
    # Hint: See example code in lab instructions entitled "Add the Relationships Table"
create_relationships_table_query = """
 CREATE TABLE IF NOT EXISTS relationships
 (
 id INTEGER PRIMARY KEY,
 person1_id INTEGER NOT NULL,
 person2_id INTEGER NOT NULL,
 type TEXT NOT NULL,
 start_date DATE NOT NULL,
 FOREIGN KEY (person1_id) REFERENCES people (id),
 FOREIGN KEY (person2_id) REFERENCES people (id)
 );
"""
# Execute the SQL query to create the 'relationships' table.
curs.execute(create_relationships_table_query)
con.commit()



# TODO: Function body
# Hint: See example code in lab instructions entitled "Populate the Relationships Table"
add_relationship_query = """
INSERT INTO relationships
( 
person1_id,
person2_id,
type,
start_date
)
VALUES (?, ?, ?, ?);
"""
fake = Faker()
# Randomly select first person in relationship
person1_id = randint(1, 200)
# Randomly select second person in relationship
# Loop ensures person will not be in a relationship with themself
person2_id = randint(1, 200)
while person2_id == person1_id:
    person2_id = randint(1, 200)
# Randomly select a relationship type
rel_type = choice(('friend', 'spouse', 'partner', 'relative'))
# Randomly select a relationship start date between now and 50 years ago
start_date = fake.date_between(start_date='-50y', end_date='today')
# Create tuple of data for the new relationship
new_relationship = (person1_id, person2_id, rel_type, start_date)
# Add the new relationship to the DB
curs.execute(add_relationship_query, new_relationship)
con.commit()


# SQL query to get all relationships
all_relationships_query = """
SELECT person1.name, person2.name, start_date, type FROM relationships
JOIN people person1 ON person1_id = person1.id
JOIN people person2 ON person2_id = person2.id;
"""
# Execute the query and get all results
curs.execute(all_relationships_query)

all_relationships = curs.fetchall()
con.close()

# Print sentences describing each relationship
for person1, person2, start_date, type in all_relationships:
    print(f'{person1} has been a {type} of {person2} since {start_date}.')



