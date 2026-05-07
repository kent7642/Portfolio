import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# Define thresholds for water quality
QUALITY_THRESHOLDS = {
    "pristine": {
        "color": "green",
        "condition": "PRISTINE",
        "explanation": ""
    },
    "safe": {
        "color": "blue",
        "condition": "SAFE",
        "explanation": ""
    },
    "concerning": {
        "color": "yellow",
        "condition": "CONCERNING",
        "explanation": "Monitor closely due to elevated risk factors."
    },
    "hazardous": {
        "color": "red",
        "condition": "HAZARDOUS",
        "explanation": "Immediate action needed due to dangerous water conditions."
    },
    "toxic": {
        "color": "black",
        "condition": "TOXIC",
        "explanation": "Water is extremely harmful. Avoid all contact."
    }
}

# Function to classify water quality based on parameters
def classify_water_quality(data_row):
    pH, dissolved_oxygen, microbial, turbidity, ammonia, nitrates, heavy_metals, tds = (
        data_row["pH"],
        data_row["Dissolved Oxygen"],
        data_row["Microbial Contamination"],
        data_row["Turbidity"],
        data_row["Ammonia"],
        data_row["Nitrates"],
        data_row["Heavy Metals"],
        data_row["TDS"]
    )

    # Example thresholds (adjust based on real data or standards)
    if 6.5 <= pH <= 8.5 and dissolved_oxygen >= 6 and microbial <= 50 and turbidity <= 5 and ammonia <= 0.5 and nitrates <= 2 and heavy_metals <= 0.01 and tds <= 300:
        return "pristine"
    elif 6 <= pH <= 9 and dissolved_oxygen >= 4 and microbial <= 100 and turbidity <= 10 and ammonia <= 1 and nitrates <= 5 and heavy_metals <= 0.02 and tds <= 500:
        return "safe"
    elif 5 <= pH <= 10 or dissolved_oxygen < 4 or microbial > 100 or turbidity > 10 or ammonia > 1 or nitrates > 5 or heavy_metals > 0.02 or tds > 500:
        return "concerning"
    elif pH < 5 or pH > 10 or dissolved_oxygen < 3 or microbial > 500 or turbidity > 20 or ammonia > 2 or nitrates > 10 or heavy_metals > 0.05 or tds > 1000:
        return "hazardous"
    else:
        return "toxic"

# Load water quality data from Excel file
def load_data(file_path):
    return pd.read_excel(file_path)

# Update plot for animation
def update_plot(frame, data, ax, text_box, explanation_box):
    ax.clear()
    current_row = data.iloc[frame]

    # Extract parameters for the current time step
    parameters = ["pH", "Dissolved Oxygen", "Microbial Contamination", "Turbidity", "Ammonia", "Nitrates", "Heavy Metals", "TDS"]
    values = current_row[parameters].values
    
    # Classify water quality
    quality = classify_water_quality(current_row)
    color = QUALITY_THRESHOLDS[quality]["color"]

    # Update plot
    ax.bar(parameters, values, color=color)
    ax.set_ylim(0, max(data[parameters].max()))
    ax.set_title(f"Water Quality: {QUALITY_THRESHOLDS[quality]['condition']}", fontsize=16)
    
    # Update explanation
    explanation = QUALITY_THRESHOLDS[quality]["explanation"]
    if quality in ["concerning", "hazardous", "toxic"]:
        explanation += f"\nFactors: {current_row.to_dict()}"
    explanation_box.set_text(explanation)

# Main function to run the program
def main():
    file_path = "water_quality_data.xlsx"  # Path to your Excel file
    data = load_data(file_path)

    fig, ax = plt.subplots()
    text_box = plt.figtext(0.5, 0.8, "", wrap=True, horizontalalignment='center', fontsize=12)
    explanation_box = plt.figtext(0.5, 0.02, "", wrap=True, horizontalalignment='center', fontsize=10)

    # Set up animation
    ani = animation.FuncAnimation(
        fig, update_plot, frames=len(data), fargs=(data, ax, text_box, explanation_box), interval=5000
    )

    plt.show()

if __name__ == "__main__":
    main()
