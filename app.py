import streamlit as st

from src.classifier import detect_persona
from src.rag_pipeline import (
    load_documents,
    chunk_documents,
    create_vector_db,
    retrieve
)
from src.generator import generate_response
from src.escalator import (
    should_escalate,
    generate_handoff
)

# ----------------------------------
# Page Config
# ----------------------------------
st.set_page_config(
    page_title="Persona Adaptive Customer Support Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Persona Adaptive Customer Support Agent")

st.write(
    "Enter a customer support query and receive a persona-adaptive response."
)

# ----------------------------------
# Load Knowledge Base
# ----------------------------------
@st.cache_resource
def initialize_rag():

    docs = load_documents()

    chunks = chunk_documents(docs)

    collection = create_vector_db(chunks)

    return collection

collection = initialize_rag()

# ----------------------------------
# User Input
# ----------------------------------
user_query = st.text_area(
    "Enter your support query",
    height=150
)

# ----------------------------------
# Submit Button
# ----------------------------------
if st.button("Submit"):

    if not user_query.strip():
        st.warning("Please enter a query.")
        st.stop()

    with st.spinner("Processing..."):

        # --------------------------
        # Persona Detection
        # --------------------------
        persona = detect_persona(user_query)

        # --------------------------
        # Retrieval
        # --------------------------
        results = retrieve(
            user_query,
            collection,
            top_k=3
        )

        retrieved_docs = []
        retrieved_sources = []

        if results["documents"]:

            retrieved_docs = results["documents"][0]

        if results["metadatas"]:

            retrieved_sources = [
                meta["source"]
                for meta in results["metadatas"][0]
            ]

        # --------------------------
        # Escalation Check
        # --------------------------
        escalation_needed = should_escalate(
            user_query,
            len(retrieved_docs)
        )

        # --------------------------
        # Generate Response
        # --------------------------
        try:

            response = generate_response(
                user_query,
                persona,
                retrieved_docs
            )

        except Exception as e:

            response = f"Response generation failed: {str(e)}"

    # ----------------------------------
    # Results
    # ----------------------------------
    st.divider()

    st.subheader("Detected Persona")
    st.success(persona)

    st.subheader("Retrieved Sources")

    if retrieved_sources:

        for source in set(retrieved_sources):
            st.write(f"• {source}")

    else:
        st.write("No sources found.")

    st.subheader("Generated Response")
    st.write(response)

    st.subheader("Escalation Status")

    if escalation_needed:

        st.error("Human Escalation Required")

        handoff = generate_handoff(
            persona,
            user_query,
            retrieved_sources
        )

        st.subheader("Human Handoff Summary")

        st.json(handoff)

    else:

        st.success("No Escalation Required")