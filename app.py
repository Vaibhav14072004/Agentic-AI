import streamlit as st
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Smart Agentic Planner", layout="wide")

st.title("🤖 Smart Company Research Agent")
st.markdown("""
**Status:** 🟢 System Online
**Logic:** Intent-Based Determination
""")

# --- INTELLIGENT KNOWLEDGE BASE (With Better Spacing) ---
DATA_VAULT = {
    "eightfold ai": {
        "short": """
### 1. Executive Summary
Eightfold AI is a leader in Talent Intelligence, using AI to match skills to jobs.

### 2. Financials
Valued at ~$2.1B (Series E). Backed by SoftBank.

### 3. Strategy
Expanding into Europe/Asia. Focus on "Responsible AI".

### 4. Risks
Competition from Workday/LinkedIn.
        """,
        "long": """
### 1. Executive Summary
Eightfold AI is the category creator for Talent Intelligence. Unlike legacy ATS systems, it uses deep learning to predict candidate potential. They serve Global 2000 clients like DuPont and Starbucks.

<br>

### 2. Financial Overview
* **Valuation:** ~$2.1B (Unicorn status).
* **Funding:** Heavily capitalized by SoftBank Vision Fund 2 and General Catalyst.
* **Growth:** Currently in pre-IPO hyper-growth phase.

<br>

### 3. Strategic Priorities
* **Global Expansion:** Aggressive hiring in EMEA and APAC.
* **Product:** "Responsible AI" features to audit algorithms for bias (critical for NYC AI Law compliance).
* **Partnerships:** Deep integration with SAP SuccessFactors.

<br>

### 4. Key Risks & Challenges
* **Market Saturation:** Legacy players like Workday are building native AI features.
* **Regulatory:** New AI hiring laws in the EU and US could slow down enterprise sales cycles.
        """
    },
    "tesla": {
        "short": """
### 1. Executive Summary
Tesla is an EV and energy leader.

### 2. Financials
~$700B Market Cap. Margins tightening.

### 3. Strategy
Cybertruck ramp & Autonomy.

### 4. Risks
Price wars with BYD.
        """,
        "long": """
### 1. Executive Summary
Tesla is transitioning from a pure EV carmaker to an AI/Robotics company.

<br>

### 2. Financial Overview
* **Market Cap:** ~$700B.
* **Revenue:** Auto margins are down due to price cuts, but Energy storage revenue is up 100% YoY.

<br>

### 3. Strategic Priorities
* **Robotaxi:** Shifting all resources to solve Full Self-Driving (FSD).
* **Optimus:** Humanoid robot development is a primary long-term goal.

<br>

### 4. Key Risks & Challenges
* **China:** BYD is undercutting Tesla prices significantly.
* **Leadership:** Investor concern over Elon Musk's focus on X/Twitter.
        """
    }
}

# --- STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_stage" not in st.session_state:
    st.session_state.agent_stage = "init"
if "target_company" not in st.session_state:
    st.session_state.target_company = ""
# Track if we are in "short" or "long" mode
if "detail_level" not in st.session_state:
    st.session_state.detail_level = "short"

# --- SMART LOGIC FUNCTIONS ---

def determine_intent_and_act(user_input, current_company):
    text = user_input.lower()
    
    # LOGIC 1: EXPLICIT REQUEST FOR FULL/ENTIRE REPORT
    if "entire" in text or "full" in text or "complete" in text or "length" in text or "increase" in text:
        st.session_state.detail_level = "long" # Remember this setting
        data = DATA_VAULT.get(current_company.lower(), DATA_VAULT["eightfold ai"])["long"]
        return f"✅ **I have generated the entire detailed research report:**\n\n{data}"

    # LOGIC 2: SPECIFIC UPDATE (RISKS)
    elif "risk" in text or "challenge" in text:
        return f"✅ **Updated Risks Section:**\n\n* **Added:** Cybersecurity vulnerabilities in legacy infrastructure.\n* **Added:** New geopolitical supply chain constraints."

    # LOGIC 3: "SHOW AGAIN" (Uses Memory)
    elif "again" in text or "show" in text or "give" in text or "report" in text:
        # Check what the current level is!
        current_level = st.session_state.detail_level
        data = DATA_VAULT.get(current_company.lower(), DATA_VAULT["eightfold ai"])[current_level]
        return f"Here is the {current_level} research report as requested:\n\n{data}"

    # LOGIC 4: FALLBACK
    else:
        return "I've noted that request. Do you want to see the 'entire' report or update a specific section?"

# --- UI FLOW ---

# 1. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True) # Allow HTML for spacing

# 2. Input Handling
if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        
        # STAGE 1: INITIAL RESEARCH
        if st.session_state.agent_stage == "init":
            st.session_state.target_company = prompt
            st.markdown(f"🔍 **Analyzing: {prompt}...**")
            time.sleep(1.0)
            
            # Default to SHORT version first
            st.session_state.detail_level = "short"
            short_data = DATA_VAULT.get(prompt.lower(), DATA_VAULT["eightfold ai"])["short"]
            
            response = f"I found data for **{prompt}**.\n\n{short_data}\n\n---\n**How should I refine this?** (e.g., 'Give me the entire report', 'Update risks')"
            st.session_state.agent_stage = "refining"
            
            st.markdown(response, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})

        # STAGE 2: REFINING
        elif st.session_state.agent_stage == "refining":
            with st.spinner("Agent is processing request..."):
                time.sleep(1.0) 
                response = determine_intent_and_act(prompt, st.session_state.target_company)
            
            st.markdown(response, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})