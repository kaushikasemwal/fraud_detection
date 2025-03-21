import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load synthetic data
data = pd.read_csv("synthetic_fraud_data.csv")

# Preprocess data
data["channel"] = data["channel"].map({"Online": 1, "POS": 0, "Mobile": 0, "ATM": 0})
data["mode"] = data["mode"].map({"Credit Card": 1, "Debit Card": 0, "UPI": 0, "Net Banking": 0})
data["bank_code"] = data["bank_code"].map({"Bank A": 1, "Bank B": 0, "Bank C": 0, "Bank D": 0})

# Features and target
X = data[["amount", "channel", "mode", "bank_code"]]
y = data["is_fraud"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, "fraud_model.pkl")
print("Model saved as 'fraud_model.pkl'.")