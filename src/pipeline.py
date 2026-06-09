import pandas as pd
from .categorizer import TransactionCategorizer
from .risk_profiler import RiskProfiler

class KubyraMLPipeline:
    def __init__(self):
        self.categorizer = TransactionCategorizer()
        self.risk_profiler = RiskProfiler()

    def train(self):
        self.risk_profiler.train()

    def process_transactions(self, transactions_df):
        results = []
        total_spare = 0
        total_spend = 0
        luxury_spend = 0

        luxury_categories = [
            "Food", "Entertainment", 
            "Shopping", "Travel"
        ]

        print("\n" + "="*60)
        print(f"{'KUBYRA — TRANSACTION ANALYSIS':^60}")
        print("="*60)

        for _, row in transactions_df.iterrows():
            description = row['description']
            amount = float(row['amount'])

            # Step 1 — Categorize
            category = self.categorizer.predict_category(
                description
            )

            # Step 2 — Round up
            spare = self.categorizer.calculate_roundup(amount)

            total_spare += spare
            total_spend += amount

            if category in luxury_categories:
                luxury_spend += amount

            results.append({
                "description": description,
                "amount": amount,
                "category": category,
                "spare_change": spare
            })

            print(
                f"  {description:<20} | "
                f"₹{amount:<8.2f} | "
                f"{category:<15} | "
                f"Round-up: ₹{spare:.2f}"
            )

        # Step 3 — Calculate behavioral features
        luxury_ratio = (
            luxury_spend / total_spend 
            if total_spend > 0 else 0
        )
        frequency = len(transactions_df)

        print(f"\nTotal Spare Change: ₹{total_spare:.2f}")
        print(f"Luxury Ratio: {luxury_ratio:.2f}")
        print(f"Transaction Frequency: {frequency}")

        # Step 4 — Risk profile
        profile = self.risk_profiler.predict(
            total_spare, luxury_ratio, frequency
        )

        # Step 5 — Allocation
        allocation = self.risk_profiler.get_allocation(profile)

        print("\n" + "="*60)
        print(f"{'RISK PROFILE & ALLOCATION':^60}")
        print("="*60)
        print(f"Risk Profile: {profile}")
        print(f"\nInvestable Capital: ₹{total_spare:.2f}")
        print(
            f"  Equity ETF    : "
            f"₹{total_spare * allocation['Equity_ETF']:.2f} "
            f"({allocation['Equity_ETF']*100:.0f}%)"
        )
        print(
            f"  Digital Gold  : "
            f"₹{total_spare * allocation['Digital_Gold']:.2f} "
            f"({allocation['Digital_Gold']*100:.0f}%)"
        )
        print(
            f"  Liquid Debt   : "
            f"₹{total_spare * allocation['Liquid_Debt']:.2f} "
            f"({allocation['Liquid_Debt']*100:.0f}%)"
        )
        print("="*60)

        return results, profile, allocation, total_spare