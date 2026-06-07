categories = {
    "Zomato" : "Food",
    "Swiggy" : "Food",
    "Uber" : "Travel",
    "IRCTC" : "Travel",
    "Amazon" : "Shopping"
}
def categorize(description):
    return categories.get(description, "Other")

