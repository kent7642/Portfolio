import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button

# Define thresholds for water quality
QUALITY_THRESHOLDS = {
    "pristine": {"color": "green", "condition": "PRISTINE", "value": 1},
    "safe": {"color": "blue", "condition": "SAFE", "value": 2},
    "concerning": {"color": "yellow", "condition": "CONCERNING", "value": 3},
    "hazardous": {"color": "red", "condition": "HAZARDOUS", "value": 4},
    "toxic": {"color": "black", "condition": "TOXIC", "value": 5}
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

# Plot the trend of water quality on the second page (time-based)
def plot_trend(data, ax_trend):
    # Create a list of water quality classifications (pristine, safe, etc.)
    quality_trend = data.apply(lambda row: QUALITY_THRESHOLDS[classify_water_quality(row)]["value"], axis=1)

    # Time-based x-axis: Assume data has a 'Time' column or use the index for time intervals (e.g., every 5 minutes)
    time_intervals = data.index  # Assuming the index represents time intervals (5 minutes each)

    # Plot the trend of quality values over time
    ax_trend.plot(time_intervals, quality_trend, 
                  color='blue', 
                  label='Water Quality Trend', 
                  linestyle='-', 
                  marker='o', 
                  markersize=6,
                  markerfacecolor='blue',  
                  markeredgecolor='black', 
                  markeredgewidth=2)       # Stroke width around the marker
    
    # Set labels and title
    ax_trend.set_title("Water Quality Trend Over Time", fontsize=16)
    ax_trend.set_ylabel("Water Quality Condition")
    ax_trend.set_xlabel("Time (5-minute Intervals)")
    
    # Map the quality values to their corresponding labels (e.g., Safe, Hazardous, etc.)
    ax_trend.set_yticks([1, 2, 3, 4, 5])
    ax_trend.set_yticklabels(['Pristine', 'Safe', 'Concerning', 'Hazardous', 'Toxic'])
    
    ax_trend.legend(loc="upper left")

# Update plot for animation (for the first page)
def update_plot(frame, data, ax, text_box, explanation_box, y_max_slider):
    ax.clear()
    current_row = data.iloc[frame]

    # Extract parameters for the current time step
    parameters = ["pH", "Dissolved Oxygen", "Microbial Contamination", "Turbidity", "Ammonia", "Nitrates", "Heavy Metals", "TDS"]
    values = current_row[parameters].values
    
    # Classify water quality
    quality = classify_water_quality(current_row)
    color = QUALITY_THRESHOLDS[quality]["color"]

    # Update plot as a line graph
    ax.plot(parameters, values, color=color, marker='o', linestyle='-', linewidth=2)

    # Set the y-axis limits based on the current value from the slider (y_max)
    y_max = y_max_slider.val
    ax.set_ylim(0, y_max)

    # Update the title
    ax.set_title(f"Water Quality: {QUALITY_THRESHOLDS[quality]['condition']}", fontsize=16)
    
    # Update explanation box
    explanation = QUALITY_THRESHOLDS[quality]["condition"]
    explanation_box.set_text(explanation)

# Toggle between pages (subplots)
def toggle_page(event, ax, ax_trend, button, is_first_page):
    if is_first_page:
        ax.set_visible(False)  # Hide the first page (water quality graph)
        ax_trend.set_visible(True)  # Show the second page (trend graph)
        button.label.set_text("Go to Water Quality")  # Update button text
    else:
        ax.set_visible(True)  # Show the first page
        ax_trend.set_visible(False)  # Hide the second page
        button.label.set_text("Go to Trend")  # Update button text
    plt.draw()

# Main function to run the program
def main():
    file_path = "water_quality_data.xlsx"  # Path to your Excel file
    data = load_data(file_path)

    # Create the figure and set up two subplots (pages)
    fig, (ax, ax_trend) = plt.subplots(2, 1, figsize=(10, 12), sharex=True)

    # Create text boxes for both pages
    text_box = plt.figtext(0.5, 0.9, "", wrap=True, horizontalalignment='center', fontsize=12)
    explanation_box = plt.figtext(0.5, 0.02, "", wrap=True, horizontalalignment='center', fontsize=10)

    # Create small circle button to show/hide the slider (circle instead of button)
    ax_button = plt.axes([0.92, 0.85, 0.05, 0.05], facecolor='lightgoldenrodyellow')  # Small button at the top right
    button = Button(ax_button, "Go to Trend", color='lightgoldenrodyellow', hovercolor='gold')
    
    # Create vertical slider for controlling the y_max value (right side of the plot)
    ax_slider = plt.axes([0.94, 0.1, 0.02, 0.3], facecolor='lightgoldenrodyellow')  # Small square size, vertical slider
    y_max_slider = Slider(ax_slider, '', 0, 2000, valinit=2000, valstep=1)

    # Initially hide the slider
    ax_slider.set_visible(False)

    # Plot the trend on the second page
    plot_trend(data, ax_trend)

    # Initially show the first page and hide the second
    ax.set_visible(True)
    ax_trend.set_visible(False)

    # Toggle page event
    button.on_clicked(lambda event: toggle_page(event, ax, ax_trend, button, is_first_page=True))

    # Set up animation for the first page (water quality graph)
    ani = animation.FuncAnimation(
        fig, update_plot, frames=len(data), fargs=(data, ax, text_box, explanation_box, y_max_slider), interval=500
    )

    plt.show()

if __name__ == "__main__":
    main()
