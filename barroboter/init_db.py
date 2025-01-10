import sqlite3

def init_db():
    """
    Initialize the database with the necessary tables.
    """
    conn = sqlite3.connect('barrobot.db')
    cursor = conn.cursor()

    # Create cocktails table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cocktails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        total_volumes TEXT NOT NULL,
        pour_times TEXT NOT NULL,
        image_url TEXT NOT NULL
    )
    ''')

    # Create positions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position INTEGER NOT NULL,
        liquid TEXT NOT NULL,
        steps INTEGER NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
