import database
import logic

from datetime import datetime

def run_monthly_billing():
   
    print("===== ПОЧАТОК РОЗРАХУНКУ ЗА ПЕРІОД =====")

    # Встановлюємо дату
    previous_readings_date = datetime(2025, 5, 1)

    
    previous_readings_data = [
        {"_id": "KYIV-001", "day": 12540, "night": 8760},
        {"_id": "LVIV-002", "day": 8321, "night": 4511},
        {"_id": "ODESA-003", "day": 21500, "night": 11200},
        {"_id": "KHARKIV-004", "day": 5000, "night": 3000},
        {"_id": "DNIPRO-005", "day": 1500, "night": 900},
    ]

    # ПОТОЧНІ ПОКАЗНИКИ
    current_readings_data = [
        {"_id": "KYIV-001", "day": 12655, "night": 8895},
        {"_id": "LVIV-002", "day": 8430, "night": 4510}, 
        {"_id": "ODESA-003", "day": 21710, "night": 11450},
        {"_id": "KHARKIV-004", "day": 4990, "night": 3050}, 
        {"_id": "DNIPRO-005", "day": 1620, "night": 980},
        {"_id": "ZHYTOMYR-006", "day": 150, "night": 70}, 
    ]

    # БАЗА ДАНИХ
    print("\n-- Підготовка бази даних ---")
    database.meters_collection.delete_many({}) 
    print("Колекцію лічильників очищено.")

    print(f"Заповнення бази даних минулими показниками (на {previous_readings_date.strftime('%Y-%m-%d')})...")
    for meter_data in previous_readings_data:
        database.add_new_meter(meter_data["_id"], meter_data["day"], meter_data["night"], date=previous_readings_date)
    print("Попередні дані завантажено до бази.\n")

    # ОБРОБКА ПОТОЧНИХ ПОКАЗНИКІВ
    print("---  Розрахунок поточних рахунків ---")
    total_billed = 0.0
    for reading_data in current_readings_data:
        meter_id = reading_data["_id"]
        current_day = reading_data["day"]
        current_night = reading_data["night"]
        
        print(f"\nОбробка лічильника: {meter_id}...")
        
        result = logic.process_reading(meter_id, current_day, current_night)
        

        print(f"  Статус: {result['status']}")
        print(f"  Період розрахунку: {result.get('days_passed', 'N/A')} дн.") 
        print(f"  Спожито (день): {result['day_consumption']:.2f} кВт·год")
        print(f"  Спожито (ніч): {result['night_consumption']:.2f} кВт·год")
        print(f"  Примітки: {result['message']}")
        print(f"  >>> СУМА ДО СПЛАТИ: {result['cost']:.2f} грн <<<")
        
        total_billed += result['cost']

    print("\n" + "="*50)
    print(f"УСІ РАХУНКИ ОБРОБЛЕНО. ЗАГАЛЬНА СУМА: {total_billed:.2f} ГРН")
    print("="*50)

if __name__ == "__main__":
    run_monthly_billing()
