import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'federal_registry.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def initialize_database():
    """Creates the database and table if they don't exist."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        with open(SCHEMA_PATH, 'r') as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)
        conn.commit()
        print(f"Database initialized at {DATABASE_PATH}")
    except sqlite3.Error as e:
        print(f"Database error during initialization: {e}")
    finally:
        if conn:
            conn.close()

def process_and_load(data):
    """
    Processes fetched data and loads it into the SQLite database.
    Uses INSERT OR IGNORE to handle potential duplicates based on doc_id.
    """
    if not data:
        print("No data to process.")
        return

    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        insert_sql = """
        INSERT OR IGNORE INTO documents (doc_id, title, publication_date, document_type, summary)
        VALUES (?, ?, ?, ?, ?);
        """

        processed_count = 0
        for item in data:
            
            doc_id = item.get('doc_id')
            title = item.get('title')
            pub_date = item.get('publication_date')
            doc_type = item.get('document_type')
            summary = item.get('summary')

            if doc_id and title and pub_date and summary:
                cursor.execute(insert_sql, (doc_id, title, pub_date, doc_type, summary))
                processed_count += 1
            else:
                print(f"Skipping item due to missing required fields: {item.get('doc_id', 'N/A')}")

        conn.commit()
        print(f"Processed and loaded {processed_count} documents into the database.")

    except sqlite3.Error as e:
        print(f"Database error during processing: {e}")
        if conn:
            conn.rollback() 
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    
    initialize_database()
    dummy_data = [
        {"doc_id": "test-001", "title": "Test Document 1", "publication_date": "2023-01-01", "document_type": "Rule", "summary": "This is a test document."},
        {"doc_id": "test-002", "title": "Test Document 2", "publication_date": "2023-01-02", "document_type": "Notice", "summary": "Another test document."},
    ]
    process_and_load(dummy_data)

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM documents;")
    count = cursor.fetchone()[0]
    print(f"Total documents in DB after processing: {count}")
    conn.close()