import os
from . import fetch_data
from . import process_data

DATABASE_DIR = os.path.join(os.path.dirname(__file__), '..')
if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)

DB_FILE = os.path.join(DATABASE_DIR, 'federal_registry.db')

def run_daily_pipeline():
    """Runs the data pipeline: fetches data and loads it."""
    print("Starting daily data pipeline...")

    process_data.initialize_database()

    #fetched_items = fetch_data.simulate_fetch_recent_documents(days=5) 
    fetched_items = fetch_data.simulate_fetch_recent_documents(days_window=30) # Fetch last 5 days
    process_data.process_and_load(fetched_items)

    print("Daily data pipeline finished.")

if __name__ == "__main__":
    run_daily_pipeline()