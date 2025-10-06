import asyncio
from re import S
from dotenv import load_dotenv
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from memory_agent.agent import memory_agent
from utils import call_agent_async

load_dotenv()

db_url = "sqlite:///./database.db"
session_service = DatabaseSessionService(
    db_url
)

initial_state = {
    "user_name": "MMTQ",
    "reminders": [],
}

async def main():
    APP_NAME = "Memory Agent"
    USER_ID = "mmtq"

    existing_sessions = await session_service.list_sessions(app_name=APP_NAME, user_id=USER_ID)

    if existing_sessions and len(existing_sessions.sessions) > 0:
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Using existing session: {SESSION_ID}")
    else:
        new_session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID = new_session.id
        print(f"Created new session: {SESSION_ID}")
    
    runner = Runner(
        app_name=APP_NAME,
        agent=memory_agent,
        session_service=session_service,
    )

    print("\nWelcome to the Memory Agent!")
    print("Your reminders will be remembered acrossed sessions.")
    print("Type 'exit' to end the conversation.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)


if __name__ == "__main__":
    asyncio.run(main())