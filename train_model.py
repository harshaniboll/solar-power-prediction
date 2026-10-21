
import os
import pickle
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load datasets
generation = pd.read_csv("data/Plant_1_Generation_Data.csv")
weather = pd.read_csv("data/Plant_1_Weather_Sensor_Data.csv")

# Convert timestamps
generation["DATE_TIME"] = pd.to_datetime(
    generation["DATE_TIME"], format="%d-%m-%Y %H:%M"
)
weather["DATE_TIME"] = pd.to_datetime(
    weather["DATE_TIME"], format="%Y-%m-%d %H:%M:%S"
)

# Combine the power output of all inverters at each timestamp
generation = generation.groupby("DATE_TIME", as_index=False)["AC_POWER"].sum()

# Keep one weather record per timestamp
weather = weather.groupby("DATE_TIME", as_index=False)[
    ["AMBIENT_TEMPERATURE", "MODULE_TEMPERATURE", "IRRADIATION"]
].mean()

# Merge generation and weather data
df = pd.merge(generation, weather, on="DATE_TIME", how="inner")

# Create time-based features
df["HOUR"] = df["DATE_TIME"].dt.hour
df["MONTH"] = df["DATE_TIME"].dt.month

features = [
    "AMBIENT_TEMPERATURE",
    "MODULE_TEMPERATURE",
    "IRRADIATION",
    "HOUR",
    "MONTH"
]

X = df[features]
y = df["AC_POWER"]

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train the model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)

print("Dataset rows after merging:", len(df))
print("Training completed successfully!")
print(f"MAE: {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R² Score: {r2:.4f}")

# Save the trained model
os.makedirs("model", exist_ok=True)

with open("model/solar_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model saved to model/solar_model.pkl")

