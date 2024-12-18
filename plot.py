#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import glob

# Function to clean and process each month's data
def process_file(file_path):
    with open(file_path, 'r') as file:
        raw_lines = file.readlines()

    # Extract relevant lines (skip headers, start from row 3)
    data_lines = raw_lines[3:]

    # Parse the lines into structured data
    cleaned_data = []
    for line in data_lines:
        line_split = line.strip().split(",")
        if len(line_split) >= 7:  # Ensure there are enough columns
            year, month, day = line_split[0].strip('"'), line_split[1].strip('"'), line_split[2].strip('"')
            sunrise, sunset = line_split[4].strip('"'), line_split[6].strip('"')
            cleaned_data.append([year, month, day, sunrise, sunset])

    # Convert to DataFrame
    month_data = pd.DataFrame(cleaned_data, columns=["Year", "Month", "Day", "Sunrise", "Sunset"])

    # Combine Year, Month, and Day into a single datetime column
    month_data["Date"] = pd.to_datetime(month_data[["Year", "Month", "Day"]])

    # Convert Sunrise and Sunset to datetime.time
    month_data["Sunrise"] = pd.to_datetime(month_data["Sunrise"], format="%H:%M").dt.time
    month_data["Sunset"] = pd.to_datetime(month_data["Sunset"], format="%H:%M").dt.time

    # Calculate day length in hours
    month_data["Day Length"] = (
        pd.to_datetime(month_data["Sunset"].astype(str)) - 
        pd.to_datetime(month_data["Sunrise"].astype(str))
    ).dt.total_seconds() / 3600

    # Add day of year column
    month_data["Day of Year"] = month_data["Date"].dt.dayofyear

    return month_data

# Main script
all_data = pd.DataFrame()

# Read and process all files from 01.csv to 12.csv
for month in range(1, 13):
    file_path = f"{month:02}.csv"
    month_data = process_file(file_path)
    all_data = pd.concat([all_data, month_data], ignore_index=True)

# Sort by day of year
all_data = all_data.sort_values("Day of Year")

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(all_data["Day of Year"], all_data["Day Length"], label="Day Length", color="blue")
plt.title("Day Length Throughout the Year in London")
plt.xlabel("Day of the Year")
plt.ylabel("Day Length (hours)")
plt.grid(True)
plt.legend()

# Save the plot to a PNG file
plt.savefig("day_length_plot.png")
plt.show()

print("Plot saved as 'day_length_plot.png'.")

