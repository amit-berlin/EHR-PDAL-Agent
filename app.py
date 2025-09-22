import streamlit as st
import json

# ------------------------------
# Streamlit Page Configuration
# ------------------------------
st.set_page_config(page_title="Library-Free EHR - PRAL MVP", layout="wide")
st.title("🏥 Library-Free EHR - PRAL MVP")
st.caption("Perceive → Reason → Act → Learn → Loop | Start → Run → Check → Loop")

# ------------------------------
# Memory to simulate learning
# ------------------------------
if "memory" not in st.session_state:
    st.session_state.memory = []

# ------------------------------
# PRAL Agent (Pure Python without Heavy Langchain Library)
# ------------------------------

def perceive():
    """Step 1: Capture patient data"""
    patient_data = {
        "patient_id": "P-001",
        "name": "John Doe",
        "dob": "1985-06-15",
        "diagnosis": "Hypertension",
        "medications": ["Lisinopril", "Aspirin"],
        "blood_pressure": 170,
        "last_visit": "2025-09-20"
    }
    return patient_data

def reason(patient_data):
    """Step 2: Analyze data and give reasoning"""
    bp = patient_data.get("blood_pressure", 0)
    reasoning = {}
    if bp >= 160:
        reasoning["Risk Level"] = "High"
        reasoning["Explanation"] = f"Patient has dangerously high blood pressure: {bp} mmHg."
        reasoning["Recommended Action"] = "Alert doctor immediately and start monitoring."
    elif bp >= 140:
        reasoning["Risk Level"] = "Moderate"
        reasoning["Explanation"] = f"Patient blood pressure is elevated: {bp} mmHg."
        reasoning["Recommended Action"] = "Schedule follow-up within 24 hours."
    else:
        reasoning["Risk Level"] = "Low"
        reasoning["Explanation"] = f"Patient blood pressure is normal: {bp} mmHg."
        reasoning["Recommended Action"] = "Continue normal care."
    return reasoning

def act(reasoning):
    """Step 3: Act based on reasoning"""
    action = reasoning.get("Recommended Action", "No action needed.")
    return action

def learn(reasoning):
    """Step 4: Learn and store reasoning in memory"""
    st.session_state.memory.append(reasoning)
    return st.session_state.memory

# ------------------------------
# Sidebar Navigation
# ------------------------------
demo_choice = st.sidebar.radio(
    "Choose a demo:",
    ["Demo 1 - Perceive", "Demo 2 - Reasoning", "Demo 3 - Full PRAL Loop"]
)

# ------------------------------
# DEMO 1: Perceive Agent 
# ------------------------------
if demo_choice == "Demo 1 - Perceive":
    st.subheader("Demo 1: Perceive")
    st.write("Simulated patient data capture:")
    patient_data = perceive()
    st.json(patient_data)

# ------------------------------
# DEMO 2: Reasoning Agent 
# ------------------------------
elif demo_choice == "Demo 2 - Reasoning":
    st.subheader("Demo 2: Reasoning")
    patient_data = perceive()
    st.write("### Patient Data")
    st.json(patient_data)
    st.write("### Reasoning")
    reasoning = reason(patient_data)
    st.json(reasoning)

# ------------------------------
# DEMO 3: Full PRAL Loop Agent
# ------------------------------
elif demo_choice == "Demo 3 - Full PRAL Loop":
    st.subheader("Demo 3: Full PRAL Loop")
    
    st.write("**Step 1: Perceive**")
    patient_data = perceive()
    st.json(patient_data)
    
    st.write("**Step 2: Reason**")
    reasoning = reason(patient_data)
    st.json(reasoning)
    
    st.write("**Step 3: Act**")
    action = act(reasoning)
    st.success(action)
    
    st.write("**Step 4: Learn**")
    memory = learn(reasoning)
    st.write("**Memory Log**")
    st.json(memory)
