#!/usr/bin/env python3
"""
Generate and save Cobas diagrams as individual files
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch
from matplotlib.patches import ConnectionPatch
import numpy as np
import base64
from io import BytesIO
import json

# Import all the diagram functions from the previous script
from create_cobas_diagrams import (
    create_system_overview,
    create_rack_color_system,
    create_qc_workflow,
    create_alarm_system,
    create_daily_maintenance,
    create_pre_routine_workflow
)

def save_diagrams():
    """Generate and save all diagrams with their base64 strings"""
    
    diagrams = {
        'system_overview': create_system_overview(),
        'rack_colors': create_rack_color_system(),
        'qc_workflow': create_qc_workflow(),
        'alarm_system': create_alarm_system(),
        'daily_maintenance': create_daily_maintenance(),
        'pre_routine': create_pre_routine_workflow()
    }
    
    # Save to JSON file for easy access
    with open('diagram_base64.json', 'w') as f:
        json.dump(diagrams, f, indent=2)
    
    print("Diagrams saved to diagram_base64.json")
    return diagrams

if __name__ == "__main__":
    diagrams = save_diagrams()
    print(f"Generated {len(diagrams)} diagrams successfully!")