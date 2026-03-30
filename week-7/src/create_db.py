import sqlite3

conn = sqlite3.connect("src/data/raw/db.sqlite")
cursor = conn.cursor()

# -------------------------------
# TABLES
# -------------------------------

cursor.execute("""
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE artists (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    artist_id INTEGER,
    amount REAL,
    date TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(artist_id) REFERENCES artists(id)
)
""")

# -------------------------------
# DATA
# -------------------------------

customers = [
    (1, "Alice"),
    (2, "Bob"),
    (3, "Charlie"),
]

artists = [
    (1, "Arijit Singh"),
    (2, "Taylor Swift"),
    (3, "Drake"),
]

sales = [
    (1, 1, 1, 500, "2023-01-10"),
    (2, 2, 2, 700, "2023-02-15"),
    (3, 1, 2, 300, "2023-03-20"),
    (4, 3, 3, 900, "2023-04-05"),
    (5, 2, 1, 400, "2023-05-11"),
    (6, 1, 3, 800, "2023-06-18"),
]

cursor.executemany("INSERT INTO customers VALUES (?, ?)", customers)
cursor.executemany("INSERT INTO artists VALUES (?, ?)", artists)
cursor.executemany("INSERT INTO sales VALUES (?, ?, ?, ?, ?)", sales)

conn.commit()
conn.close()

print("✅ Database created at data/db.sqlite")