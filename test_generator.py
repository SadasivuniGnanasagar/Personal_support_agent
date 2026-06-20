from src.generator import generate_response

docs = [
    """
    Password Reset Guide

    1. Click Forgot Password
    2. Enter registered email
    3. Create a new password
    """
]

response = generate_response(
    "How do I reset my password?",
    "Frustrated User",
    docs
)

print(response)