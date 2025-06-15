# RAG-Agentic-System
# RAG Agentic System for Federal Registry Data

This project is of a user-facing Retrieval Augmented Generation (RAG) Agentic System built with Python.
# Deploy Link : https://rag-agentic-system.onrender.com
**Key Features:**

*   **User Interface:** A simple chat interface built with Streamlit.
*   **LLM Agent:** Integrates with a Groq Large Language Model (LLM) using function calling/tool use.
*   **Data Source:** Queries a local SQLite database containing simulated federal registry documents.
*   **Data Pipeline:** Includes a basic pipeline to simulate daily updates of data into the database.
*   **Tooling:** The LLM uses a defined function (`search_federal_registry`) to retrieve relevant information from the database based on user queries.
*   **Architecture:** Demonstrates key concepts like agentic behavior, tool use, data pipelines, and database interaction using raw SQL.
*   **Constraints:** Developed according to the assessment requirements, including no ORM, no code interpreter, hidden tool calls, and focus on structured data retrieval.

**Technologies Used:**

*   Python
*   Groq (LLM API)
*   SQLite (Database)
*   Streamlit (UI)
*   `python-dotenv`, `requests`, `sqlite3`

**How it Works:**

1.  A daily pipeline script fetches simulated data and loads it into the SQLite DB.
2.  The Streamlit app provides a chat interface.
3.  User input is sent to the Agent (`agent.py`).
4.  The Agent (Groq LLM) analyzes the query and decides if a tool (the database search function) is needed.
5.  If a tool is needed, the agent calls the `search_federal_registry` function with parameters.
6.  The function queries the SQLite database using raw SQL.
7.  The search results are returned to the Agent.
8.  The Agent summarizes the results and provides a natural language response to the user via the Streamlit UI.
