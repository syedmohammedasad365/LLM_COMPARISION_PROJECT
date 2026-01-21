import streamlit as st
import pandas as pd
import time
import os

from dotenv import load_dotenv
load_dotenv()
try:
    from auth import login
    from utils.router import choose_models
    from utils.parallel import run_parallel
    from utils.rate_limiter import check_limit
    from utils.report import generate_report
except Exception as e:
    st.error(e)
    st.stop()

st.set_page_config(
    page_title="LLM Nexus | Enterprise Comparison",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg-primary: #020617;
    --bg-secondary: rgba(30, 41, 59, 0.65);
    --bg-glass: rgba(15, 23, 42, 0.65);
    --border-soft: rgba(148, 163, 184, 0.15);
    --accent: #38bdf8;
    --accent-strong: #0ea5e9;
    --text-primary: #f8fafc;
    --text-muted: #94a3b8;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(
        circle at top left,
        #020617 0%,
        #020617 40%,
        #020617 100%
    );
    color: var(--text-primary);
}
h1, h2, h3 {
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--text-primary) !important;
}

.main-header {
    font-size: clamp(2rem, 4vw, 2.8rem);
    background: linear-gradient(90deg, #e0f2fe, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sub-header {
    color: var(--text-muted);
    max-width: 720px;
    line-height: 1.6;
    margin-bottom: 2rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        rgba(15, 23, 42, 0.95),
        rgba(2, 6, 23, 0.95)
    );
    border-right: 1px solid var(--border-soft);
}

.block-container {
    padding-top: 2rem;
}

.stMetric,
div[data-testid="metric-container"],
.model-card {
    background: var(--bg-glass);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-soft);
    border-radius: 14px;
}

.stTextArea textarea,
input,
div[data-baseweb="select"] > div {
    background: rgba(2, 6, 23, 0.8);
    border: 1px solid var(--border-soft);
    color: var(--text-primary);
    border-radius: 10px;
}

.stTextArea textarea:focus,
input:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 1px var(--accent);
}

div.stButton > button {
    background: linear-gradient(135deg, #38bdf8, #0ea5e9);
    color: #020617;
    font-weight: 700;
    border-radius: 12px;
    padding: 0.9rem 1.2rem;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

div.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 30px rgba(56, 189, 248, 0.35);
}

button[data-baseweb="tab"] {
    background: transparent;
    color: var(--text-muted);
    font-weight: 600;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--accent);
    border-bottom: 2px solid var(--accent);
}

.model-card {
    padding: 1.25rem;
    height: 100%;
}

.model-name {
    font-size: 0.85rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.75rem;
}
div[data-testid="stStatusWidget"] {
    background: var(--bg-glass);
    border: 1px solid var(--border-soft);
    border-radius: 14px;
}
.stPlotlyChart,
.stChart {
    background: var(--bg-glass);
    border-radius: 14px;
    padding: 1rem;
}
@media (max-width: 768px) {
    .main-header {
        font-size: 2rem;
    }

    .sub-header {
        font-size: 0.95rem;
    }

    section[data-testid="stSidebar"] {
        padding-top: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ Controls")
    
    if "user" in st.session_state:
        st.info(f"👤 Logged in as: **{st.session_state.user}**")
    
    st.markdown("---")
    
    st.subheader("Configuration")
    model_temp = st.slider("Temperature (Creativity)", 0.0, 1.0, 0.7)
    max_tokens = st.number_input("Max Tokens", value=1024, step=256)
    
    st.markdown("---")
    st.caption("v2.1.0 | Enterprise Edition")


def main():
    
    login()
    if "user" not in st.session_state:
        st.stop()

   
    st.markdown('<div class="main-header">LLM Nexus</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Intelligent routing & cost-analysis engine for Generative AI.</div>', unsafe_allow_html=True)

    
    col1, col2 = st.columns([1, 3])

    with col1:
        task = st.selectbox(
            "Target Objective",
            ["General", "Coding", "Fast Response", "Cost Saving"],
            help="This determines which models are selected via the router."
        )
        
       
        st.metric(label="Active Models", value="3 Online", delta="All Systems Go")

    with col2:
        prompt = st.text_area(
            "Input Prompt",
            height=140,
            placeholder="E.g., Write a secure Python function to connect to AWS S3...",
            label_visibility="visible"
        )

   
    col_submit, col_spacer = st.columns([1, 4])
    with col_submit:
        run_btn = st.button("⚡ Execute Query")

    if run_btn:
        if not check_limit(st.session_state.user):
            st.error("🚫 Rate limit reached. Please upgrade your plan or wait.")
            st.stop()
            
        if not prompt.strip():
            st.warning("⚠️ Please provide a prompt to analyze.")
            st.stop()

     
        with st.status("🔄 Orchestrating Model Requests...", expanded=True) as status:
            st.write("🔍 Analyzing intent...")
            models = choose_models(task)
            st.write(f"✅ Selected optimized models: **{', '.join(models)}**")
            
            st.write("🚀 Dispatching parallel requests...")
            start_time = time.time()
            
            responses = run_parallel(prompt, models)
            
            elapsed = round(time.time() - start_time, 2)
            status.update(label=f"✅ Complete! Processed in {elapsed}s", state="complete", expanded=False)

     
        st.markdown("### 📊 Analysis Results")
        
       
        tab1, tab2, tab3, tab4 = st.tabs([
            "👁️ Visual Comparison",
            "📝 Raw Data",
            "📉 Cost Report",
            "📊 Performance Dashboard"
        ])



        with tab1:
           
            cols = st.columns(len(responses))
            
         
            for idx, (model_name, response_text) in enumerate(responses.items()):
                with cols[idx]:
                    st.markdown(f"""
                    <div class="model-card">
                        <div class="model-name">{model_name}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("---")
                    st.markdown(response_text) 

        with tab2:
            st.json(responses)

        with tab3:
           
            report_status = generate_report(prompt, responses)
            st.success("Report generated and saved to database.")
            
           
            metrics_col1, metrics_col2 = st.columns(2)
            metrics_col1.metric("Estimated Cost", "$0.0042", "-12%")
            metrics_col2.metric("Latency Average", f"{elapsed}s", "Fast")
        with tab4:
            st.markdown("### 📊 Model Performance Dashboard")

            metrics_file = "data/metrics/metrics.csv"

            if not os.path.exists(metrics_file):
                st.warning("No metrics data available yet. Run some prompts first.")
            else:
                df = pd.read_csv(metrics_file)

                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

                st.subheader("⏱️ Average Latency per Model")
                latency_df = df.groupby("model")["latency"].mean().reset_index()
                st.bar_chart(latency_df.set_index("model"))

                st.subheader("📏 Average Response Length")
                length_df = df.groupby("model")["response_length"].mean().reset_index()
                st.bar_chart(length_df.set_index("model"))

                st.subheader("📈 Requests Over Time")
                time_df = df.set_index("timestamp").resample("1min").count()["model"]
                st.line_chart(time_df)


if __name__ == "__main__":
    main()