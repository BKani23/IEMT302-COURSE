# Simple Machine Learning Example 📊

A minimal Python project demonstrating **Linear Regression** using **scikit-learn**.  
The script predicts a student’s test score based on the number of hours they studied.  

Example: `Predict the test score for a student who studied 6 hours.` → Output: `5.8`

---

## What problem does this solve?

Learning the basics of machine learning workflows can be confusing. This project provides a **hands-on, minimal example** to show how a model learns from data, makes predictions, and how to interpret results.

---

## How it works (ML)

- Uses **scikit-learn's LinearRegression** model.
- Fits a small dataset of hours studied vs. scores.
- Predicts scores for new inputs (hours studied).
- Prints model parameters: slope & intercept.
- Visualizes data points, regression line, and predictions using `matplotlib`.

---

## Features

- Train a linear regression model on a small dataset.
- Predict scores for new hours studied.
- Inspect model parameters (slope & intercept).
- Visualize original data and regression line with predictions.

---

## Setup — Step by Step

### 1) Clone or download the project
```bash
git clone https://github.com/BKani23/IEMT302-COURSE.git
cd IEMT302-COURSE/machine-learning-task 
```


### 2) Install dependencies
```bash
pip install numpy scikit-learn matplotlib
```

### 3) Run the script
```bash
python ml_example.py
```


Expected Output
```
Trained model coefficients:
Slope: 0.6
Intercept: 2.2

Predictions for 6 and 7 hours studied: [5.8 6.4]

```

Dataset

| Hours Studied | Score |
| ------------- | ----- |
| 1             | 2     |
| 2             | 4     |
| 3             | 5     |
| 4             | 4     |
| 5             | 5     |


