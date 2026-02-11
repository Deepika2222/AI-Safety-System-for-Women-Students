import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import DBSCAN
from sklearn.metrics import mean_squared_error
import joblib

# 1. Load dataset
df = pd.read_csv("/Users/deepika/Documents/PROJECTS/AI-Safety-System-for-Women-Students/ml_engine/training/data/crime_dataset.csv")

# 2. Keep required columns
df = df[['Primary Type','Location Description','Arrest','Domestic',
         'Latitude','Longitude','Date']]

# 3. Clean data
df = df.dropna(subset=['Latitude','Longitude'])
df['Location Description'] = df['Location Description'].fillna("UNKNOWN")

# 4. Time features
df['Date'] = pd.to_datetime(df['Date'], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
df['hour'] = df['Date'].dt.hour
df['day'] = df['Date'].dt.dayofweek

# 5. Encode categories
df['crime_enc'] = LabelEncoder().fit_transform(df['Primary Type'])
df['loc_enc'] = LabelEncoder().fit_transform(df['Location Description'])
df['Arrest'] = df['Arrest'].astype(int)
df['Domestic'] = df['Domestic'].astype(int)

# 6. Create risk label using spatial clustering
coords = df[['Latitude','Longitude']].values
db = DBSCAN(eps=0.002, min_samples=10).fit(coords)
df['cluster'] = db.labels_

density = df.groupby('cluster').size()
df['crime_density'] = df['cluster'].map(density)

scaler = MinMaxScaler()
df['risk_score'] = scaler.fit_transform(df[['crime_density']])

# 7. Features + target
X = df[['Latitude','Longitude','hour','day','crime_enc','loc_enc','Arrest','Domestic']]
y = df['risk_score']

# 8. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 9. Train model
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# 10. Evaluate
pred = model.predict(X_test)
print("MSE:", mean_squared_error(y_test, pred))

# 11. Save model
joblib.dump(model, "risk_model.pkl")
print("Saved as risk_model.pkl")
