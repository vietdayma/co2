# CO2 Emission Prediction

This application predicts CO2 emissions for vehicles based on their specifications using machine learning.

## Features

- Predict CO2 emissions based on vehicle specifications
- Analyze model performance and feature importance
- Benchmark testing for model performance evaluation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git
cd REPOSITORY_NAME
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application locally:
```bash
streamlit run app.py
```

The application will be available at http://localhost:8501

## Online Demo

You can access the online demo at: https://share.streamlit.io/YOUR_USERNAME/REPOSITORY_NAME/main/app.py

## Input Parameters

- Engine Size (L)
- Number of Cylinders
- Fuel Consumption (L/100 km)
- Horsepower
- Vehicle Weight (kg)
- Year of Manufacture

## Features

1. **Prediction**: Get instant CO2 emission predictions based on vehicle specifications
2. **Analysis**: View model performance metrics and feature importance
3. **Benchmark**: Run performance tests to evaluate model efficiency

## Technologies Used

- Python
- Streamlit
- Scikit-learn
- Pandas
- NumPy
- Matplotlib
- Seaborn

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Project Structure

```
co2-emission-predictor/
├── app.py                  # Main application file
├── models/                 # Model-related code
│   └── emission_model.py
├── views/                  # View-related code
│   └── main_view.py
├── controllers/            # Controller-related code
│   └── emission_controller.py
├── utils/                  # Utility functions
│   └── visualization.py
├── static/                 # Static files
│   └── images/
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## Model Features

The model takes into account the following vehicle specifications:
- Engine Size (L)
- Number of Cylinders
- Fuel Consumption (L/100 km)
- Horsepower
- Vehicle Weight (kg)
- Vehicle Year

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 