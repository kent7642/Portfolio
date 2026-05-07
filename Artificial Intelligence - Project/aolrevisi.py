import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pygame
import os

pygame.mixer.init()

QUALITY_THRESHOLDS = {
    "pristine": {
        "color": "green",
        "sound": None,
        "condition": "PRISTINE",
        "explanation": ""
    },
    "safe": {
        "color": "blue",
        "sound": None,
        "condition": "SAFE",
        "explanation": ""
    },
    "concerning": {
        "color": "yellow",
        "sound": None,
        "condition": "CONCERNING",
        "explanation": "Monitor closely due to elevated risk factors."
    },
    "hazardous": {
        "color": "red",
        "sound": "hazardoussound.wav",  
        "condition": "HAZARDOUS",
        "explanation": "Immediate action needed due to dangerous water conditions."
    },
    "toxic": {
        "color": "black",
        "sound": "toxicsound.wav",  
        "condition": "TOXIC",
        "explanation": "Water is extremely harmful. Avoid all contact."
    }
}

PRISTINE_VALUES = {
    "pH": 7.5,
    "DO": 6,
    "Microbial Contamination": 50,
    "Turbidity": 5,
    "Ammonia": 0.5,
    "Nitrates": 2,
    "Heavy Metals": 0.01,
    "TDS": 300
}

def classify_water_quality(data_row):
    pH, dissolved_oxygen, microbial, turbidity, ammonia, nitrates, heavy_metals, tds = (
        data_row["pH"],
        data_row["DO"],
        data_row["Microbial Contamination"],
        data_row["Turbidity"],
        data_row["Ammonia"],
        data_row["Nitrates"],
        data_row["Heavy Metals"],
        data_row["TDS"]
    )
    
    if (pH < 2 or pH > 12.5 or
        dissolved_oxygen < 1 or
        microbial > 1000 or
        turbidity > 30 or
        ammonia > 3 or
        nitrates > 15 or
        heavy_metals > 0.1 or
        tds > 1500):
        return "toxic"
    
    elif (2 <= pH < 5 or 10 < pH <= 12.5 or
          1 <= dissolved_oxygen < 3 or
          500 <= microbial <= 1000 or
          20 <= turbidity <= 30 or
          2 <= ammonia <= 3 or
          10 <= nitrates <= 15 or
          0.05 <= heavy_metals <= 0.1 or
          1000 <= tds <= 1500):
        return "hazardous"
    
    elif (5 <= pH < 6 or 9 < pH <= 10 or
          3 <= dissolved_oxygen < 4 or
          100 < microbial <= 500 or
          10 <= turbidity < 20 or
          1 <= ammonia < 2 or
          5 <= nitrates < 10 or
          0.02 <= heavy_metals < 0.05 or
          500 < tds <= 1000):
        return "concerning"
    
    elif (6 <= pH <= 9 and
          4 <= dissolved_oxygen <= 6 and
          50 <= microbial <= 100 and
          5 <= turbidity <= 10 and
          0.5 <= ammonia <= 1 and
          2 <= nitrates <= 5 and
          0.01 <= heavy_metals <= 0.02 and
          300 <= tds <= 500):
        return "safe"
    
    elif (6.5 <= pH <= 8.5 and
          dissolved_oxygen > 6 and
          microbial < 50 and
          turbidity < 5 and
          ammonia < 0.5 and
          nitrates < 2 and
          heavy_metals < 0.01 and
          tds < 300):
        return "pristine"
    
    else:
        return "toxic"

def play_quality_sound(quality):
    sound_path = QUALITY_THRESHOLDS[quality]["sound"]
    if sound_path and os.path.exists(sound_path):
        try:
            pygame.mixer.music.load(sound_path)  
            pygame.mixer.music.play()  
        except Exception as e:
            print(f"Error playing sound: {e}")

def load_data(file_path):
    return pd.read_excel(file_path)

def calculate_percentage_deviation(data_row):
    parameters = ["pH", "DO", "Microbial Contamination", "Turbidity", "Ammonia", "Nitrates", "Heavy Metals", "TDS"]
    percentages = []
    for param in parameters:
        pristine_value = PRISTINE_VALUES[param]
        current_value = data_row[param]
        percentage = (current_value / pristine_value) * 100
        percentages.append(percentage)
    return percentages

def update_plot(frame, data, ax, text_box, explanation_box):
    ax.clear()
    current_row = data.iloc[frame]

    parameters = ["pH", "DO", "Microbial Contamination", "Turbidity", "Ammonia", "Nitrates", "Heavy Metals", "TDS"]
    
    percentages = calculate_percentage_deviation(current_row)
    
    quality = classify_water_quality(current_row)
    color = QUALITY_THRESHOLDS[quality]["color"]

    if quality in ["hazardous", "toxic"]:
        play_quality_sound(quality)

    ax.plot(parameters, percentages, color=color, marker='o', linestyle='-', linewidth=2)

    ax.axhline(y=100, color='orange', linestyle='--', label="Pristine (100%)")
    
    ax.set_ylim(0, 2000)

    ax.set_ylabel("Percentage (%)", fontsize=12, labelpad=15)

    ax.set_title(f"Water Quality: {QUALITY_THRESHOLDS[quality]['condition']}", fontsize=16)
    
    explanation = QUALITY_THRESHOLDS[quality]["explanation"]
    if quality in ["concerning", "hazardous", "toxic"]:
        explanation += f"\nFactors: {current_row.to_dict()}"
    explanation_box.set_text(explanation)

def main():
    file_path = "waterqualitydata.xlsx"  
    data = load_data(file_path)

    fig, ax = plt.subplots()
    text_box = plt.figtext(0.5, 0.8, "", wrap=True, horizontalalignment='center', fontsize=12)
    explanation_box = plt.figtext(0.5, 0.02, "", wrap=True, horizontalalignment='center', fontsize=10)

    ani = animation.FuncAnimation(
        fig, update_plot, frames=len(data), fargs=(data, ax, text_box, explanation_box), interval=700
    )

    plt.show()

if __name__ == "__main__":
    main()
