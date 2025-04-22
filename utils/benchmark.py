import time
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
import matplotlib.pyplot as plt

class BenchmarkTester:
    def __init__(self, controller):
        self.controller = controller
        self.results = []
        
    def run_benchmark(self, n_iterations=1000):
        """Chạy benchmark với n lần lặp"""
        
        # Chuẩn bị dữ liệu test mẫu
        test_data = {
            'Engine Size(L)': 2.0,
            'Cylinders': 4,
            'Fuel Consumption Comb (L/100 km)': 8.0,
            'Horsepower': 200,
            'Weight (kg)': 1500,
            'Year': 2023
        }
        
        total_start = time.time()
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(n_iterations):
            # Đo thời gian cho mỗi lần dự đoán
            start_time = time.time()
            
            try:
                prediction = self.controller.predict_emission(test_data)
                status = 'success'
            except Exception as e:
                prediction = None
                status = f'error: {str(e)}'
            
            end_time = time.time()
            
            # Lưu kết quả
            self.results.append({
                'iteration': i + 1,
                'timestamp': datetime.now(),
                'execution_time': end_time - start_time,
                'prediction': prediction,
                'status': status
            })
            
            # Cập nhật progress bar
            progress = (i + 1) / n_iterations
            progress_bar.progress(progress)
            status_text.text(f'Đang xử lý: {i + 1}/{n_iterations} requests')
        
        total_time = time.time() - total_start
        
        # Tính toán thống kê
        df = pd.DataFrame(self.results)
        successful_requests = df[df['status'] == 'success']
        
        stats = {
            'total_requests': n_iterations,
            'successful_requests': len(successful_requests),
            'failed_requests': n_iterations - len(successful_requests),
            'total_time': total_time,
            'avg_time': df['execution_time'].mean(),
            'min_time': df['execution_time'].min(),
            'max_time': df['execution_time'].max(),
            'std_time': df['execution_time'].std(),
            'requests_per_second': n_iterations / total_time
        }
        
        return stats, df
    
    def generate_report(self, stats, df):
        """Tạo báo cáo benchmark"""
        st.markdown("## 📊 Kết quả Benchmark")
        
        # Hiển thị thống kê tổng quan
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Tổng số requests", f"{stats['total_requests']:,}")
            st.metric("Requests thành công", f"{stats['successful_requests']:,}")
            st.metric("Requests thất bại", f"{stats['failed_requests']:,}")
        
        with col2:
            st.metric("Thời gian trung bình", f"{stats['avg_time']*1000:.2f} ms")
            st.metric("Thời gian tối thiểu", f"{stats['min_time']*1000:.2f} ms")
            st.metric("Thời gian tối đa", f"{stats['max_time']*1000:.2f} ms")
        
        with col3:
            st.metric("Tổng thời gian", f"{stats['total_time']:.2f} giây")
            st.metric("Requests/giây", f"{stats['requests_per_second']:.2f}")
            st.metric("Độ lệch chuẩn", f"{stats['std_time']*1000:.2f} ms")
        
        # Vẽ biểu đồ phân phối thời gian
        st.markdown("### 📈 Phân phối thời gian xử lý")
        fig_hist = self.plot_time_distribution(df)
        st.pyplot(fig_hist)
        
        # Vẽ biểu đồ thời gian theo thời gian
        st.markdown("### 📉 Thời gian xử lý theo thời gian")
        fig_time = self.plot_time_series(df)
        st.pyplot(fig_time)
        
        # Hiển thị dữ liệu chi tiết
        st.markdown("### 📋 Dữ liệu chi tiết")
        st.dataframe(df)
        
        # Tạo nút download
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Tải kết quả (CSV)",
            data=csv,
            file_name="benchmark_results.csv",
            mime="text/csv"
        )
    
    def plot_time_distribution(self, df):
        """Vẽ biểu đồ phân phối thời gian"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(df['execution_time'] * 1000, bins=50)
        ax.set_xlabel('Thời gian xử lý (ms)')
        ax.set_ylabel('Số lượng requests')
        ax.set_title('Phân phối thời gian xử lý')
        return fig
    
    def plot_time_series(self, df):
        """Vẽ biểu đồ thời gian theo thời gian"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df.index, df['execution_time'] * 1000)
        ax.set_xlabel('Request thứ #')
        ax.set_ylabel('Thời gian xử lý (ms)')
        ax.set_title('Thời gian xử lý theo thời gian')
        return fig 