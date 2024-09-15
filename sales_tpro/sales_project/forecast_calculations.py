import pandas as pd

def load_forecast_sales_data(file_path):
    sales_df = pd.read_csv(file_path, delimiter=';')
    if sales_df.empty:
        raise ValueError("Файл продаж пустой.")
    return sales_df

def load_stock_data(file_path):
    stock_df = pd.read_csv(file_path, delimiter=';')
    if stock_df.empty:
        raise ValueError("Файл запасов пустой.")
    return stock_df

def calculate_forecast(sales_df, stock_df, months=3):
    grouped_sales = sales_df.groupby('product_id')['quantity'].sum().reset_index()
    forecast_df = pd.merge(stock_df, grouped_sales, on='product_id', how='left')
    
    # Заполняем пропущенные значения
    forecast_df['quantity'] = forecast_df['quantity'].fillna(0)
    
    # Создаем прогноз для каждого месяца
    for month in range(1, months + 1):
        forecast_df[f'Month_{month}'] = (forecast_df['quantity'] / months).round()

    # Проверяем наличие столбцов
    required_columns = [f'Month_{month}' for month in range(1, months + 1)]
    print("DataFrame columns after forecast:", forecast_df.columns)
    
    for col in required_columns:
        if col not in forecast_df.columns:
            forecast_df[col] = 0

    print("DataFrame columns after adding missing ones:", forecast_df.columns)
    
    forecast_df['forecast_sales'] = forecast_df[required_columns].sum(axis=1)
    
    return forecast_df[['product_id', 'Name'] + required_columns + ['forecast_sales']]
