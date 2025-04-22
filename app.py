from controllers.emission_controller import EmissionController
from utils.benchmark import BenchmarkTester
import streamlit as st

def main():
    st.set_page_config(page_title="CO2 Emission Prediction", layout="wide")
    
    # Initialize controller and benchmark tester
    controller = EmissionController()
    benchmark_tester = BenchmarkTester(controller)
    
    # Train the model
    try:
        test_score = controller.initialize_model('co2 Emissions.csv')
        st.success(f"Model trained successfully. Test score: {test_score:.3f}")
    except Exception as e:
        st.error(f"Error training model: {str(e)}")
        return

    # Main interface
    st.title("CO2 Emission Prediction")
    st.write("This application predicts CO2 emissions for vehicles based on their specifications.")
    
    # Input form
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            engine_size = st.number_input("Engine Size (L)", min_value=0.0, max_value=10.0, value=2.0)
            cylinders = st.number_input("Cylinders", min_value=1, max_value=16, value=4)
            fuel_consumption = st.number_input("Fuel Consumption Comb (L/100 km)", min_value=0.0, max_value=30.0, value=8.0)
            
        with col2:
            horsepower = st.number_input("Horsepower", min_value=0, max_value=1000, value=200)
            weight = st.number_input("Weight (kg)", min_value=500, max_value=5000, value=1500)
            year = st.number_input("Year", min_value=1900, max_value=2024, value=2023)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            predict_button = st.form_submit_button("Predict")
        with col2:
            analyze_button = st.form_submit_button("Analyze")
        with col3:
            benchmark_button = st.form_submit_button("Run Benchmark")
            
    # Handle button clicks
    if predict_button:
        test_data = {
            'Engine Size(L)': engine_size,
            'Cylinders': cylinders,
            'Fuel Consumption Comb (L/100 km)': fuel_consumption,
            'Horsepower': horsepower,
            'Weight (kg)': weight,
            'Year': year
        }
        try:
            prediction = controller.predict_emission(test_data)
            st.success(f"Predicted CO2 Emission: {prediction:.2f} g/km")
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")
            
    elif analyze_button:
        st.write("### Analysis Results")
        st.write("Feature importance and analysis visualization would go here")
        # Add your analysis visualization code here
        
    elif benchmark_button:
        st.write("### Running Benchmark Tests")
        with st.spinner("Running benchmark tests..."):
            stats, df = benchmark_tester.run_benchmark(n_iterations=1000)
            benchmark_tester.generate_report(stats, df)

if __name__ == "__main__":
    main() 