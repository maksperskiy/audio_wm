def to_camel_case(snake_case_string: str) -> str:
    string = snake_case_string.replace("_", " ").title().replace(" ", "")
    return string[0].lower() + string[1:]
