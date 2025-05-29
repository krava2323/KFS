import pandas as pd 

def _format_weather_row(row_data):
    
    date_str, min_t, max_t = row_data
    if min_t is not None and max_t is not None:
        temp_output = f"{min_t:.1f}-{max_t:.1f} градусів цього дня"
        if min_t > max_t:
             temp_output += " (увага: min > max!)"
    else:
        temp_output = "температурні дані неповні"
    
    if not isinstance(date_str, str): 
        date_str = f"некоректний формат дати ({date_str})"
    return f"{date_str}: {temp_output}"

def display_weather_for_date(db_module, date_str_input):
    #  вивід погоди за певну дату
    print(f"\n--- погода за {date_str_input} ---")
    weather_row = db_module.get_weather_for_date(date_str_input) 
    if weather_row:
        print(_format_weather_row(weather_row)) 
    else:
        print(f"дані за {date_str_input} не знайдено.")

def display_weather_for_month(db_module, year, month_num):
    #  вивід погоди за певний місяць
    month_names = ["січень", "лютий", "березень", "квітень", "травень", "червень", 
                   "липень", "серпень", "вересень", "жовтень", "листопад", "грудень"]
    month_name_str = month_names[month_num-1] if 0 < month_num <= 12 else f"невідомий місяць ({month_num})"

    print(f"\n--- погода за {month_name_str.lower()} {year} року ---")
    weather_data_month = db_module.get_weather_for_month(year, month_num) 
    
    if not weather_data_month:
        print(f"дані за {month_name_str.lower()} {year} року не знайдено.")
        return

    for row in weather_data_month: 
        print(_format_weather_row(row)) 

def get_historical_forecast_for_year(db_module, year):
    print(f"\n--- погода за {year} рік  ---")
    weather_data = db_module.get_weather_for_year(year) 
    
    if not weather_data:
        print(f"дані за {year} рік не знайдено в таблиці.")
        return 

    for row in weather_data: 
        print(_format_weather_row(row)) 

    if not weather_data: 
         print(f"дані для прогнозу за {year} не були відформатовані чи знайдені.")

def ml_module_health_check():
    print("ml module health check: ok (placeholder)")
    return True, "ml module is responsive (placeholder)."
