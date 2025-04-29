import sqlite3

conn = sqlite3.connect('de_en.db')
cursor = conn.cursor()


# 3. Drop old table
cursor.execute("DROP TABLE grammar")



conn.commit()
conn.close()
