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
        st.title("Performance Benchmark 📊")
        
        col1, col2 = st.columns(2)
        with col1:
            n_requests = st.number_input("Number of Requests", min_value=1, max_value=10000, value=1000)
        
        with col2:
            test_mode = st.selectbox("Test Mode", ["Fixed Parameters", "Random Parameters"])
        
        if test_mode == "Fixed Parameters":
            engine_size = st.number_input("Engine Size (L)", min_value=0.0, max_value=10.0, value=2.0)
            cylinders = st.number_input("Cylinders", min_value=0, max_value=16, value=4)
            fuel_consumption = st.number_input("Fuel Consumption (L/100km)", min_value=0.0, max_value=30.0, value=9.0)
        
        if st.button("Run Benchmark"):
            self.benchmark_utils.start_benchmark()
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(n_requests):
                if test_mode == "Random Parameters":
                    engine_size = np.random.uniform(1.0, 8.0)
                    cylinders = np.random.randint(3, 12)
                    fuel_consumption = np.random.uniform(4.0, 20.0)
                
                start_time = time.time()
                try:
                    prediction = self.controller.predict(engine_size, cylinders, fuel_consumption)
                    duration = time.time() - start_time
                    self.benchmark_utils.record_prediction(duration, prediction)
                except Exception as e:
                    self.benchmark_utils.record_prediction(time.time() - start_time, None, 
                                                         status='error', error=str(e))
                
                progress = (i + 1) / n_requests
                progress_bar.progress(progress)
                status_text.text(f"Processing request {i+1}/{n_requests}")
            
            self.benchmark_utils.end_benchmark()
            stats = self.benchmark_utils.get_statistics()
            
            st.success("Benchmark completed!")
            
            # Display overall statistics
            st.subheader("Overall Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Time", f"{stats['total_time']:.2f}s")
                st.metric("Success Rate", f"{stats['success_rate']:.1f}%")
            with col2:
                st.metric("Requests/Second", f"{stats['requests_per_second']:.1f}")
                st.metric("Avg Response Time", f"{stats['avg_response_time']*1000:.1f}ms")
            with col3:
                st.metric("Min Response Time", f"{stats['min_response_time']*1000:.1f}ms")
                st.metric("Max Response Time", f"{stats['max_response_time']*1000:.1f}ms")
            
            # Display time breakdown
            st.subheader("Time Breakdown")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Network Time", 
                         f"{stats['avg_network_time']*1000:.1f}ms",
                         f"{stats['network_percentage']:.1f}%")
            with col2:
                st.metric("Processing Time", 
                         f"{stats['avg_processing_time']*1000:.1f}ms",
                         f"{stats['processing_percentage']:.1f}%")
            with col3:
                st.metric("Streamlit Overhead", 
                         f"{stats['avg_streamlit_overhead']*1000:.1f}ms",
                         f"{stats['streamlit_percentage']:.1f}%")
            
            # Display plots
            st.subheader("Response Time Breakdown Trend")
            st.pyplot(self.benchmark_utils.plot_response_times())
            
            st.subheader("Response Time Distributions")
            st.pyplot(self.benchmark_utils.plot_response_distribution())
            
            # Download results
            results_df = self.benchmark_utils.get_results_df()
            st.download_button(
                "Download Detailed Results CSV",
                results_df.to_csv().encode('utf-8'),
                "benchmark_results.csv",
                "text/csv",
                key='download-csv'
            ) 