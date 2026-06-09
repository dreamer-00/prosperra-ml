import pandas as pd

class TransactionCategorizer:
    def __init__(self):
        self.keyword_map = {
            "zomato": "Food", "swiggy": "Food", "mcdonalds": "Food", "starbucks": "Food",
            "uber": "Travel", "ola": "Travel", "irctc": "Travel", "makemytrip": "Travel",
            "amazon": "Shopping", "flipkart": "Shopping", "myntra": "Shopping",
            "jio": "Bills", "airtel": "Bills", "bescom": "Bills", "netflix": "Entertainment",
            "blinkit": "Grocery", "zepto": "Grocery", "dmart": "Grocery", "apollo": "Medical", "phonepe": "Bills", "bigbasket" : "Grocery"
        }
    
    def predict_category(self, description: str) -> str:
        desc_lower = str(description).lower()
        for keyword, category in self.keyword_map.items():
            if keyword in desc_lower:
                return category
        return "Miscellaneous" 
    def calculate_roundup(self, amount: float) -> float:
        import math
        ceiling_10 = math.ceil(amount / 10.0) * 10
        spare = ceiling_10 - amount
        return 10.00 if spare == 0 else round(spare, 2)