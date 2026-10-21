
import pandas as pd
import os

for filename in [
    "Plant_1_Generation_Data.csv",
    "Plant_1_Weather_Sensor_Data.csv"
]:
    path = os.path.join("data", filename)
    df = pd.read_csv(path)

    print("\n" + "=" * 50)
    print("FILE:", filename)
    print("Shape:", df.shape)
    print("COLUMNS:", df.columns.tolist())
    print(df.head(3).to_string(index=False))
