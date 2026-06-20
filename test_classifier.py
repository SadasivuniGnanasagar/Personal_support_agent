from src.classifier import detect_persona

print("Test 1:")
print(detect_persona(
    "Our API authentication is failing with 401 errors"
))

print("\nTest 2:")
print(detect_persona(
    "I've tried everything and nothing works!"
))

print("\nTest 3:")
print(detect_persona(
    "How will this impact business operations?"
))