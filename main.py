# import numpy as np
# import matplotlib.pyplot as plt

# def read_data(filename):
#     data = []
#     with open(filename, 'r') as file:
#         for line in file:
#             parts = line.split()
#             print(parts)
#             if len(parts) < 6:
#                 continue  # Skip invalid lines
#             p_str = parts[0]
#             p = int(''.join(filter(str.isdigit, p_str)))  # Extract numeric part of node name
#             t_total = float(parts[1])
#             t_reg = float(parts[2])
#             t_err = float(parts[3])
#             t_adjust = float(parts[4])
#             t_init = float(parts[5])
#             data.append((p, t_total, t_reg, t_err, t_adjust, t_init))
#     return data

# def compute_speedup(data):
#     speedup_results = []
#     for p, t_total, t_reg, t_err, t_adjust, t_init in data:
#         X = (t_reg + t_err + t_adjust + t_init) / t_total  # Compute X
#         S_predicted = 1 / (1 - X + (X / p))  # Amdahl's law speedup
#         Tpar_p = 1 / S_predicted  # Parallel time prediction
#         speedup_results.append((p, S_predicted, Tpar_p))
#     return speedup_results

# def plot_results(data, speedup_results, title):
#     p_values, t_total, t_reg, t_err, t_adjust, t_init = zip(*data)
#     p_speedup, S_predicted, Tpar_p = zip(*speedup_results)
    
#     plt.figure(figsize=(10, 6))
#     plt.plot(p_values, t_total, 'o-', label='Total Time')
#     plt.plot(p_values, t_reg, 'o-', label='Regular')
#     plt.plot(p_values, t_err, 'o-', label='Error')
#     plt.plot(p_values, t_adjust, 'o-', label='Adjust')
#     plt.plot(p_values, t_init, 'o-', label='Init')
#     plt.plot(p_values, Tpar_p, 's--', label='Predicted (Amdahl)')
    
#     plt.xlabel('Number of Nodes (p)')
#     plt.ylabel('Time')
#     plt.title(title)
#     plt.legend()
#     plt.grid()
#     plt.show()

# def main():
#     filename = 'gpu_data.txt'  # Update with your actual file path
#     data = read_data(filename)
#     speedup_results = compute_speedup(data)
#     plot_results(data, speedup_results, "Amdahl's Law Analysis for GPU/CPU")
    
#     # Save processed data
#     with open('processed_results.txt', 'w') as f:
#         for p, S_predicted, Tpar_p in speedup_results:
#             f.write(f'{p} {S_predicted:.4f} {Tpar_p:.4f}\n')
#     print("Results saved to processed_results.txt")

# if __name__ == "__main__":
#     main()

import numpy as np
import matplotlib.pyplot as plt

def read_data(filename):
    data_gpu = []
    data_cpu = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) < 6:
                continue  # Skip invalid lines
            p_str = parts[0]
            p = int(''.join(filter(str.isdigit, p_str)))  # Extract numeric part of node name
            t_total = float(parts[1])
            t_reg = float(parts[2])
            t_err = float(parts[3])
            t_adjust = float(parts[4])
            t_init = float(parts[5])
            if "gpu" in p_str.lower():
                data_gpu.append((p, t_total, t_reg, t_err, t_adjust, t_init))
            else:
                data_cpu.append((p, t_total, t_reg, t_err, t_adjust, t_init))
    return data_gpu, data_cpu

def compute_speedup(data):
    speedup_results = []
    for p, t_total, t_reg, t_err, t_adjust, t_init in data:
        X = (t_reg + t_err + t_adjust + t_init) / t_total  # Compute X
        S_predicted = 1 / (1 - X + (X / p))  # Amdahl's law speedup
        Tpar_p = 1 / S_predicted  # Parallel time prediction
        speedup_results.append((p, S_predicted, Tpar_p))
    return speedup_results

def plot_results(data_gpu, data_cpu, speedup_results_gpu, speedup_results_cpu):
    plt.figure(figsize=(10, 6))
    
    if data_gpu:
        p_values_gpu, t_total_gpu, t_reg_gpu, t_err_gpu, t_adjust_gpu, t_init_gpu = zip(*data_gpu)
        p_speedup_gpu, S_predicted_gpu, Tpar_p_gpu = zip(*speedup_results_gpu)
        plt.plot(p_values_gpu, t_total_gpu, 'o-', label='GPU Total Time')
        plt.plot(p_values_gpu, Tpar_p_gpu, 's--', label='GPU Predicted (Amdahl)')
        plt.xlabel('Number of Nodes (p)')
        plt.ylabel('Time (log scale)')
        plt.title("Amdahl's Law Analysis for GPU")
        plt.legend()
        plt.grid()
        plt.savefig("gpu.png",dpi=300)
        plt.show()
    
    if data_cpu:
        p_values_cpu, t_total_cpu, t_reg_cpu, t_err_cpu, t_adjust_cpu, t_init_cpu = zip(*data_cpu)
        p_speedup_cpu, S_predicted_cpu, Tpar_p_cpu = zip(*speedup_results_cpu)
        plt.plot(p_values_cpu, t_total_cpu, 'o-', label='CPU Total Time')
        plt.plot(p_values_cpu, Tpar_p_cpu, 's--', label='CPU Predicted (Amdahl)')
        plt.xlabel('Number of Nodes (p)')
        plt.ylabel('Time (log scale)')
        plt.title("Amdahl's Law Analysis for CPU")
        plt.legend()
        plt.grid()
        plt.savefig("cpu.png",dpi=300)
        plt.show()
    
   

def main():
    filename = 'gpu_data.txt'  # Update with your actual file path
    data_gpu, data_cpu = read_data(filename)
    speedup_results_gpu = compute_speedup(data_gpu)
    speedup_results_cpu = compute_speedup(data_cpu)
    plot_results(data_gpu, data_cpu, speedup_results_gpu, speedup_results_cpu)
    
    # Save processed data
    with open('processed_results.txt', 'w') as f:
        for p, S_predicted, Tpar_p in speedup_results_gpu + speedup_results_cpu:
            f.write(f'{p} {S_predicted:.4f} {Tpar_p:.4f}\n')
    print("Results saved to processed_results.txt")

if __name__ == "__main__":
    main()
