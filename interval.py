import random
import time
import math
import statistics
import itertools
import matplotlib.pyplot as plt

# Initialization of interval
class Interval:
    def __init__(self, start, finish, id=None):
        self.start = start
        self.finish = finish
        self.id = id
        self.duration = finish - start
    
    def __repr__(self):
        return f"({self.start:.1f}, {self.finish:.1f})"

# Generating the interval dataset
def generate_dataset(n, alpha, D):
    T = alpha * n * D
    intervals = []
    for i in range(n):
        start = random.uniform(0, T)
        duration = random.uniform(1, D)
        intervals.append(Interval(start, start + duration, id=i))
    return intervals

# Sort and select non-overlapping intervals.
def greedy_schedule(intervals, strategy='EFT'):
    if not intervals: return []
    
    # Sort based on strategy
    if strategy == 'EFT':
        intervals.sort(key=lambda x: x.finish)
    elif strategy == 'EST':
        intervals.sort(key=lambda x: x.start)
    elif strategy == 'SD':
        intervals.sort(key=lambda x: x.duration)
        
    selected = [intervals[0]]
    for current in intervals[1:]:
        if current.start >= selected[-1].finish:
            selected.append(current)
    return selected

# Find the true optimal subset size (exponential time)
def exhaustive_schedule(intervals):
    # Helper to check validity
    def is_valid(subset):
        sorted_sub = sorted(subset, key=lambda x: x.finish)
        for i in range(len(sorted_sub) - 1):
            if sorted_sub[i].finish > sorted_sub[i+1].start:
                return False
        return True

    n = len(intervals)
    # Check largest subsets first
    for r in range(n, 0, -1):
        for subset in itertools.combinations(intervals, r):
            if is_valid(subset):
                return list(subset)
    return []

# Runtime Experiment Initialization (Big-O)
def run_runtime_experiment():
    print("\n Running Runtime Complexity Study")
    
    greedy_ns = [2**i for i in range(10, 18)]
    exhaustive_ns = range(5, 26, 5)
    trials = 10
    alpha = 1.0
    D = 100.0

    greedy_times = {}
    exhaustive_times = {}

    # EFT Benchmark
    print("Benchmarking Greedy (EFT)")
    for n in greedy_ns:
        times = []
        greedy_schedule(generate_dataset(n, alpha, D))
        for _ in range(trials):
            data = generate_dataset(n, alpha, D)
            start = time.perf_counter()
            greedy_schedule(data, 'EFT')
            times.append(time.perf_counter() - start)
        greedy_times[n] = statistics.mean(times)
        print(f"n={n}: {greedy_times[n]:.6f}s")

    # Exhaustive Benchmark
    print("\n Benchmarking Exhaustive")
    for n in exhaustive_ns:
        times = []
        exhaustive_schedule(generate_dataset(n, alpha, D))
        for _ in range(trials):
            data = generate_dataset(n, alpha, D)
            start = time.perf_counter()
            exhaustive_schedule(data)
            times.append(time.perf_counter() - start)
        avg_time = statistics.mean(times)
        exhaustive_times[n] = avg_time
        print(f"n={n}: {avg_time:.6f}s")
        if avg_time > 10.0:
            print("Stopping exhaustive early (too slow).")
            break

    return greedy_times, exhaustive_times

# Optimality Study
def run_optimality_study():
    print("\n Running Solution Quality Study")
    alphas = {'High Overlap': 0.1, 'Medium Overlap': 1.0, 'Low Overlap': 5.0}
    n = 15
    trials = 50 
    D = 100.0
    
    print(f"{'Regime':<15} | {'EFT %':<8} | {'EST %':<8} | {'SD %':<8}")
    print("-" * 50)
    
    for name, alpha in alphas.items():
        eft_score, est_score, sd_score = 0, 0, 0
        
        for _ in range(trials):
            data = generate_dataset(n, alpha, D)
            
            # Optimal Solution
            optimal = len(exhaustive_schedule(data))
            
            # Greedy Results
            eft = len(greedy_schedule(data[:], 'EFT'))
            est = len(greedy_schedule(data[:], 'EST'))
            sd  = len(greedy_schedule(data[:], 'SD'))
            
            # Calculate Ratio (Greedy / Optimal)
            eft_score += (eft / optimal)
            est_score += (est / optimal)
            sd_score  += (sd / optimal)
            
        print(f"{name:<15} | {eft_score/trials:.2%} | {est_score/trials:.2%} | {sd_score/trials:.2%}")

# Result Plotting
def plot_results(greedy_times, exhaustive_times):
    # Greedy Plot
    g_x = list(greedy_times.keys())
    g_y = list(greedy_times.values())
    
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.loglog(g_x, g_y, 'b-o', label='EFT Runtime')
    ref = [y for y in g_y]
    plt.title("Greedy Runtime (Log-Log)")
    plt.xlabel("n (intervals)")
    plt.ylabel("Time (s)")
    plt.grid(True, which="both", ls="-")
    
    # Exhaustive Plot
    e_x = list(exhaustive_times.keys())
    e_y = list(exhaustive_times.values())
    
    plt.subplot(1, 2, 2)
    plt.plot(e_x, e_y, 'r-o', label='Exhaustive Runtime')
    plt.title("Exhaustive Runtime (Linear Scale)")
    plt.xlabel("n (intervals)")
    plt.ylabel("Time (s)")
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_optimality_study() # Optimality Study
    
    g_times, e_times = run_runtime_experiment() # Runtime Experiment
    plot_results(g_times, e_times) # Plot Graph