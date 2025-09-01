import sqlite3

def create_db():
    """
    Creates and populates the SQLite database for the application.
    """
    conn = sqlite3.connect('allotment.db')
    cursor = conn.cursor()

    # Drop tables if they already exist to ensure a clean start
    cursor.execute("DROP TABLE IF EXISTS teachers")
    cursor.execute("DROP TABLE IF EXISTS rooms")

    # Create the teachers table
    cursor.execute('''
        CREATE TABLE teachers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')

    # Create the rooms table
    cursor.execute('''
        CREATE TABLE rooms (
            id INTEGER PRIMARY KEY,
            room_number TEXT NOT NULL
        )
    ''')

    # Sample data for teachers and rooms
    sample_teachers = [
        ('Mr. Sharma',), ('Ms. Khan',), ('Mrs. Gupta',), ('Mr. Singh',),
        ('Ms. Reddy',), ('Mr. Varma',), ('Ms. Das',), ('Mr. Rajan',)
    ]
    sample_rooms = [
        ('A101',), ('A102',), ('B201',), ('B202',), ('C301',), ('C302',)
    ]

    # Insert sample data into the tables
    cursor.executemany("INSERT INTO teachers (name) VALUES (?)", sample_teachers)
    cursor.executemany("INSERT INTO rooms (room_number) VALUES (?)", sample_rooms)

    conn.commit()
    conn.close()
    print("Database 'allotment.db' created and populated successfully.")

if __name__ == '__main__':
    create_db()
