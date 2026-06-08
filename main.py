import pandas as pd
from src.ml_pipeline import ProsperraMLEngine

try:
    df = pd.read_csv("data/sample_transactions.csv")
    df.columns = [col.lower() for col in df.columns]    
except FileNotFoundError:
    print("[ERROR] Database file data/sample_transactions.csv not found.")
    exit()
engine = ProsperraMLEngine()
engine.train_model()
user_features, investable_capital = engine.analyze_user_behavior(df)
engine.execute_allocation(user_features, investable_capital)