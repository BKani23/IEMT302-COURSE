# ml_example.py
"""
A minimal machine learning example using scikit-learn.

We predict a target value (y) from a single feature (x) using linear regression.
"""

from sklearn.linear_model import LinearRegression
import numpy as np

# Sample dataset
# x = feature (hours studied)
# y = target (score on test)
x = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)  # reshaped to 2D array
y = np.array([2, 4, 5, 4, 5])

# Create the model
model = LinearRegression()

# Train (fit) the model
model.fit(x, y)

# Make predictions
x_test = np.array([6, 7]).reshape(-1, 1)
y_pred = model.predict(x_test)

print("Trained model coefficients:")
print("Slope:", model.coef_[0])
print("Intercept:", model.intercept_)
print()
print("Predictions for 6 and 7 hours studied:", y_pred)
