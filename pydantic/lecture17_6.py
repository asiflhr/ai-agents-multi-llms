import asyncio
from pydantic_ai import Agent
import os
from dotenv import load_dotenv

async def main():
    # Fix .env loading
    try:
        load_dotenv()
    except Exception as e:
        print(f"Warning: Could not load .env file - {str(e)}")

    # Verify API key
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    os.environ["GEMINI_API_KEY"] = GOOGLE_API_KEY

    # Initialize agent
    agent = Agent(
        'google-gla:gemini-1.5-flash',
        system_prompt='Be concise, reply with one sentence.',
    )

    # First question
    try:
        result1 = await agent.run('Where does India come from?')
        print("The first result is:")
        print(result1.data)
    except Exception as e:
        print(f"First question failed: {str(e)}")
        return

    # Second question - without message history
    try:
        result2 = await agent.run('What was the first question I said?')
        print("The second result is:")
        print(result2.data)
    except Exception as e:
        print(f"Second question failed: {str(e)}")

if __name__ == "__main__":
    # Proper asyncio event loop handling
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            print("Event loop error - trying alternative approach")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(main())
            finally:
                loop.close()
        else:
            raise