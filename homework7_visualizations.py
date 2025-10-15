#!/usr/bin/env python3
"""
Homework 7: ANOVA Visualizations
Creates visualizations for the diabetes and blood pressure study
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10

# Data from Problem 12.7
groups = ["Normoglycemic", "Impaired Fasting\nGlucose", "Diabetes"]
groups_short = ["Normoglycemic", "IFG", "Diabetes"]
n = np.array([269, 53, 28])
means = np.array([115, 114, 118])
sds = np.array([13.4, 10.1, 11.6])

# Calculate statistics
N = sum(n)
k = len(groups)
grand_mean = np.sum(n * means) / N
ses = sds / np.sqrt(n)

# ANOVA calculations
df_within = n - 1
ss_within_components = df_within * sds**2
SS_within = np.sum(ss_within_components)
df_within_total = N - k
MSW = SS_within / df_within_total

deviations = means - grand_mean
squared_deviations = deviations**2
ss_between_components = n * squared_deviations
SS_between = np.sum(ss_between_components)
df_between = k - 1
MSB = SS_between / df_between

F_stat = MSB / MSW
p_value = 1 - stats.f.cdf(F_stat, df_between, df_within_total)
F_critical = stats.f.ppf(0.95, df_between, df_within_total)

print("=" * 70)
print("DIABETES AND BLOOD PRESSURE STUDY - VISUALIZATIONS")
print("=" * 70)
print(f"\nF-statistic: {F_stat:.3f}")
print(f"p-value: {p_value:.4f}")
print(f"F-critical (α=0.05): {F_critical:.3f}")
print(f"MSW: {MSW:.2f}")
print(f"MSB: {MSB:.2f}")
print(f"Grand mean: {grand_mean:.2f}")

# Create figure with subplots
fig = plt.figure(figsize=(16, 10))

# 1. Bar plot with error bars
ax1 = plt.subplot(2, 3, 1)
x_pos = np.arange(len(groups))
bars = ax1.bar(x_pos, means, yerr=1.96*ses, capsize=10,
               color=['#3498db', '#e74c3c', '#2ecc71'],
               edgecolor='black', linewidth=1.5, alpha=0.8)
ax1.axhline(grand_mean, color='black', linestyle='--', linewidth=2,
            label=f'Grand Mean = {grand_mean:.1f}')
ax1.set_ylabel('Systolic Blood Pressure (mmHg)', fontsize=11, fontweight='bold')
ax1.set_xlabel('Group', fontsize=11, fontweight='bold')
ax1.set_title('Mean Systolic BP by Group\n(with 95% CI)', fontsize=12, fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(groups, fontsize=9)
ax1.set_ylim([100, 130])
ax1.legend(loc='upper right')
ax1.grid(axis='y', alpha=0.3)

# Add value labels on bars
for i, (bar, mean, n_i) in enumerate(zip(bars, means, n)):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 2,
             f'{mean:.1f}\n(n={n_i})',
             ha='center', va='bottom', fontsize=9, fontweight='bold')

# 2. Box plot simulation
ax2 = plt.subplot(2, 3, 2)
np.random.seed(42)
# Simulate data based on means and SDs
simulated_data = []
for i in range(k):
    data = np.random.normal(means[i], sds[i], n[i])
    simulated_data.append(data)

bp = ax2.boxplot(simulated_data, labels=groups_short, patch_artist=True,
                  notch=True, showmeans=True,
                  meanprops=dict(marker='D', markerfacecolor='red', markersize=8))
colors = ['#3498db', '#e74c3c', '#2ecc71']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)
ax2.axhline(grand_mean, color='black', linestyle='--', linewidth=2, alpha=0.5)
ax2.set_ylabel('Systolic Blood Pressure (mmHg)', fontsize=11, fontweight='bold')
ax2.set_xlabel('Group', fontsize=11, fontweight='bold')
ax2.set_title('Distribution of Systolic BP by Group\n(Simulated Data)', fontsize=12, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

# 3. Variance components
ax3 = plt.subplot(2, 3, 3)
variance_labels = ['Between-Groups\nVariance (MSB)', 'Within-Groups\nVariance (MSW)']
variances = [MSB, MSW]
colors_var = ['#e74c3c', '#3498db']
bars_var = ax3.bar(variance_labels, variances, color=colors_var,
                    edgecolor='black', linewidth=1.5, alpha=0.8)
ax3.set_ylabel('Mean Square', fontsize=11, fontweight='bold')
ax3.set_title('ANOVA Variance Components', fontsize=12, fontweight='bold')
ax3.grid(axis='y', alpha=0.3)

# Add value labels
for bar, val in zip(bars_var, variances):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height/2,
             f'{val:.2f}',
             ha='center', va='center', fontsize=12, fontweight='bold', color='white')

# Add F-statistic annotation
ax3.text(0.5, max(variances) * 0.85,
         f'F = MSB/MSW = {F_stat:.3f}\np = {p_value:.4f}',
         ha='center', fontsize=11, fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

# 4. Sample sizes
ax4 = plt.subplot(2, 3, 4)
bars_n = ax4.bar(groups_short, n, color=['#3498db', '#e74c3c', '#2ecc71'],
                 edgecolor='black', linewidth=1.5, alpha=0.8)
ax4.set_ylabel('Sample Size', fontsize=11, fontweight='bold')
ax4.set_xlabel('Group', fontsize=11, fontweight='bold')
ax4.set_title('Sample Sizes by Group', fontsize=12, fontweight='bold')
ax4.grid(axis='y', alpha=0.3)

# Add value labels
for bar, n_val in zip(bars_n, n):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height/2,
             f'n = {n_val}',
             ha='center', va='center', fontsize=12, fontweight='bold', color='white')

# 5. Standard deviations
ax5 = plt.subplot(2, 3, 5)
bars_sd = ax5.bar(groups_short, sds, color=['#3498db', '#e74c3c', '#2ecc71'],
                   edgecolor='black', linewidth=1.5, alpha=0.8)
ax5.set_ylabel('Standard Deviation (mmHg)', fontsize=11, fontweight='bold')
ax5.set_xlabel('Group', fontsize=11, fontweight='bold')
ax5.set_title('Variability by Group', fontsize=12, fontweight='bold')
ax5.grid(axis='y', alpha=0.3)

# Add value labels
for bar, sd_val in zip(bars_sd, sds):
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height + 0.3,
             f'{sd_val:.1f}',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

# 6. F-distribution with critical region
ax6 = plt.subplot(2, 3, 6)
x = np.linspace(0, 6, 1000)
y = stats.f.pdf(x, df_between, df_within_total)
ax6.plot(x, y, 'b-', linewidth=2, label=f'F({df_between}, {df_within_total}) distribution')
ax6.fill_between(x[x >= F_critical], 0, stats.f.pdf(x[x >= F_critical], df_between, df_within_total),
                  alpha=0.3, color='red', label=f'Rejection region (α=0.05)')
ax6.axvline(F_stat, color='green', linestyle='--', linewidth=2,
            label=f'F-statistic = {F_stat:.3f}')
ax6.axvline(F_critical, color='red', linestyle='-', linewidth=2,
            label=f'F-critical = {F_critical:.3f}')
ax6.set_xlabel('F-value', fontsize=11, fontweight='bold')
ax6.set_ylabel('Probability Density', fontsize=11, fontweight='bold')
ax6.set_title('F-Distribution with Test Statistic', fontsize=12, fontweight='bold')
ax6.legend(loc='upper right', fontsize=9)
ax6.grid(alpha=0.3)

# Add conclusion text
if F_stat > F_critical:
    conclusion = "REJECT H₀: Significant difference found"
    color = 'red'
else:
    conclusion = "FAIL TO REJECT H₀: No significant difference"
    color = 'green'

ax6.text(0.5, 0.7, conclusion,
         transform=ax6.transAxes, ha='center', fontsize=10, fontweight='bold',
         bbox=dict(boxstyle='round', facecolor=color, alpha=0.3))

plt.suptitle('Homework 7: ANOVA Analysis of Diabetes and Blood Pressure Study\nProblem 12.7',
             fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout(rect=[0, 0, 1, 0.99])

# Save figure
output_file = '/Users/ugochi141/diabetes_bp_study_visualizations.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nVisualization saved to: {output_file}")

# Create a second figure with ANOVA table visualization
fig2, ax = plt.subplots(figsize=(10, 6))
ax.axis('tight')
ax.axis('off')

# ANOVA Table data
anova_data = [
    ['Source', 'df', 'Sum of Squares', 'Mean Square', 'F-statistic', 'p-value'],
    ['Between Groups', f'{df_between}', f'{SS_between:.2f}', f'{MSB:.2f}', f'{F_stat:.3f}', f'{p_value:.4f}'],
    ['Within Groups', f'{df_within_total}', f'{SS_within:.2f}', f'{MSW:.2f}', '', ''],
    ['Total', f'{N-1}', f'{SS_between + SS_within:.2f}', '', '', '']
]

table = ax.table(cellText=anova_data, cellLoc='center', loc='center',
                 colWidths=[0.2, 0.1, 0.2, 0.2, 0.15, 0.15])
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 3)

# Style header row
for i in range(6):
    cell = table[(0, i)]
    cell.set_facecolor('#34495e')
    cell.set_text_props(weight='bold', color='white')

# Style data rows
for i in range(1, 4):
    for j in range(6):
        cell = table[(i, j)]
        if i == 1:  # Between groups row
            cell.set_facecolor('#ecf0f1')
        elif i == 2:  # Within groups row
            cell.set_facecolor('#ffffff')
        else:  # Total row
            cell.set_facecolor('#bdc3c7')
            cell.set_text_props(weight='bold')

# Highlight F-statistic and p-value
table[(1, 4)].set_facecolor('#f39c12' if F_stat > F_critical else '#95a5a6')
table[(1, 4)].set_text_props(weight='bold')
table[(1, 5)].set_facecolor('#e74c3c' if p_value < 0.05 else '#2ecc71')
table[(1, 5)].set_text_props(weight='bold', color='white')

# Add title and interpretation
plt.title('ANOVA Table: Diabetes and Blood Pressure Study\n', fontsize=14, fontweight='bold', pad=20)

# Add interpretation text
interpretation = f"""
Interpretation:
• F-statistic ({F_stat:.3f}) {'>' if F_stat > F_critical else '≤'} F-critical ({F_critical:.3f})
• p-value ({p_value:.4f}) {'<' if p_value < 0.05 else '≥'} α (0.05)
• Conclusion: {conclusion}
"""

plt.text(0.5, 0.15, interpretation, transform=fig2.transFigure,
         ha='center', va='top', fontsize=11,
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Save ANOVA table
output_file2 = '/Users/ugochi141/anova_table_visualization.png'
plt.savefig(output_file2, dpi=300, bbox_inches='tight')
print(f"ANOVA table saved to: {output_file2}")

print("\n" + "=" * 70)
print("VISUALIZATIONS COMPLETE")
print("=" * 70)
