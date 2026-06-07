from src.categorizer import categorize
from src.roundup import round_up
from src.investment_mapper import assign_investment
import csv

transactions = []
with open("data/sample_transactions.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        transactions.append({
            "description": row["description"],
            "amount": float(row["amount"])
        })
total_invested = 0
print("=" * 55)
print(f"{'PROSPERRA - Transaction Analysis':^55}")
print("=" * 55)

for t in transactions:
    cat =  categorize(t["description"])
    spare = round_up(t["amount"])
    invest = assign_investment(cat)
    total_invested += spare
    print(f"\nTransaction : {t['description']}")
    print(f"\nAmount : ₹{t['amount']:.2f}")
    print(f"\nCategory : {cat}")
    print(f"\nRound-up : ₹{spare:.2f}")
    print(f"\nInvested in : {invest}")

print("\n" + "=" * 55)
print(f"Total Spare Change Invested: ₹{round(total_invested, 2)}")
print("=" * 55)
