import pandas as pd
from sklearn.linear_model import LinearRegression
from sales_project.predictor import predict_sales

def load_sales_data(file_path):
    return pd.read_excel(file_path)

def perform_prediction(data):
    model = LinearRegression()
    X = data['month'].values.reshape(-1, 1)
    y = data['sales']
    model.fit(X, y)
    return model.predict(X)