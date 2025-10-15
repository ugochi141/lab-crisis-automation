#!/usr/bin/env python3

# Read VEP output
with open('vep_output.txt', 'r') as f:
    lines = f.readlines()

# Skip headers and find result lines
results = []
header_line = None

for line in lines:
    if line.startswith('#Uploaded_variation'):
        header_line = line.strip().split('\t')
    elif not line.startswith('#'):
        results.append(line.strip().split('\t'))

# Display results
if header_line and results:
    print("VEP Analysis Results for chr6:15241774 A>G")
    print("=" * 50)
    
    for result in results:
        if len(result) >= len(header_line):
            print("\nVariant Details:")
            for i, field in enumerate(header_line):
                if i < len(result):
                    print(f"{field}: {result[i]}")
        print("-" * 30)
else:
    print("No results found in VEP output")
