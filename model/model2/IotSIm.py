import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_hourly_data(seeding_date, harvesting_date, crop_id):
    start_date = datetime.strptime(seeding_date, "%Y-%m-%d")
    end_date = datetime.strptime(harvesting_date, "%Y-%m-%d")
    total_days = (end_date - start_date).days + 1

    records = []

    for day in range(total_days):
        current_date = start_date + timedelta(days=day)
        for hour in range(24):
            period = "Day" if 6 <= hour < 18 else "Night"

            # Simulate values based on time of day
            if period == "Day":
                temp = round(np.random.uniform(22, 26), 1)
                humidity = round(np.random.uniform(60, 70), 1)
                co2 = round(np.random.uniform(1000, 1200), 1)
                light = round(np.random.uniform(10000, 20000), 0)
            else:
                temp = round(np.random.uniform(16, 20), 1)
                humidity = round(np.random.uniform(65, 75), 1)
                co2 = round(np.random.uniform(800, 1000), 1)
                light = round(np.random.uniform(0, 500), 0)

            soil_moisture = round(np.random.uniform(60, 80), 1)

            records.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Hour": hour,
                "Period": period,
                "Temperature_°C": temp,
                "Humidity_%": humidity,
                "CO₂_ppm": co2,
                "Soil_Moisture_%": soil_moisture,
                "Light_lux": light,
                "Crop_ID": crop_id
            })

    return pd.DataFrame(records)

# --- Main block: Generate dataset for multiple crops ---
crop_cycles = [
    {"Seeding_Date": "2025-01-01", "Harvesting_Date": "2025-03-25", "Crop_ID": "T001"},
    {"Seeding_Date": "2025-02-15", "Harvesting_Date": "2025-05-10", "Crop_ID": "T002"},
]

all_data = pd.DataFrame()

for cycle in crop_cycles:
    df = generate_hourly_data(cycle["Seeding_Date"], cycle["Harvesting_Date"], cycle["Crop_ID"])
    all_data = pd.concat([all_data, df], ignore_index=True)

# --- Save to CSV ---
all_data.to_csv("tomato_greenhouse_hourly_data.csv", index=False)
print("✅ Dataset saved as 'tomato_greenhouse_hourly_data.csv'")
