import uuid
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answer_agent import agent
load_dotenv()

# Create a new session service to store state
session_service_stateful = InMemorySessionService()

initial_state = {
    "user_name": "MMTQ",
    "user_preferences": """
        I like to play Football, Cricket, Badminton.
        My favorite food is Bangladeshi.
        My favorite TV show is Breaking Bad.
        I want to be a Data Scientist.
    """,
}

# Create a NEW session (await needed)
import asyncio

async def main():
    APP_NAME = "MMTQ Bot"
    USER_ID = "mmtq"
    SESSION_ID = str(uuid.uuid4())
    
    # Await session creation
    stateful_session = await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )

    print("CREATED NEW SESSION:")
    print(f"\tSession ID: {SESSION_ID}")

    runner = Runner(
        agent=agent.root_agent,
        app_name=APP_NAME,
        session_service=session_service_stateful,
    )

    # new_message = types.Content(
    #     role="user", parts=[types.Part(text="What is Brandon's favorite TV show?")]
    # )

    # # Use normal for loop because runner.run() returns a generator
    # for event in runner.run(
    #     user_id=USER_ID,
    #     session_id=SESSION_ID,
    #     new_message=new_message,
    # ):
    #     if event.is_final_response():
    #         if event.content and event.content.parts:
    #             print(f"Final Response: {event.content.parts[0].text}")
    print("=== Chat with MMTQ Bot ===")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Exiting chat...")
            break

        # Prepare message
        new_message = types.Content(
            role="user",
            parts=[types.Part(text=user_input)]
        )

        # Run agent and get response
        for event in runner.run(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=new_message,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                print(f"MMTQ Bot: {event.content.parts[0].text}")

    # Get session state
    session = await session_service_stateful.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    print("=== Final Session State ===")
    for key, value in session.state.items():
        print(f"{key}: {value}")

asyncio.run(main())
