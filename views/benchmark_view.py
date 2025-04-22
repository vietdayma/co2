import tkinter as tk
from tkinter import ttk
from controllers.emission_controller import EmissionController
from utils.benchmark_tester import BenchmarkTester

class BenchmarkView:
    def __init__(self, controller: EmissionController, benchmark_tester: BenchmarkTester):
        self.controller = controller
        self.benchmark_tester = benchmark_tester
        self.window = None

    def show(self):
        self.window = tk.Toplevel()
        self.window.title("CO2 Emission Prediction - Benchmark")
        self.window.geometry("600x400")

        # Create main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Add title
        title_label = ttk.Label(main_frame, text="Model Benchmark Results", font=("Helvetica", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Add benchmark button
        benchmark_button = ttk.Button(main_frame, text="Run Benchmark", command=self._run_benchmark)
        benchmark_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Create text widget for results
        self.results_text = tk.Text(main_frame, height=15, width=60)
        self.results_text.grid(row=2, column=0, columnspan=2, pady=10)
        self.results_text.config(state=tk.DISABLED)

    def _run_benchmark(self):
        # Clear previous results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        # Run benchmark tests
        results = self.benchmark_tester.run_benchmarks()
        
        # Display results
        self.results_text.insert(tk.END, "Benchmark Results:\n\n")
        self.results_text.insert(tk.END, f"Mean Absolute Error: {results['mae']:.2f}\n")
        self.results_text.insert(tk.END, f"Mean Squared Error: {results['mse']:.2f}\n")
        self.results_text.insert(tk.END, f"R² Score: {results['r2']:.3f}\n")
        self.results_text.insert(tk.END, f"\nPrediction Time: {results['prediction_time']:.3f} seconds\n")
        self.results_text.insert(tk.END, f"Memory Usage: {results['memory_usage']:.2f} MB\n")
        
        self.results_text.config(state=tk.DISABLED) 