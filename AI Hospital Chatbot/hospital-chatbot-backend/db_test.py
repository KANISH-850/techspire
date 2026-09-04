import psycopg2
from psycopg2 import OperationalError

passwords_to_try = [
    "KANISHAJAI2007", 
    "kanish850", 
    "postgres", 
    "root", 
    "admin", 
    "password", 
    "1234", 
    "123456", 
    ""
]

dbname = "hospital_chatbot"
user = "postgres"
host = "127.0.0.1"
port = "5432"

print(f"Trying to connect to {dbname} as {user} on {host}:{port}")

found = False
for pwd in passwords_to_try:
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=pwd, host=host, port=port)
        print(f"SUCCESS! Password is: '{pwd}'")
        conn.close()
        found = True
        break
    except OperationalError as e:
        if "password authentication failed" in str(e):
            continue
        elif "database" in str(e) and "does not exist" in str(e):
            print(f"SUCCESS! Password is: '{pwd}', but database does not exist.")
            found = True
            break
        else:
            print(f"Error with '{pwd}': {e}")

if not found:
    print("None of the common passwords worked.")
