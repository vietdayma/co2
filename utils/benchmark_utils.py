import time
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import requests
import streamlit as st

class BenchmarkUtils:
    def __init__(self):
        self.results = []
        self.start_time = None
        self.end_time = None
        self.model = None
        
    def start_benchmark(self):
        """Start the benchmark session"""
        self.start_time = time.time()
        self.results = []
        
    def measure_network_time(self):
        """Measure network latency"""
        try:
            start = time.time()
            # Gửi request đến health endpoint của app
            requests.get(st.get_option('server.baseUrlPath') + '/healthz', timeout=1)
            return time.time() - start
        except:
            return 0  # Return 0 if can't measure network time
            
    def measure_streamlit_overhead(self):
        """Measure Streamlit overhead"""
        start = time.time()
        # Trigger một Streamlit rerun nhỏ
        st.empty()
        return time.time() - start
        
    def record_prediction(self, duration, prediction, status='success', error=None):
        """Record a single prediction result with detailed timing"""
        # Đo các thành phần thời gian
        network_time = self.measure_network_time()
        streamlit_time = self.measure_streamlit_overhead()
        processing_time = duration - network_time - streamlit_time
        
        self.results.append({
            'timestamp': datetime.now(),
            'total_duration': duration,
            'network_time': network_time,
            'processing_time': processing_time,
            'streamlit_overhead': streamlit_time,
            'prediction': prediction,
            'status': status,
            'error': error
        })
        
    def end_benchmark(self):
        """End the benchmark session"""
        self.end_time = time.time()
        
    def get_statistics(self):
        """Calculate detailed benchmark statistics"""
        df = pd.DataFrame(self.results)
        successful_df = df[df['status'] == 'success']
        
        total_time = self.end_time - self.start_time
        total_requests = len(df)
        successful_requests = len(successful_df)
        
        # Calculate average times for each component
        avg_network = successful_df['network_time'].mean() if not successful_df.empty else 0
        avg_processing = successful_df['processing_time'].mean() if not successful_df.empty else 0
        avg_streamlit = successful_df['streamlit_overhead'].mean() if not successful_df.empty else 0
        
        stats = {
            'total_time': total_time,
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'requests_per_second': total_requests / total_time,
            'success_rate': (successful_requests / total_requests) * 100,
            'avg_response_time': successful_df['total_duration'].mean() if not successful_df.empty else 0,
            'min_response_time': successful_df['total_duration'].min() if not successful_df.empty else 0,
            'max_response_time': successful_df['total_duration'].max() if not successful_df.empty else 0,
            'std_response_time': successful_df['total_duration'].std() if not successful_df.empty else 0,
            'avg_network_time': avg_network,
            'avg_processing_time': avg_processing,
            'avg_streamlit_overhead': avg_streamlit,
            'network_percentage': (avg_network / (avg_network + avg_processing + avg_streamlit)) * 100 if avg_network > 0 else 0,
            'processing_percentage': (avg_processing / (avg_network + avg_processing + avg_streamlit)) * 100 if avg_processing > 0 else 0,
            'streamlit_percentage': (avg_streamlit / (avg_network + avg_processing + avg_streamlit)) * 100 if avg_streamlit > 0 else 0
        }
        
        return stats
    
    def plot_response_times(self):
        """Create detailed response time trend plot"""
        df = pd.DataFrame(self.results)
        successful_df = df[df['status'] == 'success']
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot stacked times
        x = range(len(successful_df))
        ax.fill_between(x, 0, successful_df['network_time']*1000, alpha=0.3, label='Network Time')
        ax.fill_between(x, successful_df['network_time']*1000, 
                       (successful_df['network_time'] + successful_df['processing_time'])*1000, 
                       alpha=0.3, label='Processing Time')
        ax.fill_between(x, (successful_df['network_time'] + successful_df['processing_time'])*1000,
                       successful_df['total_duration']*1000, 
                       alpha=0.3, label='Streamlit Overhead')
        
        ax.set_xlabel('Request Number')
        ax.set_ylabel('Response Time (ms)')
        ax.set_title('Response Time Breakdown Trend')
        ax.legend()
        return fig
    
    def plot_response_distribution(self):
        """Create detailed response time distribution plot"""
        df = pd.DataFrame(self.results)
        successful_df = df[df['status'] == 'success']
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        # Network time distribution
        ax1.hist(successful_df['network_time']*1000, bins=30, alpha=0.7)
        ax1.set_title('Network Time Distribution')
        ax1.set_xlabel('Time (ms)')
        
        # Processing time distribution
        ax2.hist(successful_df['processing_time']*1000, bins=30, alpha=0.7)
        ax2.set_title('Processing Time Distribution')
        ax2.set_xlabel('Time (ms)')
        
        # Streamlit overhead distribution
        ax3.hist(successful_df['streamlit_overhead']*1000, bins=30, alpha=0.7)
        ax3.set_title('Streamlit Overhead Distribution')
        ax3.set_xlabel('Time (ms)')
        
        plt.tight_layout()
        return fig
    
    def get_results_df(self):
        """Get detailed results as DataFrame"""
        return pd.DataFrame(self.results) 