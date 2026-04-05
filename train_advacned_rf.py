import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

print("==================================================")
print("Advanced Pipeline: Feature Engineering")
print("==================================================")

# 1. Load Data
data = pd.read_csv('thermal_data.csv')

# 2. FEATURE ENGINEERING: Calculate the Rate of Change (Delta)
# This measures how fast the nozzle is heating up or cooling down per second.
# It makes the AI predictive rather than just reactive.
print("Engineering thermal velocity features...")
data['Nozzle_Delta'] = data['Nozzle_Temp'].diff().fillna(0)
data['Ambient_Delta'] = data['Ambient_Temp'].diff().fillna(0)

# Define the new, upgraded feature set
X = data[['Nozzle_Temp', 'Ambient_Temp', 'Nozzle_Delta', 'Ambient_Delta']]
y = data['State_Label']

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. HYPERPARAMETER TUNING (GridSearchCV)
print("\nInitiating Grid Search to find the optimal Random Forest architecture...")

# We tell the computer to test all these different combinations
param_grid = {
    'n_estimators': [10, 50, 100, 200],      # How many trees?
    'max_depth': [3, 5, 10, None],           # How deep can the trees think?
    'min_samples_split': [2, 5, 10]          # How strict should the voting be?
}

# Setup the Grid Search
base_rf = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(estimator=base_rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=1)

# Run the massive computation
grid_search.fit(X_train, y_train)

# Extract the absolute best model it found
best_rf_model = grid_search.best_estimator_

print("\n--- Grid Search Complete ---")
print(f"Best Parameters Found: {grid_search.best_params_}")

# 4. Final Evaluation
predictions = best_rf_model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"\nOptimized Model Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, predictions, target_names=["Pre-heating (0)", "Optimal (1)", "Overheat (2)"]))

# Print Feature Importance (Did the Delta actually help?)
importances = best_rf_model.feature_importances_
print("\nFeature Importance:")
print(f" - Nozzle Temp:   {importances[0]*100:.1f}%")
print(f" - Ambient Temp:  {importances[1]*100:.1f}%")
print(f" - Nozzle Delta:  {importances[2]*100:.1f}%")
print(f" - Ambient Delta: {importances[3]*100:.1f}%")

# 5. Export the Final Brain
joblib.dump(best_rf_model, 'expeller_advanced_rf.pkl')
print("\n[SUCCESS] Advanced model saved as 'expeller_advanced_rf.pkl'")
