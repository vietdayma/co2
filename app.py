from controllers.emission_controller import EmissionController
from utils.benchmark import BenchmarkTester
import streamlit as st

def main():
    st.set_page_config(page_title="CO2 Emission Prediction", layout="wide")
    
    # Initialize controller
    controller = EmissionController()
    
    # Train the model
    try:
        test_score = controller.initialize_model('co2 Emissions.csv')
        st.success(f"Model trained successfully. Test score: {test_score:.3f}")
    except Exception as e:
        st.error(f"Error training model: {str(e)}")
        return

    # Initialize benchmark tester
    benchmark_tester = BenchmarkTester(controller)
    
    # Main interface
    st.title("CO2 Emission Prediction")
    
    # Create tabs
    tab1, tab2 = st.tabs(["Prediction", "Benchmark"])
    
    with tab1:
        st.header("Make Prediction")
        # Add your prediction interface here
        engine_size = st.number_input("Engine Size (L)", min_value=0.0, max_value=10.0, value=2.0)
        cylinders = st.number_input("Cylinders", min_value=1, max_value=16, value=4)
        fuel_consumption = st.number_input("Fuel Consumption Comb (L/100 km)", min_value=0.0, max_value=30.0, value=8.0)
        horsepower = st.number_input("Horsepower", min_value=0, max_value=1000, value=200)
        weight = st.number_input("Weight (kg)", min_value=500, max_value=5000, value=1500)
        year = st.number_input("Year", min_value=1900, max_value=2024, value=2023)
        
        if st.button("Predict"):
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
    
    with tab2:
        st.header("Benchmark Testing")
        n_iterations = st.slider("Number of iterations", min_value=100, max_value=5000, value=1000, step=100)
        
        if st.button("Run Benchmark"):
            stats, df = benchmark_tester.run_benchmark(n_iterations)
            benchmark_tester.generate_report(stats, df)

if __name__ == "__main__":
    main() 