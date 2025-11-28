def format_message(message: str) -> str:
    return f"*** {message} ***"

def validate_input(user_input: str) -> bool:
    return bool(user_input.strip())

def log_message(message: str) -> None:
    with open("chatbot_log.txt", "a") as log_file:
        log_file.write(f"{message}\n")