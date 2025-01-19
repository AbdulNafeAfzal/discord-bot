import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("game_data.db")
cursor = conn.cursor()

# Check if the 'inventory' table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print the list of tables in the database
print("Tables in the database:", tables)

# If the 'inventory' table exists, query its content
if ('inventory',) in tables:
    # Query all rows from the inventory table
    cursor.execute("SELECT * FROM inventory;")
    rows = cursor.fetchall()

    # Check if there are any rows in the inventory table
    if rows:
        print("\nInventory Data:")
        for row in rows:
            print(row)
    else:
        print("No data found in the inventory table. Inserting sample data...")

        # Insert sample data into the inventory table
        cursor.execute("""
        INSERT INTO inventory (team, item, quantity)
        VALUES
            ('Mount King', 'item1', 32),
            ('Mount King', 'item2', 44),
            ('Mount King', 'item3', 68),
            ('BFF', 'item1', 12),
            ('BFF', 'item2', 23),
            ('BFF', 'item3', 37)
        """)

        # Commit the changes
        conn.commit()
        print("Sample data inserted successfully!")
else:
    # Create the inventory table if it doesn't exist
    print("Inventory table doesn't exist. Creating table and inserting data...")
    cursor.execute("""
    CREATE TABLE inventory (
        team TEXT,
        item TEXT,
        quantity INTEGER
    )
    """)

    # Insert sample data into the inventory table
    cursor.execute("""
    INSERT INTO inventory (team, item, quantity)
    VALUES
        ('Mount King', 'item1', 32),
        ('Mount King', 'item2', 44),
        ('Mount King', 'item3', 68),
        ('BFF', 'item1', 12),
        ('BFF', 'item2', 23),
        ('BFF', 'item3', 37)
    """)

    # Commit the changes
    conn.commit()
    print("Sample data inserted successfully!")

# Query the table again and print the results
cursor.execute("SELECT * FROM inventory;")
rows = cursor.fetchall()

# Print the data in the inventory table
if rows:
    print("\nInventory Data:")
    for row in rows:
        print(row)
else:
    print("No data found in the inventory table.")

# Close the connection
conn.close()