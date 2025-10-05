from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='question_answer_agent',
    description='This agent answers questions based on the context provided by the user',
    instruction="""
    You are a helpful assistant that answers questions about the user's preferences.
    Here is some information about the user:
    Name: 
    {user_name}
    Preferences: 
    {user_preferences}
    """,
)
