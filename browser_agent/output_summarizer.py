import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

def output_summarizer(journey):
    load_dotenv()

    log_data = {}
    try:
        with open("browser_agent/logs/history.json", "r") as f:
            log_data = json.load(f)
    except Exception as e:
        print(f"Error loading log file: {str(e)}")

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.25,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a skilled summarizer tasked with concisely summarizing the output of an AI system that browses the web
         Your task is to create a comprehensive summary that combines:
         1. The user's original task: {journey}
         2. Detailed execution logs: {logs}
         
         Include these key elements:
         - Objective and success metrics
         - Key Steps taken by the AI
         - Critical findings and data points
         - Final outcomes and recommendations
         - Technical insights from the logs
         
         Your goal is to provide clear, accurate, and relevant summaries that capture the main points and essential information. 
         Ensure that your summaries are easy to understand and provide a comprehensive overview of the AI system's findings and
         is organized in a clear and concise manner, making it easily digestible for the user..""")
    ])

    formatted_logs = json.dumps(log_data, indent=2)

    chain = prompt | llm
    ai_message = chain.invoke(
        {
            "journey": journey,
            "logs": formatted_logs
        }
    )

    return ai_message.content

    