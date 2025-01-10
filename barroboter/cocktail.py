import json

class Cocktail:
    def __init__(self):
        self.cocktails = self.get_all_cocktails()

    def get_all_cocktails(self):
        try:
            with open('data.json', 'r') as json_file:
                data = json.load(json_file)
            return [cocktail['name'] for cocktail in data['cocktails']]
        except Exception as e:
            print(f"Error retrieving cocktails: {e}")
            return []

    def select(self, cocktail):
        try:
            with open('data.json', 'r') as json_file:
                data = json.load(json_file)
            cocktail_data = next((c for c in data['cocktails'] if c['name'] == cocktail), None)
            if cocktail_data:
                return cocktail_data
            else:
                return "Cocktail not found", 404
        except Exception as e:
            print(f"Error selecting cocktail: {e}")
            return "Internal Server Error", 500
