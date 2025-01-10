import sqlite3

def init_db():
    try:
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

        # Insert initial positions
        positions = [
            ('pos0', 0, 'None', 0),
            ('pos1', 1, 'None', 450),
            ('pos2', 2, 'None', 900),
            ('pos3', 3, 'None', 1350),
            ('pos4', 4, 'None', 1800),
            ('pos5', 5, 'None', 2250),
            ('pos6', 6, 'None', 2700),
            ('pos7', 7, 'None', 3150),
            ('pos8', 8, 'None', 3600),
            ('pos9', 9, 'None', 4050)
        ]
        cursor.executemany('''
        INSERT INTO positions (name, position, liquid, steps)
        VALUES (?, ?, ?, ?)
        ''', positions)

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == '__main__':
    init_db()
