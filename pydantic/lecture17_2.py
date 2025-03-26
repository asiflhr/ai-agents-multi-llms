'''
Structured Response
'''

from pydantic import BaseModel, Field
from pydantic_ai import Agent
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")
os.environ["GEMINI_API_KEY"] = api_key

class Response(BaseModel):
    rating: int = Field(ge=1, le=10, description="Rating must be between 1 and 10")

agent = Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt='Given a product review, rate it from 1 to 10.',
    result_type=Response
)

async def process_reviews():
    try:
        result = await agent.run('The product is super slow and boring.')
        print(result.data)
    except Exception as e:
        print(f"Error processing review: {e}")

    try:
        result = await agent.run('The product is super cool and amazing.')
        print(result.data)
    except Exception as e:
        print(f"Error processing review: {e}")

# Run the async function
if __name__ == "__main__":
    asyncio.run(process_reviews())
