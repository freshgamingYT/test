import sqlite3

def view_db():
    """
    View all data in the cocktails and positions tables.
    """
    conn = sqlite3.connect('barrobot.db')
    cursor = conn.cursor()

    # View cocktails table
    cursor.execute('SELECT * FROM cocktails')
    cocktails = cursor.fetchall()
    print("Cocktails Table:")
    for row in cocktails:
        print(row)

    # View positions table
    cursor.execute('SELECT * FROM positions')
    positions = cursor.fetchall()
    print("\nPositions Table:")
    for row in positions:
        print(row)

    conn.close()

if __name__ == '__main__':
    view_db()
