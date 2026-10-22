import time
import streamlit as st
from google import genai
from prompts import SYSTEM_PROMPT

# Gemini Client
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# Sidebar
with st.sidebar:

    st.markdown("""
# 🚀 Endpoint AI

### Enterprise Troubleshooting Assistant
""")

    st.info("""
Built by Sachleen Panesar

6+ Years Experience

1000+ Endpoints Managed
""")

    st.subheader("Core Skills")

    st.markdown("""
✅ SCCM/MECM

✅ Intune

✅ Active Directory

✅ Group Policy

✅ BitLocker

✅ Windows Defender

✅ Office 365

✅ PowerShell
""")

    st.subheader("Use Cases")

    st.markdown("""
🔍 SCCM Troubleshooting

🔍 Intune Compliance

🔍 Windows Patching

🔍 OSD Failures

🔍 PowerShell Generation

🔍 Log Analysis
""")

    st.divider()

    st.caption("Powered by Sachleen Panesar")



# Title

st.title("AI Endpoint Troubleshooting Agent")

st.markdown("""
**Built by Sachleen Panesar**

Senior Endpoint Engineer | SCCM | Intune | Active Directory | PowerShell
""")

st.success(
    "Recruiters: Try SCCM, Intune, BitLocker, Active Directory, OSD, Windows Update, or PowerShell troubleshooting scenarios."
)

# Clear button

if st.button("🔄 Clear"):
    st.rerun()

# Example Issues

st.markdown("""
### Example Issues To Test

- SCCM client not receiving policies
- OSD Task Sequence fails with 0x80070002
- Intune device marked non-compliant
- BitLocker recovery key missing
- Windows Update KB installation failed
- Generate PowerShell script to check SCCM client health
""")

# Quick Test Buttons

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("SCCM Issue"):
        st.session_state.issue = "SCCM client not receiving machine policies"

with col2:
    if st.button("Intune Issue"):
        st.session_state.issue = "Intune device showing non-compliant"

with col3:
    if st.button("BitLocker Issue"):
        st.session_state.issue = "BitLocker recovery key missing"

# Log Upload

uploaded_file = st.file_uploader(
    "Upload SCCM / Intune Log",
    type=["log", "txt"]
)

st.info(
    "Supported Logs: CCMExec.log, PolicyAgent.log, LocationServices.log, AppEnforce.log, SMSTS.log"
)

# Input box

default_issue = st.session_state.get("issue", "")

user_issue = st.text_area(
    "Describe your SCCM, Intune, AD or Windows issue",
    value=default_issue
)

# Analysis

if st.button("🔍 Analyze Issue"):

    log_content = ""

    if uploaded_file is not None:

        try:
            log_content = uploaded_file.read().decode("utf-8")

            # Limit size for speed
            log_content = log_content[:3000]

        except:
            log_content = "Unable to read uploaded log."

    # Build prompt

    if log_content:

        full_prompt = f"""


Issue:
{user_issue}

Log:
{log_content}
"""

    else:

        full_prompt = f"""


Issue:
{user_issue}
"""

    try:

        progress = st.progress(0)
        status = st.empty()

        status.text("Preparing request...")
        progress.progress(25)

        start_time = time.time()

        status.text("Sending to Gemini...")
        progress.progress(50)

        response = client.models.generate_content(
            model="Gemini 3 Flash Live",
            contents=full_prompt
        )

        progress.progress(90)

        report_text = response.text

        elapsed = round(time.time() - start_time, 2)

        status.text("Analysis completed")
        progress.progress(100)

        st.success(f"✅ Completed in {elapsed} seconds")

        # Metrics

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Response Time",
                f"{elapsed}s"
            )

        with col2:
            st.metric(
                "Log Size",
                f"{len(log_content)} chars"
            )

        # Report

        st.markdown(report_text)

        # Download button

        st.download_button(
            label="📥 Download Troubleshooting Report",
            data=report_text,
            file_name="Endpoint_Report.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"Error: {e}")

# Footer

st.divider()

st.caption(
    "⚡ Powered by Gemini | Streamlit | Python"
)
