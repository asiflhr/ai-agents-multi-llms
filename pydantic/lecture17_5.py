'''
1. Dependency Injection (DI) is a design pattern where dependencies (external services, databases, API clients, etc.) 
   are provided to a class or function rather than being hardcoded inside it. 
   This makes code more modular, reusable, and testable.

2. In this code, we are implementing DI using a `dataclass` (MyDeps), which injects:
   - An API key (used for authorization)
   - An asynchronous HTTP client (`httpx.AsyncClient`) for making API requests.

3. Instead of directly defining a static system prompt, we dynamically fetch the prompt from an external API 
   (`https://example.com`) using DI.

4. The AI agent (`Agent`) is created using the `pydantic_ai` library and configured to use `gemini-1.5-flash`.

5. The `main()` function runs the agent and prints a response to a user query.
'''

# Import necessary libraries
from dataclasses import dataclass # For creating data classes for dependency injection
import httpx # For making HTTP requests
import asyncio # For asynchronous programming

# immport AI related classes from pydantic_ai
from pydantic_ai import Agent, RunContext
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GEMINI_API_KEY"]=os.getenv("GOOGLE_API_KEY")

# --------------------------- Dependency Injection Setup --------------------------- #
@dataclass # @dataclass is used to automatically generate __init__, __repr__, __eq__, and __hash__ methods for the class
class MyDeps:
    """
    This dataclass is used for dependency injection. It contains:
    - `api_key`: An API key for authorization.
    - `http_client`: An asynchronous HTTP client for making API requests.
    """

    api_key: str
    http_client: httpx.AsyncClient # An asynchronous HTTP client for making API requests
    
# --------------------------- AI Agent configuration --------------------------- #
agent = Agent(
    'google-gla:gemini-1.5-flash', # Specifies the LLM model to use
    deps_type=MyDeps, # Specifies the type of dependencies to inject
)

# --------------------------- Dynamic System Prompt Function --------------------------- #
@agent.system_prompt # Decorator to mark this function as the system prompt
async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:
    """
    This function dynamically generates the system prompt for the AI agent.

    - It retrieves text from an external API (`https://example.com`).
    - Uses Dependency Injection (`ctx.deps`) to access:
      - `http_client`: Injected HTTP client for making requests.
      - `api_key`: Injected API key for authentication.
    - Returns the fetched text as a formatted system prompt.

    Parameters:
    - ctx: RunContext[MyDeps] → Provides access to injected dependencies.

    Returns:
    - str: The dynamically fetched system prompt.
    """

    response = await ctx.deps.http_client.get(
        "https://example.com", # URL to fetch text from
        headers={"Authorization": f"Bearer {ctx.deps.api_key}"} # Headers for authentication
    )

    response.raise_for_status() # Raises an exception if the request was unsuccessful
    print(f"System prompt: {response.text}")
    return f"System prompt: {response.text}" # Returns the fetched text as the system prompt

async def main():
    """
    This function initializes the dependencies and runs the AI agent.

    - Creates an instance of `httpx.AsyncClient` for making async HTTP requests.
    - Injects `MyDeps` dependencies (API key + HTTP client) into the AI agent.
    - Calls the AI agent to generate a response for the prompt "Tell me a joke."
    - Prints the response.

    Expected Output:
    - Example: "Did you hear about the toothpaste scandal? They called it Colgate."
    """

    async with httpx.AsyncClient() as client: # Creates an asynchronous HTTP client
        deps = MyDeps("foobar", client) # Injects dependencies
        result = await agent.run("Tell me a joke.", deps=deps) # Runs the agent with dependencies
        print(result.data) # Prints the response


# --------------------------- Running the main function --------------------------- #
if __name__ == '__main__':
    """
    Ensures the script runs only when executed directly, not when imported as a module.
    
    `asyncio.run(main())` runs the main function asynchronously.
    """
    asyncio.run(main())