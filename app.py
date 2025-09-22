import os
import json
import streamlit as st
from dotenv import load_dotenv

# LangChain latest imports
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()

# ------------------------------
# Streamlit Page Configuration
# ------------------------------
st.set_page_config(
    page_title="EHR Agent - PRAL MVP",
    page_icon="🏥",
    layout="wide"
)

# ------------------------------
# OpenAI API Key Setup
# ------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ OpenAI API key missing! Please add it in Streamlit Secrets or .env file.")
    st.stop()

# Initialize LLM
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model="gpt-4o-mini",   # Lightweight and cost-efficient
    temperature=0
)

# Initialize Memory for learning step
memory = ConversationBufferMemory(memory_key="chat_history")

# ------------------------------
# PRAL Step Functions
# ------------------------------

def perceive():
    """Step 1: Perceive - Capture patient data (simulated EHR JSON)"""
    patient_data = {
        "patient_id": "P-12345",
        "name": "John Doe",
        "dob": "1985-06-15",
        "diagnosis": "Hypertension",
        "medications": ["Lisinopril", "Aspirin"],
        "blood_pressure": 165,
        "last_visit": "2025-09-20"
    }
    return json.dumps(patient_data, indent=2)

def reason(patient_json):
    """Step 2: Reason - AI explains reasoning behind decision."""
    prompt = f"""
    You are a medical AI assistant analyzing this patient data.

    Task:
    1. Determine if urgent care is required.
    2. Provide step-by-step reasoning.
    3. Make it understandable for both a 10-year-old child and a non-technical hospital board member.

    Patient Data:
    {patient_json}

    Respond in this format:
    - Risk Level: (Low / Moderate / High)
    - Reasoning: (clear explanation)
    - Recommended Action:
    """
    return llm.predict(prompt)

def act(reasoning_text):
    """Step 3: Act - Decide what to do based on reasoning."""
    if "High" in reasoning_text or "urgent" in reasoning_text.lower():
        return "🚨 ALERT: Immediate attention required. Nurse and doctor notified."
    elif "Moderate" in reasoning_text:
        return "⚠️ Action: Follow-up scheduled within 24 hours."
    else:
        return "✅ No urgent action needed at this time."

def learn(reasoning_text):
    """Step 4: Learn - Store reasoning in memory for future improvement."""
    memory.save_context({"input": "Patient reasoning"}, {"output": reasoning_text})
    return "Memory updated with latest reasoning."

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("🏥 EHR Agent - PRAL MVP")
st.caption("Perceive → Reason → Act → Learn | Start → Run → Check → Loop")

st.sidebar.header("Choose a Demo")
demo_choice = st.sidebar.radio(
    "Select a demo to run:",
    ["Demo 1 - Perceive", "Demo 2 - Reasoning", "Demo 3 - Full PRAL Loop"]
)

# ------------------------------
# DEMO 1: Perceive
# ------------------------------
if demo_choice == "Demo 1 - Perceive":
    st.subheader("Demo 1: Perceive")
    st.write("Simulating patient data collection from an EHR system.")
    data = perceive()
    st.code(data, language="json")

# ------------------------------
# DEMO 2: Reasoning
# ------------------------------
elif demo_choice == "Demo 2 - Reasoning":
    st.subheader("Demo 2: Reasoning About Patient Data")
    st.write("AI will analyze patient data and explain its decision clearly.")

    data = perceive()
    st.write("### Patient Data")
    st.code(data, language="json")

    st.write("### AI Reasoning")
    reasoning = reason(data)
    st.write(reasoning)

# ------------------------------
# DEMO 3: Full PRAL Loop
# ------------------------------
elif demo_choice == "Demo 3 - Full PRAL Loop":
    st.subheader("Demo 3: Full PRAL Loop Simulation")
    st.write("Simulating the entire loop: Start → Run → Check → Perceive → Reason → Act → Learn → Loop")

    # Step 1: Perceive
    st.write("**Step 1: Perceive - Capturing Patient Data**")
    data = perceive()
    st.code(data, language="json")

    # Step 2: Reason
    st.write("**Step 2: Reason - AI Analysis**")
    reasoning = reason(data)
    st.write(reasoning)

    # Step 3: Act
    st.write("**Step 3: Act - Taking Action**")
    action_result = act(reasoning)
    st.success(action_result)

    # Step 4: Learn
    st.write("**Step 4: Learn - Updating Memory**")
    learning_status = learn(reasoning)
    st.info(learning_status)

    # Step 5: Loop
    st.write("**Step 5: Loop - Current Memory**")
    st.json(memory.buffer)
