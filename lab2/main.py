import database
import logic

def print_header(title):
    print("\n" + "="*50)
    print(f"--- {title} ---")
    print("="*50)

def add_new_reading_ui():
    print_header("Введення нових показників")
    try:
        meter_id = input("Введіть номер лічильника: ")
        
        meter_data = database.get_meter_by_id(meter_id)
        if meter_data:
            last_date = meter_data['last_update'].strftime('%Y-%m-%d')
            print(f"(Інформація: останні показники для цього лічильника були внесені {last_date})")
        else:
            print("(Інформація: цей лічильник буде додано як новий)")

        current_day = float(input("Введіть поточні денні показники (кВт·год): "))
        current_night = float(input("Введіть поточні нічні показники (кВт·год): "))
        
        if not meter_id or current_day < 0 or current_night < 0:
            print("Помилка: Усі поля мають бути заповнені, а показники не можуть бути від'ємними.")
            return

        result = logic.process_reading(meter_id, current_day, current_night)
        
        
        print("\n--- Результат обробки ---")
        print(f"Лічильник: {result['meter_id']}")

        if result['status'] == 'new_calculated':
            print(f"Показники для нового лічильника успішно прийнято.")
            print(f"  Спожито (день): {result['day_consumption']:.2f} кВт·год")
            print(f"  Спожито (ніч): {result['night_consumption']:.2f} кВт·год")
            print(f"  Попередньо нарахована сума: {result['cost']:.2f} грн.")
            print(f"\n  >>> Остаточний рахунок буде включено у платіжку в кінці місяця. <<<")
        
        elif result['status'] == 'updated_same_day':
            print(f"  Примітки: {result['message']}")

        else:
            print(f"  Період розрахунку: {result['days_passed']} дн.")
            print(f"  Спожито (день): {result['day_consumption']:.2f} кВт·год")
            print(f"  Спожито (ніч): {result['night_consumption']:.2f} кВт·год")
            print(f"  Примітки: {result['message']}")
            print(f"\n  >>> СУМА ДО СПЛАТИ: {result['cost']:.2f} грн <<<")
            
    except ValueError:
        print("Помилка: Будь ласка, вводьте числові значення для показників.")
    except Exception as e:
        print(f"Сталася неочікувана помилка: {e}")

def view_all_bills_ui():
    """Інтерфейс для перегляду історії рахунків."""
    print_header("Історія всіх рахунків")
    all_bills = database.get_all_bills()
    if not all_bills:
        print("Історія рахунків порожня.")
        return
        
    for bill in all_bills:
        meter_id_str = bill.get('meter_id', 'N/A')
        print(
            f"Лічильник: {meter_id_str} | Дата: {bill['billing_date'].strftime('%Y-%m-%d %H:%M')} | "
            f"Сума: {bill['total_cost']:.2f} грн | Примітки: {bill['notes']}"
        )

def main_menu():
    """Головне меню програми."""
    print("Підключення до MongoDB...")
    while True:
        print_header("Система обліку електроенергії (MongoDB)")
        print("1. Ввести нові показники лічильника")
        print("2. Переглянути історію всіх рахунків")
        print("3. Вийти")
        
        choice = input("Ваш вибір: ")
        
        if choice == '1':
            add_new_reading_ui()
        elif choice == '2':
            view_all_bills_ui()
        elif choice == '3':
            print("Дякуємо за використання системи!")
            break
        else:
            print("Невірний вибір. Будь ласка, спробуйте ще раз.")

if __name__ == "__main__":
    main_menu()
