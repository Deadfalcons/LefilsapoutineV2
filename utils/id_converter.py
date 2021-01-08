def id_convert(user_given: str) -> str:
    user = ""
    for char in user_given:
        if char in "0123456789":
            user += char
    return user
