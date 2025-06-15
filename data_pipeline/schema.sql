CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id TEXT UNIQUE, 
    title TEXT,
    publication_date TEXT, 
    document_type TEXT,
    summary TEXT
);