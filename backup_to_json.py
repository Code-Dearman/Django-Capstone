import psycopg2
import json

# Database connection details
conn = psycopg2.connect(
    dbname="dizzy_lemon_cough_507856",
    user="ut06iabq5us",
    password="qrhGvyvgD3vt",
    host="ep-gentle-mountain-a23bxz6h-pooler.eu-central-1.aws.neon.tech",
    port="5432"
)

cursor = conn.cursor()

# Get the list of all tables
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public';
""")
tables = cursor.fetchall()

# Export each table to JSON
data = {}
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT row_to_json(t) FROM {table_name} t")
    data[table_name] = cursor.fetchall()

# Save to a JSON file
with open('database_backup.json', 'w') as f:
    json.dump(data, f, indent=4)

cursor.close()
conn.close()