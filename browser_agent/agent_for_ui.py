from langchain_openai import ChatOpenAI
from browser_use import Agent
import os
import json
import base64
from dotenv import load_dotenv

async def run_browser_agent(query):
    load_dotenv()
    llm = ChatOpenAI(model='gpt-4o')

    try:
        agent = Agent(
            task=query,
            llm=llm,
            use_vision=True
        )
        result = await agent.run()

        #Logs
        url = result.urls()
        action_names = result.action_names()
        extracted_content = result.extracted_content()
        errors = result.errors()
        model_actions = result.model_actions()

        try:
            data ={
                "visited_urls": url,
                "action_names": action_names,
                "extracted_content": extracted_content,
                "errors": errors,
                "model_actions": model_actions
            }

            logs_folder = "browser_agent/logs"
            os.makedirs(logs_folder, exist_ok=True)

            # Write to JSON
            file_path = os.path.join(logs_folder, "history.json")
            with open(file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)

        except Exception as e:
            print(f'An error occured when writing logs: {str(e)}')

        return result
    
    except Exception as e:
        print(f"An error occured: {str(e)}")
    
 


    
