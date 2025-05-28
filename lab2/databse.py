from pymongo import MongoClient
from datetime import datetime
import config

client = MongoClient(config.MONGO_URI)
db = client[config.MONGO_DATABASE_NAME]
meters_collection = db["meters"]

def get_meter_by_id(meter_id):
    return meters_collection.find_one({"_id": meter_id})

def add_new_meter(meter_id, day_reading, night_reading, date=None):
    if date is None:
        date = datetime.now()
        
    new_meter_doc = {
        "_id": meter_id,
        "previous_day_reading": day_reading,
        "previous_night_reading": night_reading,
        "last_update": date,
        "bills_history": []
    }
    meters_collection.insert_one(new_meter_doc)

def update_meter_readings(meter_id, new_day, new_night):
    meters_collection.update_one(
        {"_id": meter_id},
        {"$set": {
            "previous_day_reading": new_day,
            "previous_night_reading": new_night,
            "last_update": datetime.now()
        }}
    )

def save_bill(meter_id, day_kwh, night_kwh, cost, notes=""):
    bill_document = {
        "billing_date": datetime.now(),
        "day_consumption": day_kwh,
        "night_consumption": night_kwh,
        "total_cost": cost,
        "notes": notes
    }
    meters_collection.update_one(
        {"_id": meter_id},
        {"$push": {"bills_history": bill_document}}
    )

def get_all_bills():
    pipeline = [
        {"$unwind": "$bills_history"},
        {"$replaceRoot": {"newRoot": {
            "$mergeObjects": ["$bills_history", {"meter_id": "$_id"}]
        }}},
        {"$sort": {"billing_date": -1}}
    ]
    return list(meters_collection.aggregate(pipeline))


def drop_database_for_testing():
    if client and config.MONGO_DATABASE_NAME == "test_billing_system": 
        client.drop_database(config.MONGO_DATABASE_NAME)
        print(f"Тестова база даних '{config.MONGO_DATABASE_NAME}' видалена.")
    elif config.MONGO_DATABASE_NAME != "test_billing_system":
        print(f"ПОПЕРЕДЖЕННЯ: Спроба видалити не тестову базу даних ('{config.MONGO_DATABASE_NAME}'). Операцію скасовано.")
    else:
        print("Неможливо видалити базу даних: клієнт не ініціалізовано.")
