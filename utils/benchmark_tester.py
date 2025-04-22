import time
import psutil
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from controllers.emission_controller import EmissionController

class BenchmarkTester:
    def __init__(self, controller: EmissionController):
        self.controller = controller
        
    def run_benchmarks(self):
        """Run a series of benchmark tests on the model."""
        # Get test data from the controller
        X_test = self.controller.model.X_test
        y_test = self.controller.model.y_test
        
        # Measure prediction time
        start_time = time.time()
        y_pred = self.controller.model.predict(X_test)
        prediction_time = time.time() - start_time
        
        # Calculate metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Measure memory usage
        process = psutil.Process()
        memory_usage = process.memory_info().rss / 1024 / 1024  # Convert to MB
        
        return {
            'mae': mae,
            'mse': mse,
            'r2': r2,
            'prediction_time': prediction_time,
            'memory_usage': memory_usage
        } 