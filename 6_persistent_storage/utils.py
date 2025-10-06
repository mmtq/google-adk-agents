from google.genai import types

async def display_state(session_service, app_name, user_id, session_id, label="Current State"):
    """Display the current session state in a simple way (async)."""
    try:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

        print(f"\n--- {label} ---")
        user_name = session.state.get("user_name", "Unknown")
        print(f"User: {user_name}")

        reminders = session.state.get("reminders", [])
        if reminders:
            print("Reminders:")
            for idx, reminder in enumerate(reminders, 1):
                print(f"{idx}. {reminder}")
        else:
            print("Reminders: None")
        print("--- End ---")
    except Exception as e:
        print(f"Error displaying state: {e}")


async def process_agent_response(event):
    """Process and display agent response events (simple version)."""
    print(f"Event ID: {event.id}, Author: {event.author}")

    final_response = None

    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "executable_code") and part.executable_code:
                print("Code Generated:")
                print(part.executable_code.code)
            elif hasattr(part, "code_execution_result") and part.code_execution_result:
                print("Code Execution Result:")
                print(part.code_execution_result.output)
            elif hasattr(part, "tool_response") and part.tool_response:
                print("Tool Response:")
                print(part.tool_response.output)
            elif hasattr(part, "text") and part.text and not part.text.isspace():
                print("Text:", part.text.strip())

    if event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            final_response = event.content.parts[0].text.strip()
            print("\n=== Final Agent Response ===")
            print(final_response)
            print("============================\n")
        else:
            print("\nFinal Agent Response: [No text content in final event]\n")

    return final_response


async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent asynchronously with the user's query (simple)."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(f"\n--- Running Query: {query} ---")

    final_response_text = None

    # Await the state display
    await display_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        "State BEFORE processing",
    )

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f"Error during agent call: {e}")

    # Await the state display again
    await display_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        "State AFTER processing",
    )

    return final_response_text
