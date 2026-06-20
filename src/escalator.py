def should_escalate(query, retrieval_count):

    sensitive_words = [
        "refund",
        "billing",
        "legal",
        "lawsuit"
    ]

    if retrieval_count == 0:
        return True

    for word in sensitive_words:
        if word in query.lower():
            return True

    return False

def generate_handoff(persona, query, sources):

    return {
        "persona": persona,
        "issue": query,
        "documents_used": sources,
        "recommendation":
        "Human support should investigate."
    }