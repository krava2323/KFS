import sqlite3
import pandas as pd

DATABASE_NAME = 'weather_app.db' 

def init_db():
    conn = sqlite3.connect(DATABASE_NAME) 
    cursor = conn.cursor() 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_weather_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE UNIQUE NOT NULL,
            min_temp REAL NOT NULL,
            max_temp REAL NOT NULL
        )
    ''')
    conn.commit() 
    conn.close() 
    print("базу даних ініціалізовано для щоденних зведень.") 

def load_hourly_data_and_aggregate_to_daily(csv_filepath):
    try:
        df = pd.read_csv(csv_filepath) 
        
        required_columns = ['timestamp', 'temperature']
        if not all(col in df.columns for col in required_columns):
            print(f"помилка: csv файл повинен містити стовпці: {', '.join(required_columns)}")
            return False 

        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%dT%H%M')
        except ValueError as e:
            print(f"помилка формату стовпця timestamp. очікується 'YYYYMMDDTHHMM'. деталі: {e}")
            return False
        
        if not pd.api.types.is_numeric_dtype(df['temperature']):
            print("помилка: стовпець 'temperature' повинен бути числовим.")
            try:
                df['temperature'] = pd.to_numeric(df['temperature']) 
            except ValueError:
                print("не вдалося конвертувати 'temperature' в числовий тип.")
                return False 


        df['date'] = df['timestamp'].dt.date

        daily_summary = df.groupby('date').agg(
            min_temp=('temperature', 'min'), 
            max_temp=('temperature', 'max')  
        ).reset_index() 

        daily_summary['date'] = daily_summary['date'].astype(str)

        conn = sqlite3.connect(DATABASE_NAME) 
        daily_summary.to_sql('daily_weather_summary', conn, if_exists='replace', index=False)
        conn.close() 
        print(f"щоденні зведені дані з {csv_filepath} успішно завантажено в базу даних.")
        return True 
        
    except FileNotFoundError:
        print(f"помилка: файл {csv_filepath} не знайдено.") 
        return False
    except pd.errors.EmptyDataError:
        print(f"помилка: файл {csv_filepath} порожній.")
        return False
    except Exception as e:
        print(f"помилка під час завантаження  даних: {e}") 
        return False

def get_weather_for_year(year):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    query = "SELECT date, min_temp, max_temp FROM daily_weather_summary WHERE strftime('%Y', date) = ? ORDER BY date ASC"
    cursor.execute(query, (str(year),)) 
    rows = cursor.fetchall() 
    conn.close()
    return rows 

def get_weather_for_month(year, month_num):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    month_str = f"{month_num:02d}" 
    query = "SELECT date, min_temp, max_temp FROM daily_weather_summary WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ? ORDER BY date ASC"
    cursor.execute(query, (str(year), month_str))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_weather_for_date(date_str): 
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    query = "SELECT date, min_temp, max_temp FROM daily_weather_summary WHERE date = ?"
    cursor.execute(query, (date_str,))
    row = cursor.fetchone() #
    conn.close()
    return row

