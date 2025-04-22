import streamlit as st
from utils.visualization import (
    plot_feature_importance,
    plot_emission_comparison,
    create_gauge_chart,
    style_metric_cards
)
import pandas as pd
import time
import numpy as np
from utils.benchmark_utils import BenchmarkUtils

class MainView:
    def __init__(self, controller):
        self.controller = controller
        self.benchmark_utils = BenchmarkUtils()
        st.set_page_config(
            page_title="CO2 Emission Predictor",
            page_icon="🌍",
            layout="wide"
        )

    def show(self):
        """Display the main application interface"""
        # Add custom CSS
        st.markdown(style_metric_cards(), unsafe_allow_html=True)
        
        # Sidebar
        with st.sidebar:
            st.markdown("# 🚗 CO2 Emission Predictor")
            st.markdown("---")
            page = st.radio("Navigation", ["Prediction", "Analysis", "Benchmark"])

        if page == "Prediction":
            self._show_prediction_page()
        elif page == "Analysis":
            self._show_analysis_page()
        else:
            self._show_benchmark_page()

    def _show_prediction_page(self):
        """Display the prediction interface"""
        st.title("🌍 Predict Vehicle CO2 Emissions")
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin-bottom: 20px'>
            <h4 style='margin: 0; color: #0f4c81'>Enter your vehicle specifications to predict CO2 emissions</h4>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            engine_size = st.number_input("🔧 Engine Size (L)", 
                                        min_value=0.1, 
                                        max_value=10.0, 
                                        value=2.0,
                                        step=0.1)
            
            cylinders = st.number_input("⚙️ Number of Cylinders",
                                      min_value=2,
                                      max_value=16,
                                      value=4,
                                      step=1)
            
            fuel_consumption = st.number_input("⛽ Fuel Consumption (L/100 km)",
                                             min_value=1.0,
                                             max_value=30.0,
                                             value=8.0,
                                             step=0.1)

        with col2:
            horsepower = st.number_input("🏎️ Horsepower",
                                       min_value=50,
                                       max_value=1000,
                                       value=200,
                                       step=10)
            
            weight = st.number_input("⚖️ Vehicle Weight (kg)",
                                   min_value=500,
                                   max_value=5000,
                                   value=1500,
                                   step=100)
            
            year = st.number_input("📅 Vehicle Year",
                                 min_value=2015,
                                 max_value=2024,
                                 value=2023,
                                 step=1)

        if st.button("🔍 Predict Emissions", type="primary"):
            features = {
                'Engine Size(L)': engine_size,
                'Cylinders': cylinders,
                'Fuel Consumption Comb (L/100 km)': fuel_consumption,
                'Horsepower': horsepower,
                'Weight (kg)': weight,
                'Year': year
            }

            try:
                prediction = self.controller.predict_emission(features)
                avg_emission = self.controller.get_average_emission()
                rating = self.controller.get_emission_rating(prediction)
                tips = self.controller.get_eco_tips(prediction)

                # Display results
                st.markdown("### 📊 Results")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <h3>🎯 Predicted CO2 Emission</h3>
                            <div class="metric-value">{prediction:.1f} g/km</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col2:
                    rating_colors = {
                        'A': '🟢', 'B': '🟡', 'C': '🟠',
                        'D': '🔴', 'E': '🟣', 'F': '⚫'
                    }
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <h3>📈 Emission Rating</h3>
                            <div class="metric-value">{rating_colors.get(rating, '⚪')} {rating}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col3:
                    comparison = ((prediction - avg_emission) / avg_emission * 100)
                    icon = "🔽" if comparison < 0 else "🔼"
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <h3>📊 Compared to Average</h3>
                            <div class="metric-value">
                                {icon} {'+' if comparison > 0 else ''}{comparison:.1f}%
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # Visualization
                st.markdown("### 📈 Visualization")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.pyplot(plot_emission_comparison(prediction, avg_emission))
                
                with col2:
                    st.pyplot(create_gauge_chart(prediction, 0, 300, "Emission Meter"))

                # Eco Tips
                st.markdown("### 🌱 Eco-friendly Tips")
                for tip in tips:
                    st.markdown(f"- {tip}")

            except Exception as e:
                st.error(f"Error making prediction: {str(e)}")

    def _show_analysis_page(self):
        """Display the analysis interface"""
        st.title("📊 CO2 Emission Analysis")
        
        # Feature Importance
        st.subheader("🎯 Feature Importance Analysis")
        try:
            importance_dict = self.controller.get_feature_importance()
            st.pyplot(plot_feature_importance(importance_dict))
            
            # Add explanation
            st.markdown("""
            <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin-top: 20px'>
                <h4 style='margin: 0; color: #0f4c81'>Understanding Feature Importance</h4>
                <p style='margin-top: 10px'>
                    This chart shows how much each vehicle characteristic influences CO2 emissions. 
                    Longer bars indicate stronger influence on the prediction.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error getting feature importance: {str(e)}")

        # Additional analysis sections can be added here 

    def _show_benchmark_page(self):
        st.title("Benchmark")
        
        col1, col2 = st.columns(2)
        with col1:
            num_requests = st.number_input("Number of requests", min_value=1, value=1000)
        with col2:
            batch_size = st.number_input("Batch size", min_value=1, value=100)
        
        if st.button("Run Benchmark"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            timing_log = st.empty()
            
            benchmark = BenchmarkUtils()
            benchmark.start_benchmark()
            
            for i in range(num_requests):
                try:
                    # Measure total request time
                    request_start = time.perf_counter_ns()
                    
                    # Measure processing time
                    process_start = time.perf_counter_ns()
                    prediction = self.controller.predict_emission([100, 100, 100, 100])
                    process_end = time.perf_counter_ns()
                    
                    # Calculate timing in milliseconds
                    total_time = (time.perf_counter_ns() - request_start) / 1_000_000
                    processing_time = (process_end - process_start) / 1_000_000
                    
                    # Network time is the difference, with a minimum threshold
                    network_time = max(0.1, total_time - processing_time)
                    
                    timing_data = {
                        'total_time': total_time,
                        'network_time': network_time,
                        'processing_time': processing_time,
                        'prediction': prediction[0] if prediction is not None else None,
                        'status': 'success' if prediction is not None else 'error'
                    }
                except Exception as e:
                    # If there's an error, estimate network time as 30% of total
                    total_time = (time.perf_counter_ns() - request_start) / 1_000_000
                    timing_data = {
                        'total_time': total_time,
                        'network_time': total_time * 0.3,
                        'processing_time': total_time * 0.7,
                        'prediction': None,
                        'status': 'error',
                        'error': str(e)
                    }
                
                benchmark.record_prediction(timing_data)
                
                # Update progress
                progress = (i + 1) / num_requests
                progress_bar.progress(progress)
                status_text.text(f"Processing request {i+1}/{num_requests}")
                
                # Show detailed timing log every batch_size requests
                if (i + 1) % batch_size == 0:
                    stats = benchmark.get_statistics()
                    timing_log.text(
                        f"Batch {(i+1)//batch_size} metrics:\n"
                        f"Total Time: {stats['avg_total_time']:.1f}ms\n"
                        f"Network Time: {stats['avg_network_time']:.1f}ms ({stats['avg_network_time']/stats['avg_total_time']*100:.1f}%)\n"
                        f"Processing Time: {stats['avg_processing_time']:.1f}ms ({stats['avg_processing_time']/stats['avg_total_time']*100:.1f}%)\n"
                        f"Success Rate: {stats['success_rate']:.1f}%"
                    )
            
            benchmark.end_benchmark()
            stats = benchmark.get_statistics()
            
            st.success("Benchmark completed!")
            
            # Display statistics
            st.header("Results")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Time", f"{stats['total_time']:.2f}s")
                st.metric("Success Rate", f"{stats['success_rate']:.1f}%")
            with col2:
                st.metric("Requests/Second", f"{stats['requests_per_second']:.1f}")
                st.metric("Network %", f"{stats['avg_network_time']/stats['avg_total_time']*100:.1f}%")
            with col3:
                st.metric("Total Requests", stats['total_requests'])
                st.metric("Processing %", f"{stats['avg_processing_time']/stats['avg_total_time']*100:.1f}%")
            
            # Plot response times
            st.subheader("Response Time Trend")
            fig = benchmark.plot_response_times()
            st.pyplot(fig)
            
            # Plot response time distribution
            st.subheader("Response Time Distribution")
            fig = benchmark.plot_response_distribution()
            st.pyplot(fig)
            
            # Show detailed results table
            st.subheader("Detailed Results")
            results_df = benchmark.get_results_df()
            st.dataframe(results_df) 