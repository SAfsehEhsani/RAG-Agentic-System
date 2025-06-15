import sqlite3
import os
from datetime import datetime, timedelta

from data_pipeline import process_data

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'federal_registry.db')

def search_federal_registry(keywords: str = None, document_type: str = None, days_ago: int = None) -> str:
    """
    Searches the federal registry database for documents based on keywords, type, or publication date.

    Args:
        keywords (str, optional): Keywords to search for in title or summary. Defaults to None.
        document_type (str, optional): Specific type of document (e.g., "Executive Order", "Rule"). Defaults to None.
        days_ago (int, optional): Search for documents published in the last N days. Defaults to None.

    Returns:
        str: A formatted string of search results or a message indicating no results or an error.
    """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        query = "SELECT title, publication_date, document_type, summary FROM documents WHERE 1=1"
        params = []

        if keywords:
            query += " AND (title LIKE ? OR summary LIKE ?)"
            
            params.append(f'%{keywords}%')
            params.append(f'%{keywords}%')

        if document_type:
            query += " AND document_type LIKE ?"
            params.append(f'%{document_type}%') 

        if days_ago is not None and days_ago >= 0:
            cutoff_date = datetime.now() - timedelta(days=days_ago)
            query += " AND publication_date >= ?"
            params.append(cutoff_date.strftime('%Y-%m-%d'))

        query += " ORDER BY publication_date DESC LIMIT 10" 

        print(f"Executing SQL: {query} with params: {params}") 
        cursor.execute(query, params) 

        results = cursor.fetchall()

        if not results:
            return "No documents found matching your criteria in the database."

        formatted_results = "Search Results:\n\n"
        for row in results:
            title, date, doc_type, summary = row
            short_summary = (summary[:200] + '...') if summary and len(summary) > 200 else summary
            formatted_results += f"Title: {title}\nDate: {date}\nType: {doc_type}\nSummary: {short_summary}\n---\n"

        return formatted_results.strip()

    except sqlite3.Error as e:
        print(f"Database error during search: {e}")
        return f"An error occurred while searching the database: {e}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}"
    finally:
        if conn:
            conn.close()

SEARCH_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "search_federal_registry",
        "description": "Search the local federal registry database for documents. Use this when the user asks questions about executive orders, rules, notices, or other federal documents, especially recent ones or related to specific topics.",
        "parameters": {
            "type": "object",
            "properties": {
                "keywords": {
                    "type": "string",
                    "description": "Keywords to search for in the document title or summary (e.g., 'AI safety', 'emissions standards'). Optional."
                },
                "document_type": {
                    "type": "string",
                    "description": "Specific type of document to search for (e.g., 'Executive Order', 'Rule', 'Notice', 'Presidential Memorandum'). Optional."
                },
                "days_ago": {
                    "type": "integer",
                    "description": "Search for documents published within the last N days. For example, specify 7 for documents in the last week. If not specified, search covers all dates."
                }
            },
            "required": [], 
        }
    }
}
AVAILABLE_TOOLS = {
    "search_federal_registry": search_federal_registry
}

if __name__ == "__main__":
    print("--- Testing search_federal_registry ---")
    process_data.initialize_database() 
    process_data.process_and_load([ 
         {"doc_id": "test-001-search", "title": "AI Security Directive", "publication_date": "2023-11-15", "document_type": "Directive", "summary": "Ensuring security in artificial intelligence development."},
         {"doc_id": "test-002-search", "title": "New Rule on Water Quality", "publication_date": "2023-11-18", "document_type": "Rule", "summary": "Updates to water quality standards."},
         {"doc_id": "test-003-search", "title": "Executive Order on Climate Goals", "publication_date": "2023-11-20", "document_type": "Executive Order", "summary": "Setting new climate change targets."}
    ])

    print("\nSearching for 'AI'...")
    print(search_federal_registry(keywords="AI"))

    print("\nSearching for 'Rule'...")
    print(search_federal_registry(document_type="Rule"))

    print("\nSearching for documents in the last 3 days...")
    print(search_federal_registry(days_ago=365)) 

    print("\nSearching for 'Executive Order' with keywords 'climate'...")
    print(search_federal_registry(document_type="Executive Order", keywords="climate"))