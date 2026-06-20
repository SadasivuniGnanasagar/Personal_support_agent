# src/classifier.py

def detect_persona(message):
    msg = message.lower()

    technical_keywords = [
        "api", "token", "endpoint", "database",
        "configuration", "logs", "authentication"
    ]

    frustrated_keywords = [
        "nothing works", "frustrated", "angry",
        "immediately", "urgent", "terrible"
    ]

    executive_keywords = [
        "business", "impact", "operations",
        "timeline", "revenue", "executive"
    ]

    if any(word in msg for word in technical_keywords):
        return "Technical Expert"

    elif any(word in msg for word in frustrated_keywords):
        return "Frustrated User"

    elif any(word in msg for word in executive_keywords):
        return "Business Executive"

    return "Frustrated User"