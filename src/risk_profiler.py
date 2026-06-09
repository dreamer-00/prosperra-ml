import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib
import os

class RiskProfiler:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = KMeans(n_clusters=3, random_state=42, n_init=10)
        self.is_trained = False
        self.profile_map = {}

    def generate_training_data(self):
        # Synthetic but realistic user profiles
        # Features: [total_spare_change, luxury_ratio, frequency]
        np.random.seed(42)

        # Conservative users — low spare change, low luxury, low frequency
        conservative = np.random.normal(
            loc=[150, 0.15, 4], 
            scale=[30, 0.05, 1], 
            size=(100, 3)
        )

        # Balanced users — medium everything
        balanced = np.random.normal(
            loc=[400, 0.45, 12], 
            scale=[50, 0.08, 2], 
            size=(100, 3)
        )

        # Aggressive users — high spare change, high luxury, high frequency
        aggressive = np.random.normal(
            loc=[850, 0.80, 25], 
            scale=[80, 0.05, 3], 
            size=(100, 3)
        )

        return np.vstack([conservative, balanced, aggressive])

    def train(self):
        print("Generating training data...")
        X = self.generate_training_data()

        print("Scaling features...")
        X_scaled = self.scaler.fit_transform(X)

        print("Training K-means clustering...")
        self.model.fit(X_scaled)

        # Figure out which cluster is which profile
        # by looking at cluster centers
        centers = self.scaler.inverse_transform(
            self.model.cluster_centers_
        )

        # Sort clusters by luxury_ratio (feature index 1)
        # Low luxury = Conservative
        # Medium luxury = Balanced  
        # High luxury = Aggressive
        sorted_clusters = np.argsort(centers[:, 1])
        
        self.profile_map = {
            sorted_clusters[0]: "Conservative",
            sorted_clusters[1]: "Balanced",
            sorted_clusters[2]: "Aggressive"
        }

        self.is_trained = True
        print(f"Cluster profiles mapped: {self.profile_map}")

        # Save model
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, 'models/kmeans_model.pkl')
        joblib.dump(self.scaler, 'models/risk_scaler.pkl')
        joblib.dump(self.profile_map, 'models/profile_map.pkl')
        print("Risk profiler saved.")

    def predict(self, spare_change, luxury_ratio, frequency):
        if not self.is_trained:
            raise Exception("Model not trained. Call train() first.")

        features = np.array([[spare_change, luxury_ratio, frequency]])
        features_scaled = self.scaler.transform(features)
        cluster = int(self.model.predict(features_scaled)[0])
        return self.profile_map[cluster]

    def get_allocation(self, profile):
        allocations = {
            "Conservative": {
                "Equity_ETF": 0.20,
                "Digital_Gold": 0.50,
                "Liquid_Debt": 0.30
            },
            "Balanced": {
                "Equity_ETF": 0.50,
                "Digital_Gold": 0.30,
                "Liquid_Debt": 0.20
            },
            "Aggressive": {
                "Equity_ETF": 0.70,
                "Digital_Gold": 0.20,
                "Liquid_Debt": 0.10
            }
        }
        return allocations[profile]