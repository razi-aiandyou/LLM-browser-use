from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import json
import os

load_dotenv()

llm = ChatOpenAI(model='gpt-4o')

async def main(query):
    agent = Agent(
        task=query,
        llm=llm,
        use_vision=True,
        save_conversation_path="logs/conversation.json"
    )
    result = await agent.run()

    #Logs
    url = result.urls()
    screenshots = result.screenshots()
    action_names = result.action_names()
    extracted_content = result.extracted_content()
    errors = result.errors()
    model_actions = result.model_actions()

    try:
        data ={
            "visited_urls": url,
            "screenshots": screenshots,
            "action_names": action_names,
            "extracted_content": extracted_content,
            "errors": errors,
            "model_actions": model_actions
        }

        logs_folder = "logs"
        os.makedirs(logs_folder, exist_ok=True)

        # Write to JSON
        file_path = os.path.join(logs_folder, "history.json")
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

    except Exception as e:
        print(f'An error occured: {str(e)}')

    print(result)

query = "visit the website of'tiket.com', find a hotel in Bandung for 27 - 28 January 2025 with the price range per night between IDR 500.000 - IDR 2.000.000. Then open a google docs and write the hotels that met the requirements and save it as a .pdf"
asyncio.run(main(query))