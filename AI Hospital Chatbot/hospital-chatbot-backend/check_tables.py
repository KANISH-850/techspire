import psycopg2
try:
    conn=psycopg2.connect(dbname='hospital_chatbot', user='postgres', password='KANISHAJAI2007', host='127.0.0.1', port=5432)
    cur=conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = cur.fetchall()
    print("TABLES:")
    for t in tables:
        print(t[0])
except Exception as e:
    print(e)
