import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import logging

logger = logging.getLogger(__name__)

# Функция для загрузки данных о продажах
def load_sales_data(file_path):
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        # Проверяем наличие необходимых столбцов
        required_columns = ['month', 'sales']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Неверный формат данных. Ожидаются столбцы: {required_columns}")
        return df
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных: {str(e)}")
        raise

# Функция для выполнения предсказаний
def perform_prediction(data):
    try:
        # Проверка данных на пропущенные значения
        if data['month'].isnull().any() or data['sales'].isnull().any():
            raise ValueError("Данные содержат пропущенные значения.")

        # Преобразуем данные для регрессии
        X = data['month'].values.reshape(-1, 1)
        y = data['sales'].values

        # Разделение данных на тренировочную и тестовую выборки
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Инициализация и тренировка модели
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Предсказание на тестовой выборке
        y_pred = model.predict(X_test)

        # Оценка качества модели (ошибка)
        mse = mean_squared_error(y_test, y_pred)
        logger.info(f"Среднеквадратичная ошибка модели: {mse}")

        # Предсказания на всех данных
        predictions = model.predict(X)
        return pd.DataFrame({'month': data['month'], 'actual_sales': data['sales'], 'predicted_sales': predictions})
    except Exception as e:
        logger.error(f"Ошибка при выполнении предсказаний: {str(e)}")
        raise
