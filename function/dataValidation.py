import re

def isValidEmail(email: str) -> bool:
    # Define a regular expression for email validation
    email_regex = re.compile(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    )
    # Return True if the email matches the regex, otherwise False
    return re.match(email_regex, email) is not None
