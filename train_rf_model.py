import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

print("========================================")
print("CNSL Expeller: Random Forest Training")
print("========================================")

# 1. Load the physical dataset
try:
    data = pd.read_csv('thermal_data.csv')
    print(f"Dataset loaded successfully. Total data points: {len(data)}")
except FileNotFoundError:
    print("[ERROR] thermal_data.csv not found! Run your Arduino data logger first.")
    exit()

# 2. Define Features (X) and Target (y)
X = data[['Nozzle_Temp', 'Ambient_Temp']]
y = data['State_Label']

# 3. Split into 80% Training and 20% Testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Initialize the Cyber-Physical AI
# n_estimators=100 (Builds 100 decision trees)
# max_depth=5 (Prevents the model from overfitting to noisy sensor data)
rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)

print("\nTraining the Random Forest model...")
rf_model.fit(X_train, y_train)

# 5. Evaluate the Model (Crucial for your defense documentation)
predictions = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("\n--- Model Performance Metrics ---")
print(f"Overall Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, predictions, target_names=["Pre-heating (0)", "Optimal (1)", "Overheat (2)"]))

# Feature Importance (Tells you which sensor reading mattered most)
importances = rf_model.feature_importances_
print(f"Feature Importance -> Nozzle Temp: {importances[0]*100:.1f}%, Ambient Temp: {importances[1]*100:.1f}%")

# 6. Export the trained brain
joblib.dump(rf_model, 'expeller_rf_model.pkl')
print("\n[SUCCESS] Model saved as 'expeller_rf_model.pkl'. Transfer this file to your Raspberry Pi.")
