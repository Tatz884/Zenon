from typing import List, Callable
from ..schemas.words import WordsList


# def get_connection(database_name: str = "enwiki"):
#     """Establish and return a connection to the specified database."""
#     return toolforge.connect(database_name)



# def get_words_from_db() -> WordsList:
#     # Logic to fetch words from external database
#     # Example:
#     # conn = toolforge.connect("enwiki")
#     # cursor = conn.cursor()
#     # cursor.execute("SELECT word_column FROM words_table")
#     # words = cursor.fetchall()
#     # conn.close()
#     # return [word[0] for word in words]
#     data = [
#         {
#             "wiktionary_id": 1,
#             "original_form": "mamić",
#             "changed_form": "mamić",
#             "grammatical_group": "verb",
#             "change_logic": "first-person singular present",
#             "language": "Polish"
#         },
#         {
#             "wiktionary_id": 2,
#             "original_form": "mama",
#             "changed_form": "mamy",
#             "grammatical_group": "noun",
#             "change_logic": ["genitive", "singular"],
#             "language": "Polish"
#         },
#         {
#             "wiktionary_id": 3,
#             "original_form": "mamić",
#             "changed_form": "mamiłęm",
#             "grammatical_group": "verb",
#             "change_logic": ["first-person", "singular", "past", "masculine"],
#             "language": "Polish"
#         }
#     ]
    
#     # Mapping the result to the schema
#     return data


# def get_table_names(database_name: str = "enwiki") -> List[str]:
#     """Fetch the list of table names from the specified database."""
    
#     # Connect to the specified database
#     conn = get_connection(database_name)
    
#     try:
#         # Create a cursor object to execute queries
#         with conn.cursor() as cur:
#             cur.execute("SHOW TABLES;")
#             tables = cur.fetchall()

#         # Extract and return the table names
#         return [table[0] for table in tables]
    
#     finally:
#         # Ensure the connection is closed regardless of success or error
#         conn.close()