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
        df = pd.DataFrame(self.results)
        successful_df = df[df['status'] == 'success']
        
        total_time = self.end_time - self.start_time
        total_requests = len(df)
        successful_requests = len(successful_df)
        
        stats = {
            'total_time': total_time,
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'requests_per_second': total_requests / total_time,
            'success_rate': (successful_requests / total_requests) * 100,
            'avg_response_time': successful_df['duration'].mean() if not successful_df.empty else 0,
            'min_response_time': successful_df['duration'].min() if not successful_df.empty else 0,
            'max_response_time': successful_df['duration'].max() if not successful_df.empty else 0,
            'std_response_time': successful_df['duration'].std() if not successful_df.empty else 0
        }
        
        return stats
    
    def plot_response_times(self):
        """Create response time trend plot"""
        df = pd.DataFrame(self.results)
        successful_df = df[df['status'] == 'success']
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(range(len(successful_df)), successful_df['duration'] * 1000)
        ax.set_xlabel('Request Number')
        ax.set_ylabel('Response Time (ms)')
        ax.set_title('Response Time Trend')
        return fig
    
    def plot_response_distribution(self):
        """Create response time distribution plot"""
        df = pd.DataFrame(self.results)
        successful_df = df[df['status'] == 'success']
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.hist(successful_df['duration'] * 1000, bins=50)
        ax.set_xlabel('Response Time (ms)')
        ax.set_ylabel('Frequency')
        ax.set_title('Response Time Distribution')
        return fig
    
    def get_results_df(self):
        """Get results as DataFrame"""
        return pd.DataFrame(self.results) 