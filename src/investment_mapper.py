mapping = {
    "Food" : "Liquid Mutual Fund",
    "Travel" : "Gold ETF",
    "Shopping" : "Index Fund",
    "Other" : "Liquid Mutual Fund"
}

def assign_investment(category):
    return mapping.get(category, "Liquid Mutual Fund")

