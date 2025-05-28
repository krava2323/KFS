import unittest
from pymongo import MongoClient
import config
import database
import logic 
from datetime import datetime, timedelta

class TestBillingLogicMongo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.original_db_name = getattr(config, 'MONGO_DATABASE_NAME', 'billing_system')
        config.MONGO_DATABASE_NAME = "test_billing_system"
        
        cls.client = MongoClient(config.MONGO_URI)
        cls.db = cls.client[config.MONGO_DATABASE_NAME]
        
        database.client = cls.client
        database.db = cls.db
        database.meters_collection = cls.db["meters"]
        
    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'client') and cls.client:
            cls.client.drop_database(config.MONGO_DATABASE_NAME)
            print(f"\nТестова база даних '{config.MONGO_DATABASE_NAME}' видалена після всіх тестів.")
            cls.client.close()
            print("З'єднання MongoClient закрито.")
        
        config.MONGO_DATABASE_NAME = cls.original_db_name

    def setUp(self):
        database.meters_collection.delete_many({}) 
        
        yesterday = datetime.now() - timedelta(days=1)
        database.add_new_meter('EXISTING-001', 1000, 500, date=yesterday)

    def tearDown(self):
        database.meters_collection.delete_many({})

    def test_update_existing_meter(self):
        result = logic.process_reading('EXISTING-001', 1150, 550)
        self.assertEqual(result['status'], 'updated')
        self.assertAlmostEqual(result['day_consumption'], 150)
        self.assertAlmostEqual(result['night_consumption'], 50)
        expected_cost = (150 * config.DAY_TARIFF) + (50 * config.NIGHT_TARIFF)
        self.assertAlmostEqual(result['cost'], expected_cost)
        self.assertEqual(result['days_passed'], 1)

    def test_add_new_meter(self): 
        result = logic.process_reading('NEW-METER-002', 10, 5)
        self.assertEqual(result['status'], 'new_calculated')
        
        self.assertAlmostEqual(result['day_consumption'], 10)
        self.assertAlmostEqual(result['night_consumption'], 5)
        expected_cost = (10 * config.DAY_TARIFF) + (5 * config.NIGHT_TARIFF)
        self.assertAlmostEqual(result['cost'], expected_cost)
        self.assertTrue(result['days_passed'] >= 0) 
        
        meter_in_db = database.get_meter_by_id('NEW-METER-002')
        self.assertIsNotNone(meter_in_db)
        self.assertEqual(meter_in_db['_id'], 'NEW-METER-002')
        self.assertEqual(meter_in_db['previous_day_reading'], 10)
        self.assertEqual(meter_in_db['previous_night_reading'], 5)
        self.assertIn("Перший розрахунок", result['message'])

    def test_tamper_night_reading(self):
        result = logic.process_reading('EXISTING-001', 1100, 450)
        self.assertEqual(result['status'], 'updated')
        self.assertAlmostEqual(result['day_consumption'], 100)
        self.assertAlmostEqual(result['night_consumption'], config.PENALTY_NIGHT_KWH)
        self.assertIn("Занижено нічний показник", result['message'])
        self.assertEqual(result['days_passed'], 1)

    def test_tamper_day_reading(self):
        result = logic.process_reading('EXISTING-001', 950, 550)
        self.assertEqual(result['status'], 'updated')
        self.assertAlmostEqual(result['day_consumption'], config.PENALTY_DAY_KWH)
        self.assertAlmostEqual(result['night_consumption'], 50)
        self.assertIn("Занижено денний показник", result['message'])
        self.assertEqual(result['days_passed'], 1)

    def test_tamper_both_readings(self):
        result = logic.process_reading('EXISTING-001', 900, 400)
        self.assertEqual(result['status'], 'updated')
        self.assertAlmostEqual(result['day_consumption'], config.PENALTY_DAY_KWH)
        self.assertAlmostEqual(result['night_consumption'], config.PENALTY_NIGHT_KWH)
        self.assertIn("Занижено денний показник", result['message'])
        self.assertIn("Занижено нічний показник", result['message'])
        self.assertEqual(result['days_passed'], 1)
        
        meter_in_db = database.get_meter_by_id('EXISTING-001')
        self.assertAlmostEqual(meter_in_db['previous_day_reading'], 900)
        self.assertAlmostEqual(meter_in_db['previous_night_reading'], 400)

if __name__ == '__main__':
    unittest.main()
