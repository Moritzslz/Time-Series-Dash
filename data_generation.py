import pandas as pd
import numpy as np

# Define parameters
sampling_rate = 1000  # 1000 datapoints per second
duration_seconds = 10 * 60  # 10 minutes in seconds
total_datapoints = sampling_rate * duration_seconds

# Generate timestamps
timestamps = pd.date_range(start="2024-07-01 00:00:00", periods=total_datapoints, freq="ms")

# Generate sensor readings (e.g., random noise)
noise = 50
sensor_readings = np.random.normal(loc=0, scale=noise, size=total_datapoints)

# Create DataFrame
df = pd.DataFrame({"Timestamp": timestamps, "SensorValue": sensor_readings})

# Save to a CSV file (optional)
df.to_csv("sensor_readings.csv", index=False)

print(df.head())
print(f"Total number of datapoints: {len(df)}")
