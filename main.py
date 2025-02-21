import numpy as np
import matplotlib.pyplot as plt

def read_data(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            print(parts)
            if len(parts) < 6:
                continue  # Skip invalid lines
            p_str = parts[0]
            p = int(''.join(filter(str.isdigit, p_str)))  # Extract numeric part of node name
            t_total = float(parts[1])
            t_reg = float(parts[2])
            t_err = float(parts[3])
            t_adjust = float(parts[4])
            t_init = float(parts[5])
            data.append((p, t_total, t_reg, t_err, t_adjust, t_init))
    return data

def compute_speedup(data):
    speedup_results = []
    for p, t_total, t_reg, t_err, t_adjust, t_init in data:
        X = (t_reg + t_err + t_adjust + t_init) / t_total  # Compute X
        S_predicted = 1 / (1 - X + (X / p))  # Amdahl's law speedup
        Tpar_p = 1 / S_predicted  # Parallel time prediction
        speedup_results.append((p, S_predicted, Tpar_p))
    return speedup_results

def plot_results(data, speedup_results, title):
    p_values, t_total, t_reg, t_err, t_adjust, t_init = zip(*data)
    p_speedup, S_predicted, Tpar_p = zip(*speedup_results)
    
    plt.figure(figsize=(10, 6))
    plt.plot(p_values, t_total, 'o-', label='Total Time')
    plt.plot(p_values, t_reg, 'o-', label='Regular')
    plt.plot(p_values, t_err, 'o-', label='Error')
    plt.plot(p_values, t_adjust, 'o-', label='Adjust')
    plt.plot(p_values, t_init, 'o-', label='Init')
    plt.plot(p_values, Tpar_p, 's--', label='Predicted (Amdahl)')
    
    plt.xlabel('Number of Nodes (p)')
    plt.ylabel('Time')
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()

def main():
    filename = 'gpu_data.txt'  # Update with your actual file path
    data = read_data(filename)
    speedup_results = compute_speedup(data)
    plot_results(data, speedup_results, "Amdahl's Law Analysis for GPU/CPU")
    
    # Save processed data
    with open('processed_results.txt', 'w') as f:
        for p, S_predicted, Tpar_p in speedup_results:
            f.write(f'{p} {S_predicted:.4f} {Tpar_p:.4f}\n')
    print("Results saved to processed_results.txt")

if __name__ == "__main__":
    main()