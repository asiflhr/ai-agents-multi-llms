from pydantic_ai import Agent
import os
from dotenv import load_dotenv
import logfire
import asyncio

# Load environment variables
load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Configure Logfire properly
logfire.configure()
logfire.instrument_httpx()
os.environ["LOGFIRE_TOKEN"] = os.getenv("LOGFIRE_TOKEN")

async def run_agent_queries():
    # Create agents inside the async function
    agent_1 = Agent(  
        'google-gla:gemini-1.5-flash',
        system_prompt='Be funny, reply with one sentence.',  
    )
    
    agent_2 = Agent(
        'google-gla:gemini-1.5-flash',
        system_prompt='Be funny, reply with one sentence.',  
    )

    try:
        # Run first query
        result_1 = await agent_1.run('What is Pythagoras theorem?')
        print(result_1.data)
        logfire.info("Pythagoras theorem response", response=result_1.data)

        # Run second query
        result_2 = await agent_2.run('What is the capital of France?')
        print(result_2.data)
        logfire.info("Capital of France response", response=result_2.data)

    except Exception as e:
        logfire.error("Error running agent queries", error=str(e))
        raise

def main():
    # Create a new event loop for the main thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(run_agent_queries())
    finally:
        loop.close()

if __name__ == "__main__":
    main()