import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Generating EDA Scatter Plot for Chapter 4...")

# 1. Load the dataset
try:
    data = pd.read_csv('thermal_data.csv')
except FileNotFoundError:
    print("[ERROR] thermal_data.csv not found. Please run the hardware data logger first.")
    exit()

# 2. Map the numeric labels to readable names for the graph legend
state_mapping = {0: 'Pre-heating (Cold)', 1: 'Optimal Extraction', 2: 'Overheating (Danger)'}
data['State_Name'] = data['State_Label'].map(state_mapping)

# 3. Setup the visual style
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

# 4. Generate the Scatter Plot
# X-axis = Nozzle Temp, Y-axis = Ambient PCB Temp, Color = Machine State
scatter = sns.scatterplot(
    data=data, 
    x='Nozzle_Temp', 
    y='Ambient_Temp', 
    hue='State_Name',
    palette=['blue', 'green', 'red'], # Blue=Cold, Green=Optimal, Red=Hot
    s=100, # Marker size
    alpha=0.8 # Slight transparency to show overlapping data points
)

# 5. Format the Graph for your Manuscript
plt.title("Cyber-Physical Thermal Distribution: Cashew Expeller Nozzle vs Ambient PCB", fontsize=14, fontweight='bold')
plt.xlabel("Nozzle Temperature (°C)", fontsize=12)
plt.ylabel("GY-906 Ambient PCB Temperature (°C)", fontsize=12)
plt.axhline(y=85, color='black', linestyle='--', label='Critical PCB Failure Limit (85°C)')

# Move legend outside the plot area
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# 6. Save as a high-res PNG for your thesis
output_filename = 'thermal_scatter_plot.png'
plt.savefig(output_filename, dpi=300)
print(f"Success! Graph saved as {output_filename}")
plt.show()
