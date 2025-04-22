import time
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class BenchmarkUtils:
    def __init__(self):
        self.results = []
        self.start_time = None
        self.end_time = None
        
    def start_benchmark(self):
        """Start the benchmark session"""
        self.start_time = time.perf_counter_ns()
        self.results = []
        
    def record_prediction(self, timing_data):
        """Record a prediction result with network metrics"""
        # Ensure all required fields exist with defaults
        timing_data = {
            'timestamp': datetime.now(),
            'total_time': timing_data.get('total_time', 0),
            'network_time': timing_data.get('network_time', 0),
            'processing_time': timing_data.get('processing_time', 0),
            'prediction': timing_data.get('prediction'),
            'status': timing_data.get('status', 'error'),
            'error': timing_data.get('error')
        }
        
        self.results.append(timing_data)
        
    def end_benchmark(self):
        """End the benchmark session"""
        self.end_time = time.perf_counter_ns()
        
    def get_statistics(self):
        """Calculate benchmark statistics including network metrics"""
        if not self.results:
            return {
                'total_time': 0,
                'total_requests': 0,
                'successful_requests': 0,
                'requests_per_second': 0,
                'success_rate': 0,
                'avg_total_time': 0,
                'avg_network_time': 0,
                'avg_processing_time': 0,
                'min_response_time': 0,
                'max_response_time': 0
            }
            
        df = pd.DataFrame(self.results)
        successful_df = df[df['status'] == 'success']
        
        total_time = (self.end_time - self.start_time) / 1_000_000_000  # Convert to seconds
        total_requests = len(df)
        successful_requests = len(successful_df)
        
        # Calculate statistics only if there are successful requests
        if successful_requests > 0:
            avg_total_time = successful_df['total_time'].mean()
            avg_network_time = successful_df['network_time'].mean()
            avg_processing_time = successful_df['processing_time'].mean()
            min_response_time = successful_df['total_time'].min()
            max_response_time = successful_df['total_time'].max()
        else:
            avg_total_time = avg_network_time = avg_processing_time = min_response_time = max_response_time = 0
        
        stats = {
            'total_time': total_time,
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'requests_per_second': total_requests / total_time if total_time > 0 else 0,
            'success_rate': (successful_requests / total_requests * 100) if total_requests > 0 else 0,
            'avg_total_time': avg_total_time,
            'avg_network_time': avg_network_time,
            'avg_processing_time': avg_processing_time,
            'min_response_time': min_response_time,
            'max_response_time': max_response_time
        }
        
        return stats
    
    def plot_response_times(self):
        """Create response time trend plot with network breakdown"""
        df = pd.DataFrame(self.results)
        successful_df = df[df['status'] == 'success']
        
        if successful_df.empty:
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.text(0.5, 0.5, 'No successful requests to plot', 
                   ha='center', va='center')
            ax.set_xlabel('Request Number')
            ax.set_ylabel('Time (ms)')
            ax.set_title('Response Time Breakdown')
            return fig
            
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Plot total time
        ax.plot(range(len(successful_df)), successful_df['total_time'], 
                label='Total Time', color='blue')
        
        # Plot network time as stacked area
        ax.fill_between(range(len(successful_df)), 
                       successful_df['network_time'],
                       color='red', alpha=0.3, label='Network Time')
        
        # Plot processing time as stacked area
        ax.fill_between(range(len(successful_df)),
                       successful_df['processing_time'],
                       successful_df['network_time'],
                       color='green', alpha=0.3, label='Processing Time')
        
        ax.set_xlabel('Request Number')
        ax.set_ylabel('Time (ms)')
        ax.set_title('Response Time Breakdown')
        ax.legend()
        plt.grid(True, alpha=0.3)
        return fig
    
    def plot_response_distribution(self):
        """Create response time distribution plot with network breakdown"""
        df = pd.DataFrame(self.results)
        successful_df = df[df['status'] == 'success']
        
        if successful_df.empty:
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.text(0.5, 0.5, 'No successful requests to plot', 
                   ha='center', va='center')
            ax.set_xlabel('Time (ms)')
            ax.set_ylabel('Frequency')
            ax.set_title('Response Time Distribution')
            return fig
            
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))
        
        # Total time distribution
        sns.histplot(data=successful_df, x='total_time', bins=30, 
                    color='blue', alpha=0.7, ax=ax1)
        ax1.set_xlabel('Total Time (ms)')
        ax1.set_ylabel('Frequency')
        ax1.set_title(f'Total Response Time\n(mean: {successful_df["total_time"].mean():.1f}ms)')
        ax1.grid(True, alpha=0.3)
        
        # Network time distribution
        sns.histplot(data=successful_df, x='network_time', bins=30,
                    color='red', alpha=0.7, ax=ax2)
        ax2.set_xlabel('Network Time (ms)')
        ax2.set_title(f'Network Time\n(mean: {successful_df["network_time"].mean():.1f}ms)')
        ax2.grid(True, alpha=0.3)
        
        # Processing time distribution
        sns.histplot(data=successful_df, x='processing_time', bins=30,
                    color='green', alpha=0.7, ax=ax3)
        ax3.set_xlabel('Processing Time (ms)')
        ax3.set_title(f'Processing Time\n(mean: {successful_df["processing_time"].mean():.1f}ms)')
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def get_results_df(self):
        """Get results as DataFrame with network metrics"""
        df = pd.DataFrame(self.results)
        if not df.empty:
            # Calculate percentages
            total_time = df['total_time']
            df['network_percentage'] = (df['network_time'] / total_time * 100).round(2)
            df['processing_percentage'] = (df['processing_time'] / total_time * 100).round(2)
            
            # Add request number
            df['request_number'] = range(1, len(df) + 1)
            
            # Reorder columns
            columns = ['request_number', 'timestamp', 'total_time', 'network_time', 
                      'processing_time', 'network_percentage', 'processing_percentage',
                      'prediction', 'status', 'error']
            df = df[columns]
        return df 