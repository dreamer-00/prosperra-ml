import pandas as pd
from src.pipeline import KubyraMLPipeline

# Load transactions
try:
    df = pd.read_csv("data/sample_transactions.csv")
    df.columns = [col.lower() for col in df.columns]
except FileNotFoundError:
    print("[ERROR] sample_transactions.csv not found.")
    exit()

# Run pipeline
pipeline = KubyraMLPipeline()
pipeline.train()
results, profile, allocation, total_spare = \
    pipeline.process_transactions(df)