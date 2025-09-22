import os
import json
import requests
import pandas as pd
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool, initialize_agent

# ==============================
# CONFIGURATION
# ==============================
st.set_page_config(page_title="Healthcare Agentic AI MVP", layout="wide")
st.title("🏥 Healthcare Agentic AI - MVP Demo")
st.write("This demo follows the Agentic Loop: **Start → Run → Check → Perceive → Reason → Act → Learn → Loop**")

# Set OpenAI Key (can be set in Streamlit Secrets for security)
OPENAI_API_KEY = st.text_input("Enter your OpenAI API Key", type="password")
if not OPENAI_API_KEY:
    st.warning("⚠️ Please enter your OpenAI API Key to continue")
    st.stop()

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# ==============================
# LANGCHAIN SETUP
# ==============================
llm = ChatOpenAI(temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ==============================
# DUMMY EHR DATA SIMULATION
# ==============================
def fetch_patient_data():
    """Simulated FHIR patient data"""
    patient_data = {
        "id": "P12345",
        "name": "John Doe",
        "dob": "1980-01-01",
        "diagnosis": "Hypertension",
        "medications": ["Lisinopril"],
        "last_update": "2025-09-22"
    }
    return json.dumps(patient_data, indent=2)

# ==============================
# AGENT FUNCTIONS
# ==============================
def perceive():
    return fetch_patient_data()

def compliance_check(patient_json):
    patient = json.loads(patient_json)
    violations = []
    
    if not patient.get("dob"):
        violations.append("Missing Date of Birth")
    
    if "Lisinopril" in patient.get("medications", []):
        violations.append("Medication review needed: Lisinopril")

    if len(violations) == 0:
        return "✅ No compliance violations."
    return "⚠️ Violations Found: " + ", ".join(violations)

def act_on_violations(patient_json, violations):
    if "No compliance violations" in violations:
        return "✅ No action required. All records are safe."
    return f"🚨 ALERT: Nurse notified about -> {violations}"

# ==============================
# DEFINE TOOLS FOR LANGCHAIN
# ==============================
perceive_tool = Tool(
    name="Perceive",
    func=lambda _: perceive(),
    description="Collect patient data from EHR"
)

check_tool = Tool(
    name="CheckCompliance",
    func=compliance_check,
    description="Check patient record for compliance issues"
)

act_tool = Tool(
    name="Act",
    func=lambda data: act_on_violations(data, compliance_check(data)),
    description="Take action on compliance violations"
)

agent = initialize_agent(
    tools=[perceive_tool, check_tool, act_tool],
    llm=llm,
    agent="zero-shot-react-description",
    memory=memory,
    verbose=True
)

# ==============================
# STREAMLIT UI
# ==============================
st.sidebar.header("Demo Controls")
demo_choice = st.sidebar.selectbox("Choose a Demo", ["Demo 1 - Perceive", "Demo 2 - Check", "Demo 3 - Full Loop"])

if demo_choice == "Demo 1 - Perceive":
    st.subheader("Demo 1: Patient Data Perception")
    data = perceive()
    st.code(data, language="json")
    st.success("Perceived raw patient data successfully.")

elif demo_choice == "Demo 2 - Check":
    st.subheader("Demo 2: Compliance Check")
    data = perceive()
    result = compliance_check(data)
    st.write("### Compliance Result")
    st.write(result)

elif demo_choice == "Demo 3 - Full Loop":
    st.subheader("Demo 3: Full Agentic Loop")
    st.write("Simulating Start → Run → Check → Perceive → Reason → Act → Learn → Loop")

    data = perceive()
    st.write("**Step 1 - Perceive:** Patient Data Fetched")
    st.code(data, language="json")

    check_result = compliance_check(data)
    st.write("**Step 2 - Check & Reason:**")
    st.write(check_result)

    action_result = act_on_violations(data, check_result)
    st.write("**Step 3 - Act:**")
    st.write(action_result)

    # Learn by saving into memory
    agent.run(f"Learning from today's cycle: {action_result}")
    st.write("**Step 4 - Learn & Loop:** Memory Updated")

    # Display memory for audit
    st.write("### Agent Memory Log")
    st.json(memory.buffer)

st.info("💡 Tip: Run each demo to see the agent evolve step-by-step.")
