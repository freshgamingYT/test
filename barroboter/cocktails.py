import sqlite3

class Cocktail:
    """
    A class to represent a cocktail and its related operations.
    """

    def __init__(self):
        self.cocktails = ["Mojito", "Martini", "Margarita"]

    def select(self, cocktail):
        """
        Select a cocktail from the database.

        Args:
            cocktail (str): The name of the cocktail.

        Returns:
            dict: A dictionary containing the cocktail details if found.
            tuple: A tuple containing an error message and status code if not found.
        """
        conn = sqlite3.connect('barrobot.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cocktails WHERE name = ?', (cocktail,))
        cocktail_data = cursor.fetchone()
        conn.close()
        if cocktail_data:
            return {
                "name": cocktail_data[1],
                "ingredients": cocktail_data[2],
                "total_volumes": cocktail_data[3],
                "pour_times": cocktail_data[4],
                "image_url": cocktail_data[5]
            }
        else:
            return "Cocktail not found", 404
