from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from utils.report import generate_report
from utils.parallel import run_parallel

st.set_page_config(
    page_title="LLM Comparison Tool", 
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 LLM Comparison Tool")
st.markdown(
    """
    Compare **ChatGPT**, **Gemini**, and **LLaMA**  
    Using a **single unified prompt**.
    """
)

# 🔹 DEFINE PROMPT HERE
prompt = st.text_area(
    "Enter your prompt",
    placeholder="Ask something you want to compare across models...",
    height=150
)

if st.button("Compare Models"):
    if not prompt.strip():
        st.warning("Please enter a prompt")
    else:
        with st.spinner("Running models in parallel..."):
            responses = run_parallel(prompt)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("ChatGPT")
            st.write(responses.get("ChatGPT", ""))
            st.subheader("Gemini")
            st.write(responses.get("Gemini", ""))
        
        with col2:
            st.subheader("LLaMA")
            st.write(responses.get("LLaMA", ""))

        report_path = generate_report(prompt, responses)

        with open(report_path, "rb") as f:
            st.download_button(
                label="📥 Download Comparison Report (CSV)", 
                data=f,
                file_name="llm_comparison_report.csv",
                mime="text/csv"
            )

        st.success("Comparison completed successfully!")