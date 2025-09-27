from datetime import datetime
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

from asyncio import tools

def get_current_time() -> dict:
    """Return the current time as a string in the format '%Y-%m-%d %H:%M:%S'."""
    return {
        "current time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="""
    You are a helpful assistant for user questions by using the following tools:
    - get_current_time
    """,
    instruction='Answer user questions to the best of your knowledge',
    tools=[get_current_time]
    # tools=[google_search]
)
