import pandas as pd

def load_sales_data(file_path):
    """
    Загружает данные о продажах из CSV файла.
    
    :param file_path: Путь к CSV файлу с данными о продажах.
    :return: DataFrame с данными о продажах.
    :raises ValueError: Если файл пустой.
    """
    sales_df = pd.read_csv(file_path, delimiter=';')
    if sales_df.empty:
        raise ValueError("Файл продаж пустой.")
    return sales_df

def load_supplier_data(file_path):
    """
    Загружает данные о поставщиках из CSV файла.
    
    :param file_path: Путь к CSV файлу с данными о поставщиках.
    :return: DataFrame с данными о поставщиках.
    :raises ValueError: Если файл пустой.
    """
    supplier_df = pd.read_csv(file_path, delimiter=';')
    if supplier_df.empty:
        raise ValueError("Файл поставщиков пустой.")
    return supplier_df

def calculate_profitability(sales_df, supplier_df):
    """
    Рассчитывает доходность на основе данных о продажах и поставщиках.
    
    :param sales_df: DataFrame с данными о продажах.
    :param supplier_df: DataFrame с данными о поставщиках.
    :return: DataFrame с добавленными расчетами доходности.
    """
    # Outer join для объединения данных по всем продуктам
    merged_data = pd.merge(sales_df, supplier_df, on='product_id', how='outer')

    # Преобразование типов данных и обработка пропусков
    merged_data['quantity'] = pd.to_numeric(merged_data['quantity'], errors='coerce').fillna(0)
    merged_data['price2'] = pd.to_numeric(merged_data['price2'].str.replace(',', '.'), errors='coerce').fillna(0)

    # Рассчитываем доход как quantity * price2
    merged_data['revenue'] = merged_data['quantity'] * merged_data['price2']
    
    # Предупреждение, если у некоторых продуктов отсутствует информация о цене
    if merged_data['price2'].isnull().any():
        print("Внимание: У некоторых продуктов отсутствует информация о цене.")
    
    return merged_data

def abc_xyz_classification(data):
    """
    Классифицирует данные по методологии ABC/XYZ.
    
    :param data: DataFrame с данными о продажах и доходности.
    :return: DataFrame с добавленными категориями ABC и XYZ.
    """
    # Сортировка данных по доходности в порядке убывания
    data = data.sort_values('revenue', ascending=False)
    
    # Рассчитываем кумулятивный процент доходности
    data['cumulative_revenue'] = data['revenue'].cumsum()
    data['cumulative_revenue_percentage'] = data['cumulative_revenue'] / data['revenue'].sum()

    # Классификация ABC на основе кумулятивного дохода
    data['ABC'] = pd.cut(data['cumulative_revenue_percentage'], bins=[0, 0.7, 0.9, 1], labels=['A', 'B', 'C'], right=False)
    
    # Классификация XYZ на основе стандартного отклонения количества
    data['std_quantity'] = data.groupby('product_id')['quantity'].transform('std').fillna(0)
    data['XYZ'] = pd.cut(data['std_quantity'], bins=[-float('inf'), 1, 2, float('inf')], labels=['X', 'Y', 'Z'], right=False)

    # Рассчитываем коэффициент вариации
    data['coefficient_of_variation'] = data.groupby('product_id').apply(
        lambda x: x['std_quantity'].mean() / x['quantity'].mean() if x['quantity'].mean() != 0 else float('nan')
    ).reset_index(level=0, drop=True)
    
    # Создание комбинированной категории ABC-XYZ
    data['ABC_XYZ'] = data['ABC'].astype(str) + "-" + data['XYZ'].astype(str)
    
    return data
