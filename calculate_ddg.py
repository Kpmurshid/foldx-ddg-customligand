import csv
import os
import matplotlib.pyplot as plt
import numpy as np

# File list and paths
mutation_list_file = "individual_list.txt"
results_dir = "AnalyseComplex_Results"  
output_csv = os.path.join(os.getcwd(), "mutation_ddg_results.csv")  

# Load mutation labels
with open(mutation_list_file) as f:
    mutation_lines = [line.strip().strip(';') for line in f if line.strip()]

def format_mutation_label(raw_label):
    return f"{raw_label[1]}{raw_label[2:-1]}{raw_label[-1]}"

def extract_interaction_energy(filepath):
    with open(filepath) as f:
        for line in f:
            if line.startswith("./"):
                return float(line.split()[5])

def extract_total_stability(filepath):
    with open(filepath) as f:
        for line in f:
            if line.startswith("./"):
                parts = line.split()
                return float(parts[6]) + float(parts[7])

mutation_data = []

for i, raw_mutation in enumerate(mutation_lines, start=1):
    mutation_label = format_mutation_label(raw_mutation)

    interaction_wt_file = os.path.join(results_dir, f"Interaction_WT_complex_repaired_{i}_AC.fxout")
    interaction_mut_file = os.path.join(results_dir, f"Interaction_complex_repaired_{i}_AC.fxout")
    summary_wt_file = os.path.join(results_dir, f"Summary_WT_complex_repaired_{i}_AC.fxout")
    summary_mut_file = os.path.join(results_dir, f"Summary_complex_repaired_{i}_AC.fxout")

    try:
        interaction_energy_wt = extract_interaction_energy(interaction_wt_file)
        interaction_energy_mut = extract_interaction_energy(interaction_mut_file)
        ddg_binding = interaction_energy_mut - interaction_energy_wt

        stability_wt = extract_total_stability(summary_wt_file)
        stability_mut = extract_total_stability(summary_mut_file)
        ddg_stability = stability_mut - stability_wt

        print(f"{mutation_label}\tΔΔG_binding = {ddg_binding:.3f}, ΔΔG_stability = {ddg_stability:.3f}")
        mutation_data.append([mutation_label, f"{ddg_binding:.3f}", f"{ddg_stability:.3f}"])

    except Exception as e:
        print(f"Error processing mutation {i} ({mutation_label}): {e}")

# Save results to CSV in current directory
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Mutation", "ΔΔG_binding", "ΔΔG_stability"])
    writer.writerows(mutation_data)

print(f"\n All results saved to {output_csv}")

# Plotting
mutations = [row[0] for row in mutation_data]
ddg_binding_vals = [float(row[1]) for row in mutation_data]
ddg_stability_vals = [float(row[2]) for row in mutation_data]

x = np.arange(len(mutations))
width = 0.35

plt.figure(figsize=(12, 6))
bars1 = plt.bar(x - width/2, ddg_binding_vals, width=width, label="ΔΔG_binding", color="#1f77b4")
bars2 = plt.bar(x + width/2, ddg_stability_vals, width=width, label="ΔΔG_stability", color="#ff7f0e")

def annotate_bars(bars):
    for bar in bars:
        height = bar.get_height()
        plt.annotate(f'{height:.3f}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 4),
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=8)

annotate_bars(bars1)
annotate_bars(bars2)

y_min = min(ddg_binding_vals + ddg_stability_vals)
y_max = max(ddg_binding_vals + ddg_stability_vals)
plt.yticks(np.arange(np.floor(y_min) - 0.25, np.ceil(y_max) + 0.25, 0.25))

plt.xlabel("Mutation")
plt.ylabel("ΔΔG (kcal/mol)")
plt.title("ΔΔG Binding vs Stability for Each Mutation")
plt.xticks(ticks=x, labels=mutations, rotation=45, ha="right")
plt.legend()
plt.tight_layout()

# Save plot to current directory
plot_path = os.path.join(os.getcwd(), "mutation_ddg_plot.png")
plt.savefig(plot_path)
plt.show()

print(f"Plot saved to {plot_path}")

