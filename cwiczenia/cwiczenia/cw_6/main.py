import sqlite3 
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
#cursor.execute('''DROP TABLE test''')
cursor.execute('''CREATE TABLE test (id integer, name text, value real)''')

cursor.execute('''Insert into test values (1, 'test', 1.3)''')

for row in cursor.execute('Select * from test'):
    print(row)
print("111")
conn.commit()
conn.close()