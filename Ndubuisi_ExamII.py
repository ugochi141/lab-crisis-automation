#!/usr/bin/env python3
import os
import re

print("="*50)
print("Starting Exam II - Ndubuisi")
print("="*50)

# Questions 1 & 2: DNA sequence processing
print("\nQuestions 1 & 2: Processing DNA sequence...")

# Q1: Read the DNA file and split into exons/intron
with open('Q1_dna.txt', 'r') as file:
    sequence = file.read().strip()

# Your code for extracting exons and intron
# Remember: exon1 is 0:63, intron is 63:90, exon2 is 90:end
exon1 = sequence[?:?]  # You fill in the numbers
intron = sequence[?:?]  # You fill in the numbers
exon2 = sequence[?:]   # You fill in the numbers

# Combine coding regions and write files
coding = exon1 + exon2

with open('coding.txt', 'w') as file:
    file.write(coding)

with open('non_coding.txt', 'w') as file:
    file.write(intron)

print("Q1: Files 'coding.txt' and 'non_coding.txt' created")

# Q2: Calculate percentage
percentage = (len(coding) / len(sequence)) * 100
print(f"Q2: Percentage of sequence that is coding: {percentage:.2f}%")

# Question 3: FASTA file creation
print("\nQuestion 3: Creating FASTA files...")

# Read both files
with open('Q2_sequences.txt', 'r') as file:
    sequences = file.read().strip().split('\n')

with open('Q2_AccessionNumbers.txt', 'r') as file:
    accessions = file.read().strip().split('\n')

# Process each sequence
for i in range(len(sequences)):
    sequence = sequences[i]
    accession = accessions[i]
    
    # Clean sequence - you need to:
    # 1. Make uppercase
    # 2. Remove special characters (-)
    clean_sequence = sequence.?().?('-', '')  # Fill in the methods
    
    # Create FASTA file
    filename = f"{accession}.txt"
    
    with open(filename, 'w') as file:
        file.write(f">{accession}\n")
        file.write(f"{clean_sequence}\n")
    
    print(f"Created {filename}")

# Question 4: Reverse complement checker
print("\nQuestion 4: Reverse complement checker...")
# Your code here - remember:
# - Get two sequences from user
# - Create complement (A↔T, G↔C)
# - Reverse it
# - Compare

# Question 5: Population growth
print("\nQuestion 5: Population growth calculator...")

# Input validation for starting population
while True:
    start_pop = int(input("Starting number of organisms: "))
    if start_pop >= ?:  # What's the minimum?
        break
    print("Error: Must have at least ? organisms")

# Input validation for growth rate
while True:
    growth_rate = float(input("Average daily increase (as percentage): "))
    if growth_rate >= ?:  # What's the minimum?
        break
    print("Error: Growth rate cannot be ?")

# Input validation for days
while True:
    days = int(input("Number of days to multiply: "))
    if days >= ?:  # What's the minimum?
        break
    print("Error: Must have at least ? day")

# Display table
print("\nDay\tOrganisms")
print("-" * 29)

population = float(start_pop)
for day in range(1, days + 1):
    print(f"{day}\t{population}")
    # Calculate next day's population
    population = population * (1 + growth_rate/?)  # Convert percentage

print("\n" + "="*50)
print("Questions 1-5 Complete")
print("="*50)


