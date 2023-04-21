from values import bring_values
from queries import make_queries

new_values = input("Viedäänkö hinnat apista tietokantaan? (K / E) ")

if new_values.upper() == "K":
    bring_values()

make_queries()