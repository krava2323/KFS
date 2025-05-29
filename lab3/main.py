import database      
import weth_mod      
import sanity_check  
import pandas as pd  
import sqlite3       
import re            

CSV_FILE_PATH = 'dataset.csv' 
TARGET_YEAR = 2023            

def run_health_checks():
    print("\n--- health checks ---") 
    db_ok, db_msg = False, "not checked" 
    ml_ok, ml_msg = weth_mod.ml_module_health_check() 
    
    #  перевірка підключення до бд
    try:
        conn = sqlite3.connect(database.DATABASE_NAME) 
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='daily_weather_summary';")
        if cursor.fetchone(): 
            db_ok = True
            db_msg = "database connection successful and 'daily_weather_summary' table exists."
        else: 
            db_ok = False
            db_msg = "database connection successful, but 'daily_weather_summary' table not found."
        conn.close()
        print(f"health check: database - {'ok' if db_ok else 'fail'}. {db_msg}")
    except Exception as e: 
        db_ok = False
        db_msg = f"database connection error: {str(e)}"
        print(f"health check: database - fail. {db_msg}")

    #  в результат перевірки  модуля
    if ml_ok:
        print(f"health check: weather module  - ok. {ml_msg}")
    else:
        print(f"health check: weather module  - fail. {ml_msg}")
        
    
    if db_ok and ml_ok: 
        print("overall health status: ok")
    else:
        print("overall health status: issues detected")
    print("--- end of health checks ---\n")
    return db_ok and ml_ok 

def display_menu():
    print("\n--- меню прогнозу погоди ---")
    print(f"обраний рік 2023': {TARGET_YEAR}")
    print("1. погода на конкретну дату")
    print("2. погода на місяць")
    print("3. погода на весь рік")
    print("4. вихід")
    return input("обери опцію (1-4): ") 

def main():
    print(f"запуск програми ")

    #. ініціалізаця бд 
    database.init_db()

    # завантаження данних з файлу
    raw_df = None 
    try:
        print(f"\nспроба завантажити  дані з {CSV_FILE_PATH} для sanity check")
        raw_df = pd.read_csv(CSV_FILE_PATH) 
    except FileNotFoundError: 
        print(f"помилка: файл даних {CSV_FILE_PATH} не знайдено. неможливо продовжити.")
        print("будь ласка, створіть файл dataset.csv '")
        return 
    except pd.errors.EmptyDataError: 
        print(f"помилка: файл {CSV_FILE_PATH} порожній. немає даних для обробки.")
        return
    except Exception as e: 
        print(f"не вдалося завантажити  дані  {e}")
        return

    # завантаження успішне - sanity check
    data_loaded_successfully = False 
    if raw_df is not None:
        if sanity_check.check_hourly_data_quality(raw_df.copy()): 
            print("sanity check сирих погодинних даних пройдено.")
            
            # завантажуємо дані в бд та агрегуємо їх 
            print(f"\nзавантаження  даних з {CSV_FILE_PATH} в базу даних")
            if database.load_hourly_data_and_aggregate_to_daily(CSV_FILE_PATH):
                print("дані успішно завантажено ")
                data_loaded_successfully = True 
            else:
                print("помилка під час завантаження. подальша робота може бути некоректною.")
        else:
            print("sanity check  даних не пройдено. перевірте дані у файлі.")
            print("завантаження  даних скасовано.")
    else:
        print("не вдалося завантажити дані для обробки.")
        return

    if not data_loaded_successfully:
        print("\nне вдалося підготувати дані. робота програми неможлива.")
        return 

    # запуск перевірка
    run_health_checks()

    # меню
    while True:
        choice = display_menu() 

        if choice == '1':
            date_input = input("введіть дату у форматі рррр-мм-дд: ")
            if re.match(r"^\d{4}-\d{2}-\d{2}$", date_input):
                weth_mod.display_weather_for_date(database, date_input)
            else:
                print("неправильний формат дати. спробуйте ще раз.")
        
        elif choice == '2':
            try:
                month_input = int(input(f"введіть номер місяця (1-12) для {TARGET_YEAR} року: "))
                if 1 <= month_input <= 12:
                    weth_mod.display_weather_for_month(database, TARGET_YEAR, month_input)
                else:
                    print("номер місяця має бути від 1 до 12.")
            except ValueError:
                print("це не схоже на номер місяця. спробуйте ввести число.")
        
        elif choice == '3':
            weth_mod.get_historical_forecast_for_year(database, TARGET_YEAR)
        
        elif choice == '4':
            print("до побачення!")
            break 
        
        else:
            print("незрозуміла опція. спробуйте ще раз (введіть число від 1 до 4).")

    print("\nроботу програми завершено.") 

if __name__ == '__main__':
   
    main()
