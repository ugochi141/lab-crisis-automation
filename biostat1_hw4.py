#!/usr/bin/env python3
"""
Biostatistics Homework 4 Solutions
"""

import math

print("\n" + "="*60)
print(" BIOSTATISTICS HOMEWORK 4 SOLUTIONS")
print("="*60)

# Problem 8.2
print("\n8.2 Why is random sampling important?")
print("-" * 40)
print("""
- Ensures unbiased representation
- Enables valid statistical inference  
- Allows calculation of sampling error
- Results are generalizable
- Sample statistics are unbiased estimators
""")

# Problem 8.4
print("\n8.4 Standard Error")
print("-" * 40)
print("""
SE = σ/√n

- Always smaller than σ (when n > 1)
- Decreases as n increases
- Measures variability of sample means
- σ measures variability of individual values
""")

# Problem 8.11: Norwegian Birth Weights
print("\n8.11 Norwegian Birth Weights")
print("-" * 40)

mu = 3500
sigma = 430
n = 5

# Part a
z_a = (2500 - mu) / sigma
print(f"\na) P(weight < 2500g):")
print(f"   Z-score = {z_a:.4f}")
print(f"   Probability ≈ 0.01 or 1%")

# Part b
z_b = -1.645
x_b = mu + z_b * sigma
print(f"\nb) 5th percentile:")
print(f"   Value = {x_b:.1f} grams")

# Part c
se = sigma / math.sqrt(n)
print(f"\nc) Distribution of sample means (n=5):")
print(f"   Mean of means = {mu} grams")
print(f"   Standard error = {se:.2f} grams")

# Part d
x_bar_d = mu + z_b * se
print(f"\nd) 5th percentile of sample means:")
print(f"   Value = {x_bar_d:.1f} grams")

# Part e
z_e = (2500 - mu) / se
print(f"\ne) P(mean of 5 < 2500g):")
print(f"   Z-score = {z_e:.4f}")
print(f"   Probability ≈ 0.0000001 (essentially 0)")

# Part f
p = 0.01
prob_f = 5 * p * (1-p)**4
print(f"\nf) P(exactly 1 of 5 < 2500g):")
print(f"   Probability = {prob_f:.4f} or {prob_f*100:.2f}%")

# Problem 9.3
print("\n9.3 Factors affecting CI length")
print("-" * 40)
print("""
1. Sample size (n): Larger n → Shorter CI
2. Confidence level: Higher confidence → Wider CI  
3. Standard deviation: Greater σ → Wider CI
4. Known vs unknown σ: Unknown σ → Wider CI
""")

# Problem 9.12 - Demo code
print("\n9.12 Serum Zinc (Demo with simulated data)")
print("-" * 40)
n = 462
mean = 86.0
std = 12.0
se = std / math.sqrt(n)
t_critical = 1.96  # approximation for large n
margin = t_critical * se

print(f"Sample: n={n}, mean={mean:.1f}, std={std:.1f}")
print(f"95% CI = ({mean-margin:.2f}, {mean+margin:.2f}) μg/dL")
print("\nInterpretation: We are 95% confident the true mean")
print(f"is between {mean-margin:.2f} and {mean+margin:.2f} μg/dL")

# Problem 9.13 - Demo code  
print("\n9.13 Blood Pressure (Demo with simulated data)")
print("-" * 40)
# Males
m_mean, m_std, m_n = 45.0, 11.0, 50
m_se = m_std / math.sqrt(m_n)
m_margin = 1.96 * m_se

# Females
f_mean, f_std, f_n = 43.0, 10.0, 50
f_se = f_std / math.sqrt(f_n)
f_margin = 1.96 * f_se

print(f"Males 95% CI: ({m_mean-m_margin:.2f}, {m_mean+m_margin:.2f}) mmHg")
print(f"Females 95% CI: ({f_mean-f_margin:.2f}, {f_mean+f_margin:.2f}) mmHg")

# Known sigma = 11
known_sigma = 11
m_margin_known = 1.96 * known_sigma / math.sqrt(m_n)
f_margin_known = 1.96 * known_sigma / math.sqrt(f_n)

print(f"\nWith known σ=11:")
print(f"Males: ({m_mean-m_margin_known:.2f}, {m_mean+m_margin_known:.2f}) mmHg")
print(f"Females: ({f_mean-f_margin_known:.2f}, {f_mean+f_margin_known:.2f}) mmHg")

print("\n" + "="*60)
print("All problems solved!")
print("For 9.12 and 9.13, replace simulated data with actual data")
print("="*60)
