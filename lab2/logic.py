import database
import config
from datetime import datetime

def process_reading(meter_id, current_day, current_night):
    
    previous_meter_data = database.get_meter_by_id(meter_id)
    today = datetime.now()

    if previous_meter_data is None:
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        days_passed = (today - start_of_month).days
        if days_passed < 0: 
            days_passed = 0
        
        if days_passed == 0:
             days_passed = 1  

        day_consumption = current_day
        night_consumption = current_night

        cost = (day_consumption * config.DAY_TARIFF) + (night_consumption * config.NIGHT_TARIFF)

        database.add_new_meter(meter_id, current_day, current_night, date=today)

        notes = f"Перший розрахунок на {start_of_month.strftime('%Y-%m-%d')})."
        database.save_bill(meter_id, day_consumption, night_consumption, cost, notes)

        return {
            "status": "new_calculated",
            "meter_id": meter_id,
            "day_consumption": day_consumption,
            "night_consumption": night_consumption,
            "cost": cost,
            "message": notes,
            "days_passed": days_passed
        }

    previous_update_date = previous_meter_data['last_update']
    days_passed = (today.date() - previous_update_date.date()).days 
    
   
    if days_passed <= 0: 
        days_passed = 1

    previous_day = previous_meter_data['previous_day_reading']
    previous_night = previous_meter_data['previous_night_reading']
    
    day_consumption_calculated = 0.0 
    night_consumption_calculated = 0.0
    notes_list = []

    if current_day < previous_day:
        day_consumption_calculated = config.PENALTY_DAY_KWH
        notes_list.append(f"Занижено денний показник! Нараховано штраф {config.PENALTY_DAY_KWH} кВт·год.")
    else:
        day_consumption_calculated = float(current_day - previous_day)

    if current_night < previous_night:
        night_consumption_calculated = config.PENALTY_NIGHT_KWH
        notes_list.append(f"Занижено нічний показник! Нараховано штраф {config.PENALTY_NIGHT_KWH} кВт·год.")
    else:
        night_consumption_calculated = float(current_night - previous_night)
            
    cost = (day_consumption_calculated * config.DAY_TARIFF) + (night_consumption_calculated * config.NIGHT_TARIFF)
    
    database.update_meter_readings(meter_id, current_day, current_night)
    
    final_notes_str = " | ".join(notes_list) if notes_list else "Стандартний розрахунок."
    database.save_bill(meter_id, day_consumption_calculated, night_consumption_calculated, cost, final_notes_str)
    
    return {
        "status": "updated",
        "meter_id": meter_id,
        "day_consumption": day_consumption_calculated,
        "night_consumption": night_consumption_calculated,
        "cost": cost,
        "message": final_notes_str,
        "days_passed": days_passed
    }
