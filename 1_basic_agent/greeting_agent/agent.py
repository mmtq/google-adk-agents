from google.adk.agents import Agent

root_agent = Agent(
    name="greeting_agent",
    model="gemini-2.0-flash-lite",
    description="This agent greets the user.",
    instruction="""
    You are a helpful assistant that greets the users. Ask for the user's name and greet them by name.
    """
)