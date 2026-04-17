import streamlit as st
import os
from groq import Groq

# Configure the Streamlit page
st.set_page_config(page_title="AI Document Classifier", page_icon="📄", layout="centered")

st.title("📄 AI Document Classifier")
st.subheader("Powered by Groq")

# Sidebar for configuration
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter your Groq API Key", type="password")

if not api_key:
    st.warning("Please enter your Groq API Key in the sidebar to begin.")
else:
    st.success("API Key loaded successfully!")
    
    # File Upload method
    uploaded_file = st.file_uploader("Upload a document (.txt, .pdf) to classify:", type=["txt", "pdf", "md", "csv"])

    document_text = ""
    if uploaded_file is not None:
        try:
            if uploaded_file.name.lower().endswith(".pdf"):
                import PyPDF2
                reader = PyPDF2.PdfReader(uploaded_file)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        document_text += extracted + "\n"
            else:
                document_text = uploaded_file.read().decode("utf-8", errors="ignore")
                
            with st.expander("📄 Document Preview"):
                st.write(document_text[:1000] + ("..." if len(document_text) > 1000 else ""))
        except Exception as e:
            st.error(f"Failed to read document: {e}")

    if st.button("Classify Document"):
        if not document_text.strip():
            st.error("Please enter some document text to classify.")
        else:
            with st.spinner("Analyzing document with Groq..."):
                try:
                    # Initialize Groq client
                    client = Groq(api_key=api_key)
                    
                    # Prompt structure guiding the model
                    system_prompt = (
                        "You are a highly intelligent document classification assistant. "
                        "Read the provided document text and identify what category of document it is "
                        "(e.g., Invoice, Legal Contract, Financial Report, Patient Record, etc.). "
                        "Provide a concise classification and a brief one-sentence reason."
                    )
                    
                    # Call Groq's fast inference
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": system_prompt
                            },
                            {
                                "role": "user",
                                "content": f"Document Text:\n\n{document_text}"
                            }
                        ],
                        model="llama-3.1-8b-instant",  # Fast and effective model
                        temperature=0.3,
                        max_tokens=150
                    )
                    
                    # Extract the response
                    classification_result = chat_completion.choices[0].message.content
                    
                    # Display the result
                    st.markdown("### 🔍 Classification Result")
                    st.info(classification_result)
                    
                except Exception as e:
                    st.error(f"An error occurred while contacting Groq: {e}")
