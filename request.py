from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///mydatabase.db', echo=True)
conn = engine.connect()
result = conn.execute(text("SELECT * FROM clean_stations LIMIT 5")).fetchall()

print(result)
conn.close()
