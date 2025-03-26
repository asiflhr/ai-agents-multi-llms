'''
Tools with pydantic.AI
'''

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GEMINI_API_KEY"]=os.getenv("GOOGLE_API_KEY")

# Define output structures
class Response(BaseModel):
    rating: int
    review_summary: str
    review_length: int

simple_agent = Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt='Given a product review, rate it from 1 to 10.',
    result_type=Response
)

# Define a tool
@simple_agent.tool
async def get_review_length(context: RunContext, review: str) -> int:
    """
    Given a review, return the length of the review."
    """
    return len(review)

result = simple_agent.run_sync('The product is super slow and boring.')
print(result.data)


# Accessing review_length from the result.data
print(result.data.review_length)

# Cross Verification
print(len('The product is super slow and boring.'))