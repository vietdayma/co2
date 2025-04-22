import time
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

class BenchmarkUtils:
    def __init__(self):
        self.results = []
        self.start_time = None
        self.end_time = None
        
    def start_benchmark(self):
        """Start the benchmark session"""
        self.start_time = time.time()
        self.results = []
        
    def record_prediction(self, duration, prediction, status='success', error=None):
        """Record a single prediction result"""
        # Validate prediction result
        if prediction is None and error is None:
            status = 'error'
            error = 'No prediction result'
        elif prediction is None and error is not None:
            status = 'error'
        elif prediction is not None:
            status = 'success'
            error = None
            
        # Ensure duration is positive
        duration = max(duration, 0.000001)  # Minimum 1 microsecond
        
        self.results.append({
            'timestamp': datetime.now(),
            'duration': duration,
            'prediction': prediction,
            'status': status,
            'error': error
        })
        
    def end_benchmark(self):
        """End the benchmark session"""
        self.end_time = time.time()
        
    def get_statistics(self):
        """Calculate benchmark statistics"""
        if not self.results:
            return {
                'total_time': 0,
                'total_requests': 0,
                'successful_requests': 0,
                'requests_per_second': 0,
                'success_rate': 0,
                'avg_response_time': 0,
                'min_response_time': 0,
                'max_response_time': 0,
                'std_response_time': 0
            }
            
        df = pd.DataFrame(self.results)
        successful_df = df[df['status'] == 'success']
        
        total_time = self.end_time - self.start_time
        total_requests = len(df)
        successful_requests = len(successful_df)
        
        # Calculate statistics only if there are successful requests
        if successful_requests > 0:
            avg_response_time = successful_df['duration'].mean()
            min_response_time = successful_df['duration'].min()
            max_response_time = successful_df['duration'].max()
            std_response_time = successful_df['duration'].std()
        else:
            avg_response_time = min_response_time = max_response_time = std_response_time = 0
        
        stats = {
            'total_time': total_time,
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'requests_per_second': total_requests / total_time if total_time > 0 else 0,
            'success_rate': (successful_requests / total_requests * 100) if total_requests > 0 else 0,
            'avg_response_time': avg_response_time,
            'min_response_time': min_response_time,
            'max_response_time': max_response_time,
            'std_response_time': std_response_time
        }
        
        return stats
    
    def plot_response_times(self):
        """Create response time trend plot"""
        df = pd.DataFrame(self.results)
        successful_df = df[df['status'] == 'success']
        
        if successful_df.empty:
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.text(0.5, 0.5, 'No successful requests to plot', 
                   ha='center', va='center')
            ax.set_xlabel('Request Number')
            ax.set_ylabel('Response Time (ms)')
            ax.set_title('Response Time Trend')
            return fig
            
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(range(len(successful_df)), successful_df['duration'] * 1000)
        ax.set_xlabel('Request Number')
        ax.set_ylabel('Response Time (ms)')
        ax.set_title('Response Time Trend')
        plt.grid(True, alpha=0.3)
        return fig
    
    def plot_response_distribution(self):
        """Create response time distribution plot"""
        df = pd.DataFrame(self.results)
        successful_df = df[df['status'] == 'success']
        
        if successful_df.empty:
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.text(0.5, 0.5, 'No successful requests to plot', 
                   ha='center', va='center')
            ax.set_xlabel('Response Time (ms)')
            ax.set_ylabel('Frequency')
            ax.set_title('Response Time Distribution')
            return fig
            
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.hist(successful_df['duration'] * 1000, bins=50)
        ax.set_xlabel('Response Time (ms)')
        ax.set_ylabel('Frequency')
        ax.set_title('Response Time Distribution')
        plt.grid(True, alpha=0.3)
        return fig
    
    def get_results_df(self):
        """Get results as DataFrame"""
        df = pd.DataFrame(self.results)
        if not df.empty:
            df['duration_ms'] = df['duration'] * 1000  # Convert to milliseconds
        return df 