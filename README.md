# Interval Scheduling: Empirical Runtime & Optimality Study

## Overview

This project performs a rigorous empirical analysis of Interval Scheduling Algorithms. It compares the performance and accuracy of various Greedy strategies (polynomial time) against an Exhaustive Search (exponential time) oracle. The study validates theoretical Big-O complexity predictions and measures "solution quality" across different conflict regimes (High, Medium, and Low overlap).

## Features
1. **Synthetic Dataset Generator:** Creates randomized interval sets with tunable "conflict density" (α).
2. **Algorithms Implemented:**
   - **Greedy (EFT):** Earliest Finish Time (Proven Optimal).
   - **Greedy (EST):** Earliest Start Time (Heuristic).
   - **Greedy (SD):** Shortest Duration (Heuristic).
   - **Exhaustive:** Recursive Brute-Force (O(2^n)) to find the ground truth.
3. **Automated Benchmarking:** Measures execution time for n=10 up to n=100,000+.
4. **Visualization:** Automatically generates Log-Log and Linear plots to verify Time Complexity.

## Requirements
- Python 3.x
- matplotlib (for plotting graphs)
`pip install matplotlib`

## Usage
`python interval.py`

## What happens when you run it?
1. **Optimality Study:** Runs all algorithms on small datasets (n=15) over 50 trials to compare accuracy.
2. **Runtime Study:** Benchmarks Greedy algorithms on massive datasets and Exhaustive algorithms on small datasets.
3. **Plotting:** Opens a window showing the Runtime vs. Input Size graphs.
