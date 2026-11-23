import streamlit as st
from retriever import MedicalRetriever
from llm_generator import generate_answer

st.set_page_config(
    page_title="Medical RAG Assistant",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Evidence-Based Medical RAG Assistant")

st.write("Ask questions based on our healthcare document collection.")

st.info(
    "This assistant provides document-based information "
    "and is not a substitute for professional medical advice."
)


@st.cache_resource
def load_retriever():
    return MedicalRetriever()


try:
    retriever = load_retriever()
    st.success("Medical knowledge base loaded successfully!")

    question = st.text_input(
        "Enter your medical question:",
        placeholder="Example: What are the risk factors for diabetes?"
    )

    if st.button("Get Answer"):
        if not question.strip():
            st.warning("Please enter a question.")

        else:
            with st.spinner("Searching medical documents..."):
                passages = retriever.search(question, top_k=3)

            if not passages:
                st.warning(
                    "The answer is not available in the provided "
                    "medical documents."
                )

            else:
                with st.spinner("Generating answer..."):
                    answer = generate_answer(question, passages)

                unavailable_message = (
                    "The answer is not available in the provided medical documents."
                )

                st.subheader("Answer")
                st.write(answer)

                # Show sources only when an answer is supported
                if unavailable_message.lower() not in answer.lower():
                    st.subheader("Sources Used")

                    for passage in passages:
                        with st.expander(
                            f"{passage['source']} — Page {passage['page']}"
                        ):
                            st.write(passage["text"])

except Exception as error:
    st.error(f"Application error: {error}")