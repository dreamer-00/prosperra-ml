import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import warnings
from .categorizer import TransactionCategorizer
warnings.filterwarnings("ignore")
class ProsperraMLEngine:
    def __init__(self):
        self.model = KMeans(n_clusters=3, random_state=42, n_init=10)
        self.cluster_allocations = {
            0: {"Profile": "Conservative", "Equity_ETF": 0.30, "Digital_Gold": 0.40, "Liquid_Debt": 0.30},
            1: {"Profile": "Aggressive", "Equity_ETF": 0.70, "Digital_Gold": 0.20, "Liquid_Debt": 0.10},
            2: {"Profile": "Balanced", "Equity_ETF": 0.50, "Digital_Gold": 0.30, "Liquid_Debt": 0.20}
        }
    def train_model(self):
        historical_training_data = np.array([
            [150.0, 0.15, 4.0],  # User A (Conservative)
            [850.0, 0.80, 25.0], # User B (Aggressive)
            [400.0, 0.45, 12.0], # User C (Balanced)
            [100.0, 0.10, 3.0],  # User D (Conservative)
            [900.0, 0.85, 28.0]  # User E (Aggressive)
        ])
        self.model.fit(historical_training_data)
    def analyze_user_behavior(self, transactions_df):
        cat_engine = TransactionCategorizer()
        
        total_spare_change = 0
        luxury_spend = 0
        total_spend = 0
        frequency = len(transactions_df)
        for _, row in transactions_df.iterrows():
            desc = row['description']
            amount = float(row['amount'])
            
            category = cat_engine.predict_category(desc)
            spare = cat_engine.calculate_roundup(amount)
            
            total_spare_change += spare
            total_spend += amount
            if category in ["Food", "Entertainment", "Shopping", "Travel"]:
                luxury_spend += amount
                
            print(f" ├── [TX] ₹{amount:<6.2f} | Cat: {category:<14} | Round-Up: ₹{spare:.2f}")
        luxury_ratio = luxury_spend / total_spend if total_spend > 0 else 0
        feature_vector = [total_spare_change, luxury_ratio, frequency]     
        return feature_vector, total_spare_change
    def execute_allocation(self, feature_vector, total_spare_change):
        vector_array = np.array(feature_vector).reshape(1, -1)
        cluster_id = int(self.model.predict(vector_array)[0])
        allocation = self.cluster_allocations[cluster_id]
        print("\n" + "="*60)
        print(f"{'ML CLUSTERING & ASSET ALLOCATION':^60}")
        print("="*60)
        print(f"User Behavioral Vector : [Spare: ₹{feature_vector[0]:.2f}, Lux Ratio: {feature_vector[1]:.2f}, Freq: {feature_vector[2]}]")
        print(f"ML Cluster Assigned    : {cluster_id} ({allocation['Profile']} Profile)")
        print("-" * 60)
        print(f"Total Investable Capital: ₹{total_spare_change:.2f}")
        print(f" 🟢 Equity ETF (Nifty50) : ₹{(total_spare_change * allocation['Equity_ETF']):.2f} ({allocation['Equity_ETF']*100}%)")
        print(f" 🟡 Digital Gold 24K     : ₹{(total_spare_change * allocation['Digital_Gold']):.2f} ({allocation['Digital_Gold']*100}%)")
        print(f" 🔵 Liquid Debt Funds    : ₹{(total_spare_change * allocation['Liquid_Debt']):.2f} ({allocation['Liquid_Debt']*100}%)")
        print("="*60 + "\n")
if __name__ == "__main__":
    mock_data = {
        "description": ["Uber Ride to Office", "Zomato Lunch", "Blinkit Groceries", "Netflix Sub", "Starbucks Coffee"],
        "amount": [245.50, 432.00, 891.20, 199.00, 315.50]
    }
    df = pd.DataFrame(mock_data)
    engine = ProsperraMLEngine()
    engine.train_model() 
    user_features, investable_capital = engine.analyze_user_behavior(df)
    engine.execute_allocation(user_features, investable_capital)