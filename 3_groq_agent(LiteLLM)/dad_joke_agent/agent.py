import random
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

model = LiteLlm(
    model="groq/llama-3.3-70b-versatile",
)

def get_dad_joke():
    """
    Returns a dad joke
    """
    dad_jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why did the math book look sad? Because it had too many problems.",
        "I only know 25 letters of the alphabet. I don't know y.",
        "Why can't your nose be 12 inches long? Because then it would be a foot!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the coffee file a police report? It got mugged.",
        "How do you organize a space party? You planet.",
    ]

    return random.choice(dad_jokes)

root_agent = Agent(
    name="dad_joke_agent",
    model=model,
    description="This agent tells a dad joke.",
    instruction="""
    You are a helpful assistant that tells dad jokes to the users.
    Only use the tool 'get_dad_joke' to tell the user a dad joke.
    """,
    tools=[get_dad_joke]
)