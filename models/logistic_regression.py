import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
df = pd.read_csv('data/Credit card transactions - India - Simple.csv')
df = df.dropna()
#features
le_city = LabelEncoder()
le_card = LabelEncoder()
le_gender = LabelEncoder()
le_target = LabelEncoder()

df['City_encoded'] = le_city.fit_transform(df['City'])
df['Card_encoded'] = le_card.fit_transform(df['Card Type'])
df['Gender_encoded'] = le_gender.fit_transform(df['Gender'])
df['Target'] = le_target.fit_transform(df['Exp Type'])

X = df[['City_encoded', 'Card_encoded', 'Gender_encoded', 'Amount']]
y = df['Target']

print(f"Features shape: {X.shape}")
print(f"Categories: {le_target.classes_}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

print("\nTraining Logistic Regression...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {accuracy:.2%}")
print("\nDetailed Report:")
print(classification_report(y_test, y_pred,
      target_names=le_target.classes_,
      zero_division=0))

print("\nSaving model...")
os.makedirs('models', exist_ok=True)

joblib.dump(model, 'models/transaction_classifier.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(le_city, 'models/le_city.pkl')
joblib.dump(le_card, 'models/le_card.pkl')
joblib.dump(le_gender, 'models/le_gender.pkl')
joblib.dump(le_target, 'models/le_target.pkl')

print("Model saved successfully.")