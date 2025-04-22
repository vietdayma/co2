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
        self.app_url = "https://co2lan1.streamlit.app"
        
    def start_benchmark(self):
        """Start the benchmark session"""
        self.start_time = time.time()
        self.results = []
        
    def measure_network_time(self):
        """Measure network latency to Streamlit Cloud"""
        try:
            start = time.time()
            response = requests.get(self.app_url, timeout=5)
            duration = time.time() - start
            return duration if response.ok else 0
        except Exception as e:
            st.warning(f"Network measurement error: {str(e)}")
            return 0
            
    def measure_streamlit_overhead(self):
        """Measure Streamlit overhead"""
        try:
            start = time.time()
            placeholder = st.empty()
            placeholder.empty()
            duration = time.time() - start
            return duration
        except Exception as e:
            st.warning(f"Streamlit overhead measurement error: {str(e)}")
            return 0
        
    def record_prediction(self, duration, prediction, status='success', error=None):
        """Record a single prediction result with detailed timing"""
        try:
            # Measure individual components
            network_start = time.time()
            network_time = self.measure_network_time()
            
            processing_start = time.time()
            processing_time = time.time() - processing_start
            
            streamlit_time = self.measure_streamlit_overhead()
            
            # Calculate remaining time
            remaining_time = max(0, duration - (network_time + processing_time + streamlit_time))
            
            # Debug information
            if st.session_state.get('debug_mode', False):
                st.write(f"""
                Debug Timing (ms):
                - Total: {duration*1000:.2f}
                - Network: {network_time*1000:.2f}
                - Processing: {processing_time*1000:.2f}
                - Streamlit: {streamlit_time*1000:.2f}
                - Other: {remaining_time*1000:.2f}
                """)
            
            self.results.append({
                'timestamp': datetime.now(),
                'total_duration': duration,
                'network_time': network_time,
                'processing_time': processing_time,
                'streamlit_overhead': streamlit_time,
                'other_time': remaining_time,
                'prediction': prediction,
                'status': status,
                'error': error
            })
            
        except Exception as e:
            st.error(f"Error recording prediction: {str(e)}")
            self.results.append({
                'timestamp': datetime.now(),
                'total_duration': duration,
                'network_time': 0,
                'processing_time': 0,
                'streamlit_overhead': 0,
                'other_time': duration,
                'prediction': prediction,
                'status': 'error',
                'error': str(e)
            })
        
    def end_benchmark(self):
        """End the benchmark session"""
        self.end_time = time.time()
        
    def get_statistics(self):
        """Calculate detailed benchmark statistics"""
        try:
            df = pd.DataFrame(self.results)
            successful_df = df[df['status'] == 'success']
            
            total_time = self.end_time - self.start_time
            total_requests = len(df)
            successful_requests = len(successful_df)
            
            # Calculate component averages
            avg_network = successful_df['network_time'].mean() if not successful_df.empty else 0
            avg_processing = successful_df['processing_time'].mean() if not successful_df.empty else 0
            avg_streamlit = successful_df['streamlit_overhead'].mean() if not successful_df.empty else 0
            avg_other = successful_df['other_time'].mean() if not successful_df.empty else 0
            
            # Calculate total average time
            avg_total = avg_network + avg_processing + avg_streamlit + avg_other
            
            # Calculate percentages
            network_pct = (avg_network / avg_total * 100) if avg_total > 0 else 0
            processing_pct = (avg_processing / avg_total * 100) if avg_total > 0 else 0
            streamlit_pct = (avg_streamlit / avg_total * 100) if avg_total > 0 else 0
            other_pct = (avg_other / avg_total * 100) if avg_total > 0 else 0
            
            stats = {
                'total_time': total_time,
                'total_requests': total_requests,
                'successful_requests': successful_requests,
                'requests_per_second': total_requests / total_time if total_time > 0 else 0,
                'success_rate': (successful_requests / total_requests * 100) if total_requests > 0 else 0,
                'avg_response_time': successful_df['total_duration'].mean() if not successful_df.empty else 0,
                'min_response_time': successful_df['total_duration'].min() if not successful_df.empty else 0,
                'max_response_time': successful_df['total_duration'].max() if not successful_df.empty else 0,
                'std_response_time': successful_df['total_duration'].std() if not successful_df.empty else 0,
                'avg_network_time': avg_network,
                'avg_processing_time': avg_processing,
                'avg_streamlit_overhead': avg_streamlit,
                'avg_other_time': avg_other,
                'network_percentage': network_pct,
                'processing_percentage': processing_pct,
                'streamlit_percentage': streamlit_pct,
                'other_percentage': other_pct
            }
            
            return stats
            
        except Exception as e:
            st.error(f"Error calculating statistics: {str(e)}")
            return {
                'total_time': 0,
                'total_requests': 0,
                'successful_requests': 0,
                'requests_per_second': 0,
                'success_rate': 0,
                'avg_response_time': 0,
                'min_response_time': 0,
                'max_response_time': 0,
                'std_response_time': 0,
                'avg_network_time': 0,
                'avg_processing_time': 0,
                'avg_streamlit_overhead': 0,
                'avg_other_time': 0,
                'network_percentage': 0,
                'processing_percentage': 0,
                'streamlit_percentage': 0,
                'other_percentage': 0
            }
    
    def plot_response_times(self):
        """Create detailed response time trend plot"""
        try:
            df = pd.DataFrame(self.results)
            successful_df = df[df['status'] == 'success']
            
            if successful_df.empty:
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.text(0.5, 0.5, 'No successful requests to display',
                       horizontalalignment='center',
                       verticalalignment='center')
                return fig
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Plot stacked times
            x = range(len(successful_df))
            
            # Create stacked area plot
            ax.fill_between(x, 0, successful_df['network_time']*1000, 
                          alpha=0.3, label='Network Time', color='blue')
            
            ax.fill_between(x, successful_df['network_time']*1000,
                          (successful_df['network_time'] + successful_df['processing_time'])*1000,
                          alpha=0.3, label='Processing Time', color='green')
            
            ax.fill_between(x, (successful_df['network_time'] + successful_df['processing_time'])*1000,
                          (successful_df['network_time'] + successful_df['processing_time'] + 
                           successful_df['streamlit_overhead'])*1000,
                          alpha=0.3, label='Streamlit Overhead', color='orange')
            
            ax.fill_between(x, (successful_df['network_time'] + successful_df['processing_time'] + 
                               successful_df['streamlit_overhead'])*1000,
                          successful_df['total_duration']*1000,
                          alpha=0.3, label='Other Time', color='red')
            
            ax.set_xlabel('Request Number')
            ax.set_ylabel('Response Time (ms)')
            ax.set_title('Response Time Breakdown Trend')
            ax.legend()
            
            return fig
            
        except Exception as e:
            st.error(f"Error plotting response times: {str(e)}")
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.text(0.5, 0.5, f'Error creating plot: {str(e)}',
                   horizontalalignment='center',
                   verticalalignment='center')
            return fig
    
    def plot_response_distribution(self):
        """Create detailed response time distribution plot"""
        try:
            df = pd.DataFrame(self.results)
            successful_df = df[df['status'] == 'success']
            
            if successful_df.empty:
                fig, ax = plt.subplots(figsize=(15, 5))
                ax.text(0.5, 0.5, 'No successful requests to display',
                       horizontalalignment='center',
                       verticalalignment='center')
                return fig
            
            fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20, 5))
            
            # Network time distribution
            ax1.hist(successful_df['network_time']*1000, bins=30, alpha=0.7, color='blue')
            ax1.set_title('Network Time Distribution')
            ax1.set_xlabel('Time (ms)')
            
            # Processing time distribution
            ax2.hist(successful_df['processing_time']*1000, bins=30, alpha=0.7, color='green')
            ax2.set_title('Processing Time Distribution')
            ax2.set_xlabel('Time (ms)')
            
            # Streamlit overhead distribution
            ax3.hist(successful_df['streamlit_overhead']*1000, bins=30, alpha=0.7, color='orange')
            ax3.set_title('Streamlit Overhead Distribution')
            ax3.set_xlabel('Time (ms)')
            
            # Other time distribution
            ax4.hist(successful_df['other_time']*1000, bins=30, alpha=0.7, color='red')
            ax4.set_title('Other Time Distribution')
            ax4.set_xlabel('Time (ms)')
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            st.error(f"Error plotting distributions: {str(e)}")
            fig, ax = plt.subplots(figsize=(15, 5))
            ax.text(0.5, 0.5, f'Error creating plot: {str(e)}',
                   horizontalalignment='center',
                   verticalalignment='center')
            return fig
    
    def get_results_df(self):
        """Get detailed results as DataFrame"""
        return pd.DataFrame(self.results) 