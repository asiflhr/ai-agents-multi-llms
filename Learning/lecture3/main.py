'''
This is a simple corchestration of 3 workers.

HOMWEWORK:

1. Optimize the code to make it more efficient.
2. Add more workers to the system.
3. Add more tasks to the system.
4. Add more workers to the system.
'''

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()  # Load environment variables from .env file

# Corrected way to retrieve the API key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Make sure it's set in the .env file.")

os.environ["GOOGLE_API_KEY"] = api_key
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")

n=input("Enter the query on which you want to perform the tasks: ")

orchestrator_prompt = f"""
You are a manager of a company who needs to allocate tasks to workers.
You are given a task: {n}
You have 3 workers available:

worker1 is a sentiment analysis expert
worker2 is a classification expert which can classify the text into technical, product, marketing, sales, finance, etc.
worker3 is a text summarization expert

Return the output in the following format in XML format(strictly follow the format, nothing else should be there in the output):

<worker1>
Actual Task: (eg. "Analyze the sentiment (add actual query) of the text b/w positive, negative, neutral.")
</worker1>
<worker2>
Actual Task: (eg. "Analyze the text (add actual query) into who should be assigned to this ticket from technical, product, marketing, sales, finance, etc.")
</worker2>
<worker3>
Actual Task: (eg. "Summarize the text (add actual query) into 3-4 lines.")
</worker3>
"""

def extract_worker1_task(result):
    return result.content.split('```')[1].split('<worker1>')[1].split('</worker1>')[0].split("<")[0].strip()

def extract_worker2_task(result):
    return result.content.split('```')[1].split('<worker2>')[1].split('</worker2>')[0].split("<")[0].strip()

def extract_worker3_task(result):
    return result.content.split('```')[1].split('<worker3>')[1].split('</worker3>')[0].split("<")[0].strip()

result = llm.invoke(orchestrator_prompt)
print(result.content)
print(extract_worker1_task(result))
print(extract_worker2_task(result))
print(extract_worker3_task(result))

worker1_prompt=f"""
You are a sentiment analysis expert. (Always output response amoung positive, negative, neutral)
Your task is: {extract_worker1_task(result)}

Always return the output in the following format in XML format(strictly follow the format, nothing else should be there in the output):

<output>
Actual Output: (eg. "positive")
</output>
"""

def extract_worker1_output(result):
    return result.content.split('```')[1].split('<output>')[1].split('</output>')[0].split("<")[0].strip()

worker1_llm=llm.invoke(worker1_prompt)
# print (worker1_llm.content)
print(extract_worker1_output(worker1_llm))

worker2_prompt=f"""
You are a classification expert which can classify the text into technical, product, marketing, sales, finance, etc.
Your task is: {extract_worker2_task(result)}

Always return the output in the following format in XML format(strictly follow the format, nothing else should be there in the output):

<output>
Actual Output: (eg. "positive")
</output>
"""

def extract_worker2_output(result):
    return result.content.split('```')[1].split('<output>')[1].split('</output>')[0].split("<")[0].strip()

worker2_llm=llm.invoke(worker2_prompt)
# print (worker2_llm.content)
print(extract_worker2_output(worker2_llm))

worker3_prompt=f"""
You are a summarization expert. 
Your task is: {extract_worker3_task(result)}

Always return the output in the following format in XML format(strictly follow the format, nothing else should be there in the output):

<output>
Actual Output: (eg. "positive")
</output>
"""

def extract_worker3_output(result):
    return result.content.split('```')[1].split('<output>')[1].split('</output>')[0].split("<")[0].strip()

worker3_llm=llm.invoke(worker3_prompt)
# print (worker3_llm.content)
print(extract_worker3_output(worker3_llm))
