import pandas as pd

def check_hourly_data_quality(df):
    print("\n sanity checks for hourly data ") 
    issues_found = False 

    #  перевірка на пропущенні дані
    if df.isnull().sum().any():
        print("знайдено пропущені значення в погодинних даних:")
        print(df.isnull().sum()[df.isnull().sum() > 0]) 
        issues_found = True
    else:
        print("пропущених значень в погодинних даних не знайдено.")

    # перевірка формату дданних
    if 'timestamp' in df.columns: #
        try:
            
            pd.to_datetime(df['timestamp'], format='%Y%m%dT%H%M')
            print("стовпець 'timestamp' успішно валідовано (формат YYYYMMDDTHHMM).")
        except Exception as e:
            print(f"помилка формату стовпця 'timestamp': {e}. очікується YYYYMMDDTHHMM.")
            issues_found = True
    else:
        print("стовпець 'timestamp' відсутній.")
        issues_found = True
        
    # перевіряю формату данних температури
    if 'temperature' in df.columns: 
        if not pd.api.types.is_numeric_dtype(df['temperature']): 
            print("стовпець temperature не є числовим. спроба конвертації...")
            try:
                df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
                if df['temperature'].isnull().any(): 
                    print("деякі значення temperature не вдалося конвертувати в числа.")
                    issues_found = True
            except Exception as e:
                 print(f"помилка при конвертації temperature: {e}")
                 issues_found = True
        
        # перевірка меж температцри
        if 'temperature' in df.columns and pd.api.types.is_numeric_dtype(df['temperature']):
            if not df['temperature'].between(-90, 60).all(): 
                print("деякі значення 'temperature' виходять за межі реалістичного діапазону (-90 до +60 c).")
                issues_found = True
    else:
        print("стовпець temperature відсутній.")
        issues_found = True

    if not issues_found:
        print("базові sanity checks для погодинних даних пройдені успішно.")
    else:
        print("виявлено проблеми під час sanity checks для погодинних даних.")
    print("--- end of hourly sanity checks ---")
    return not issues_found 

def check_daily_summary_quality(df_daily):
    #  перевірка вже для агрегованих даних (
    print("\n--- sanity checks for daily summary data ---")
    issues_found = False
    
    if 'min_temp' in df_daily.columns and 'max_temp' in df_daily.columns:
        if not (df_daily['min_temp'] <= df_daily['max_temp']).all():
            print("помилка: min_temp  бути меншим або рівним max_temp для всіх агрегованих днів.")
            issues_found = True
    else:
        print("стовпці 'min_temp' або 'max_temp' відсутні в агрегованих даних.")
        issues_found = True
        
    if not issues_found:
        print("sanity checks для агрегованих щоденних даних пройдені успішно.")
    else:
        print("виявлено проблеми під час sanity checks для агрегованих щоденних даних.")
    print("--- end of daily summary sanity checks ---")
    return not issues_found

