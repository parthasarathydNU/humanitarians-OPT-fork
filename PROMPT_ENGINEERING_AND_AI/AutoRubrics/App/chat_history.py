def format_chat_history(messages):
    formatted_history = ""
    for message in messages:
        role = "user" if message["role"] == "user" else "Assistant"
        content = message["content"]
        formatted_history += f"{role}: {content}\n"
    return formatted_history
