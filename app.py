import streamlit as st
import json
from transformers import pipeline

# ------------------------------
# Lightweight free model setup
# ------------------------------
@st.cache_resource
def load_model():
    # Free Hugging Face model
    return pipeline("text-generation", model="distilgpt2")

model = load_model()

# ------------------------------
# PRAL Step Functions
# ------------------------------
def perceive():
    """Step 1: Perceive - Simulate capturing patient data."""
    patient_data = {
        "patient_id": "P-001",
        "name": "John Doe",
        "dob": "1985-06-15",
        "diagnosis": "Hypertension",
        "medications": ["Lisinopril", "Aspirin"],
        "blood_pressure": 170,
        "last_visit": "2025-09-20"
    }
    return json.dumps(patient_data, indent=2)

def reason(patient_json):
    """Step 2: Reason - Explain what AI thinks using free model."""
    prompt = (
        "You are a healthcare assistant. Analyze this patient data and "
        "explain in simple words if the patient needs urgent care.\n\n"
        f"Patient Data:\n{patient_json}\n\n"
        "Response:"
    )
    result = model(prompt, max_length=200, num_return_sequences=1)
    return result[0]['generated_text']

def act(reasoning_text):
    """Step 3: Act - Simple decision making."""
    if "high blood pressure" in reasoning_text.lower() or "urgent" in reasoning_text.lower():
        return "🚨 ALERT: Immediate attention required. Notify doctor now."
    elif "follow-up" in reasoning_text.lower():
        return "⚠️ Schedule a follow-up appointment within 24 hours."
    else:
        return "✅ No urgent action needed right now."

def learn(reasoning_text, memory_list):
    """Step 4: Learn - Store reasoning for later reference."""
    memory_list.append(reasoning_text)
    return memory_list

# ------------------------------
# Streamlit App UI
# ------------------------------
st.set_page_config(page_title="EHR PRAL Agent", layout="wide")

st.title("🏥 Free EHR Agent - PRAL MVP")
st.caption("Perceive → Reason → Act → Learn → Loop | 100% Free and Lightweight")

# Memory to simulate AI learning
if "memory" not in st.session_state:
    st.session_state.memory = []

# Sidebar Navigation
demo_choice = st.sidebar.radio(
    "Choose a demo:",
    ["Demo 1 - Perceive", "Demo 2 - Reasoning", "Demo 3 - Full PRAL Loop"]
)

# ------------------------------
# DEMO 1: Perceive
# ------------------------------
if demo_choice == "Demo 1 - Perceive":
    st.subheader("Demo 1: Perceive")
    st.write("Capturing patient data like a hospital EHR system.")
    data = perceive()
    st.code(data, language="json")

# ------------------------------
# DEMO 2: Reasoning
# ------------------------------
elif demo_choice == "Demo 2 - Reasoning":
    st.subheader("Demo 2: Reasoning")
    st.write("The free model will analyze patient data and explain in simple language.")

    data = perceive()
    st.write("### Patient Data")
    st.code(data, language="json")

    st.write("### AI Reasoning")
    reasoning = reason(data)
    st.text_area("Reasoning Output", reasoning, height=150)

# ------------------------------
# DEMO 3: Full PRAL Loop
# ------------------------------
elif demo_choice == "Demo 3 - Full PRAL Loop":
    st.subheader("Demo 3: Full PRAL Loop Simulation")
    st.write("Start → Run → Check → Perceive → Reason → Act → Learn → Loop")

    # Step 1: Perceive
    st.write("**Step 1: Perceive - Capturing Patient Data**")
    data = perceive()
    st.code(data, language="json")

    # Step 2: Reason
    st.write("**Step 2: Reason - Analyzing Patient Data**")
    reasoning = reason(data)
    st.text_area("Reasoning Output", reasoning, height=150)

    # Step 3: Act
    st.write("**Step 3: Act - Taking Action Based on Reasoning**")
    action = act(reasoning)
    st.success(action)

    # Step 4: Learn
    st.write("**Step 4: Learn - AI Improves Over Time**")
    st.session_state.memory = learn(reasoning, st.session_state.memory)
    st.write("**Memory Log:**")
    st.json(st.session_state.memory)
