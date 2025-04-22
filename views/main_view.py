import streamlit as st
from utils.visualization import (
    plot_feature_importance,
    plot_emission_comparison,
    create_gauge_chart,
    style_metric_cards
)

class MainView:
    def __init__(self, controller):
        self.controller = controller
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
            page = st.radio("Navigation", ["Prediction", "Analysis"])

        if page == "Prediction":
            self._show_prediction_page()
        else:
            self._show_analysis_page()

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