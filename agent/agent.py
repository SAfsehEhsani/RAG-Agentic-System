import os
from groq import Groq
from dotenv import load_dotenv
import json
import time 
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=GROQ_API_KEY)

from .tools import AVAILABLE_TOOLS, SEARCH_TOOL_SCHEMA



SYSTEM_PROMPT = """You are a helpful AI assistant that provides information about US federal documents.
You have access to a database of federal registry documents including Executive Orders, Rules, Notices, Presidential Memoranda, Directives, and Proposed Rules.
When a user asks a question about federal documents, like executive orders, rules, or notices, or asks for recent documents or documents on specific topics (e.g., AI, environment, trade, health), use your available tool to search the database.
**Crucially:**
1. Analyze the user's query to determine the relevant keywords, document type, or date range.
2. For date ranges, accurately interpret phrases like 'last week' (days_ago=7), 'last 30 days' (days_ago=30), 'recent' (days_ago=7 or similar recent window), 'this month' (days_ago=30), 'last year' (days_ago=365). Pass the calculated number of days to the `days_ago` parameter of the tool. If no specific date range is mentioned, omit the `days_ago` parameter to search all available data.
3. Call the `search_federal_registry` tool with appropriate parameters extracted from the query.
4. Wait for the tool's results.
5. Summarize the search results in a concise and helpful way to answer the user's question. Do not just dump the raw search results.
6. If the tool finds no results, inform the user that no relevant documents were found in the database matching their criteria.
7. If the user's query is not related to federal documents or searching the database, answer normally without using the tool.
8. Do NOT include the tool call details (like function name or arguments) in your final response to the user. Only provide the summarized answer based on the search results (or a direct answer if no tool was needed).
9. Be polite and informative.
"""


def chat_with_agent(user_query: str, history: list):
    """
    Handles a single turn of conversation with the agent, including tool use.

    Args:
        user_query (str): The user's input message.
        history (list): List of previous messages in the conversation thread.

    Returns:
        str: The agent's response message.
    """
    history.append({"role": "user", "content": user_query})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        print("\n--- Calling LLM (Decision step) ---")
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192", # Or Groq model like "mixtral-8x7b-32768" or "gemma-7b-it"
            messages=messages,
            tools=[SEARCH_TOOL_SCHEMA], 
            tool_choice="auto",   
        )

        response_message = chat_completion.choices[0].message
        print(f"LLM Response 1: {response_message}") 
        tool_calls = response_message.tool_calls
        if tool_calls:
            print("--- Tool Call Detected ---")
            history.append(response_message)

            tool_outputs = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args_json = tool_call.function.arguments
                print(f"Function Name: {function_name}")
                print(f"Function Args: {function_args_json}")

                if function_name in AVAILABLE_TOOLS:
                    try:
                        
                        function_args = json.loads(function_args_json)
                        print(f"Parsed Args: {function_args}")

                        tool_to_call = AVAILABLE_TOOLS[function_name]

                        print(f"--- Executing Tool: {function_name} ---")
                        
                        tool_result = tool_to_call(**function_args)
                        print(f"Tool Result (first 500 chars): {tool_result[:500]}...") 
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": tool_result,
                        })

                    except json.JSONDecodeError:
                        tool_result = f"Error: Invalid JSON arguments provided for function {function_name}. Args: {function_args_json}"
                        print(tool_result)
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": tool_result,
                        })
                    except Exception as e:
                        tool_result = f"Error executing tool {function_name}: {e}"
                        print(tool_result)
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": tool_result,
                        })
                else:
                    tool_result = f"Error: Tool '{function_name}' not found."
                    print(tool_result)
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": tool_result,
                    })

            for output in tool_outputs:
                 history.append({
                    "role": "tool",
                    "content": output["output"],
                    "tool_call_id": output["tool_call_id"] 
                })

            print("\n--- Calling LLM (Summarization step) ---")
            chat_completion_2 = client.chat.completions.create(
                model="llama3-8b-8192", 
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history, 
            )

            final_response = chat_completion_2.choices[0].message.content
            print(f"LLM Response 2 (Final): {final_response}") 
            history.append({"role": "assistant", "content": final_response}) 

            return final_response

        else:
            final_response = response_message.content
            print(f"LLM Responded Directly: {final_response}") 
            history.append({"role": "assistant", "content": final_response}) 
            return final_response

    except Exception as e:
        print(f"An error occurred during agent interaction: {e}")
        error_message = f"An error occurred: {e}"
        history.append({"role": "assistant", "content": error_message})
        return error_message

if __name__ == "__main__":
    
    print("Agent Test: Ask questions about federal documents.")
    print("Type 'quit' to exit.")

    from data_pipeline import run_pipeline
    run_pipeline.run_daily_pipeline() 

    test_history = []
    while True:
        query = input("\nUser: ")
        if query.lower() == 'quit':
            break

        agent_response = chat_with_agent(query, test_history)

        print(f"Agent: {agent_response}")