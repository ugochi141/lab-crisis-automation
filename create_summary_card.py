import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(1, 1, figsize=(8, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# Title
title_box = patches.FancyBboxPatch((0.5, 10), 9, 1.5, 
                                   boxstyle="round,pad=0.1",
                                   facecolor='darkblue', 
                                   edgecolor='black',
                                   linewidth=2)
ax.add_patch(title_box)
ax.text(5, 10.75, 'NGS VARIANT ANALYSIS REPORT', 
        ha='center', fontsize=16, fontweight='bold', color='white')

# Participant info
ax.text(5, 9.5, 'Participant: huD3FFCB', ha='center', fontsize=14, fontweight='bold')
ax.text(5, 9, 'Variant: chr6:15241774 A>G', ha='center', fontsize=12)

# Key finding box
key_box = patches.FancyBboxPatch((0.5, 6.5), 9, 2, 
                                 boxstyle="round,pad=0.1",
                                 facecolor='lightyellow', 
                                 edgecolor='red',
                                 linewidth=2)
ax.add_patch(key_box)
ax.text(5, 7.8, '⚠️ NOVEL/ULTRA-RARE VARIANT', 
        ha='center', fontsize=14, fontweight='bold', color='red')
ax.text(5, 7.3, 'Not found in gnomAD or ClinVar', ha='center', fontsize=11)
ax.text(5, 6.9, 'Intergenic location (JARID2 upstream)', ha='center', fontsize=11)

# Results summary
results_y = 5.5
ax.text(1, results_y, 'Database Results:', fontsize=12, fontweight='bold')
results = [
    ('gnomAD v4.1.0:', 'NOT FOUND', 'red'),
    ('ClinVar:', 'NOT FOUND', 'red'),
    ('VEP Impact:', 'MODIFIER', 'orange'),
    ('Location:', 'Intergenic', 'blue')
]

y_pos = results_y - 0.5
for label, value, color in results:
    ax.text(1.5, y_pos, label, fontsize=10)
    ax.text(4, y_pos, value, fontsize=10, fontweight='bold', color=color)
    y_pos -= 0.4

# Classification
class_box = patches.FancyBboxPatch((0.5, 2), 9, 1, 
                                   boxstyle="round,pad=0.1",
                                   facecolor='lightgray', 
                                   edgecolor='black',
                                   linewidth=1)
ax.add_patch(class_box)
ax.text(5, 2.5, 'ACMG Classification: VUS (Variant of Uncertain Significance)', 
        ha='center', fontsize=12, fontweight='bold')

# Recommendations
ax.text(1, 1.5, 'Next Steps:', fontsize=11, fontweight='bold')
ax.text(1.5, 1.1, '1. Family segregation analysis', fontsize=9)
ax.text(1.5, 0.8, '2. Check for regulatory elements', fontsize=9)
ax.text(1.5, 0.5, '3. Consider functional validation', fontsize=9)

plt.tight_layout()
plt.savefig('variant_summary_card.png', dpi=300, bbox_inches='tight')
plt.savefig('variant_summary_card.pdf', bbox_inches='tight')
print("Summary card created!")
