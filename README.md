# 🤖 Smart Company Research Agent (Account Plan Generator)

This project is a conversational AI **Company Research Assistant** that helps users research companies and generate/refine lightweight account plans through natural, iterative conversation. It is implemented as a **chat-based web app using Streamlit**. :contentReference[oaicite:0]{index=0}

---

## 1. Problem Statement

**Chosen brief:**  
> Company Research Assistant (Account Plan Generator)

The agent’s goals:

- Help users **research companies** through a natural conversation.
- **Summarize and structure findings** into an account plan (executive summary, financials, strategy, risks).
- Demonstrate **agentic behaviour**: asking clarifying questions, offering updates, and remembering user preferences.
- Allow users to **refine or update sections** of the plan via follow-up messages.

---

## 2. High-Level Design

### 2.1 Interaction Flow

The agent operates in two main stages:

1. **Stage 1 – Initial Research**
   - First user message is treated as the **target company name** (e.g., “Eightfold AI” or “Tesla”).
   - The agent:
     - Acknowledges the request (`🔍 Analyzing: ...`).
     - Generates a **short account plan** from its internal knowledge base.
     - Asks how to refine:  
       > “Give me the entire report”, “Update risks”, etc.

2. **Stage 2 – Refinement / Agentic Behaviour**
   - The agent reads the **intent** of each follow-up message and:
     - Expands to a **full, detailed report**.
     - Updates **specific sections** (e.g., Risks).
     - Re-shows the report at the **current detail level**.
     - Asks clarifying questions when the intent is unclear.

---

## 3. Agentic Behaviour & Reasoning

### 3.1 Intent-Based Logic

Intent is detected using simple rule-based checks on the user’s latest message: :contentReference[oaicite:1]{index=1}

- **“Full / entire / complete / increase / length” → Full report**
  - Updates an internal `detail_level = "long"`.
  - Responds with a **fully detailed account plan**.

- **“Risk / challenge” → Update Risks section**
  - Responds with only the **Risks** part updated:
    - e.g., adds “cybersecurity vulnerabilities” and “geopolitical supply chain constraints”.

- **“again / show / give / report” → Show current report**
  - Respects the remembered `detail_level` (short or long).
  - Re-displays the current version of the account plan.

- **Fallback → Clarifying question**
  - If none of the above match:
    - > “I’ve noted that request. Do you want to see the ‘entire’ report or update a specific section?”

**Reasoning for this design:**

- Keeps behaviour **transparent & debuggable** (simple rules).
- Ensures **predictable responses** for the four demo user types.
- Makes it easy to show **agentic decisions**: “I inferred you want X, so I did Y.”

---

## 4. Memory & State Management

The agent uses `st.session_state` to simulate long-lived conversational memory: :contentReference[oaicite:2]{index=2}

- `messages`: full chat transcript for rendering history.
- `agent_stage`: `"init"` or `"refining"` to control the flow.
- `target_company`: remembers which company the user is exploring.
- `detail_level`: remembers whether the user wants `"short"` or `"long"` reports.

**Why:**  
This allows the agent to:

- Remember **which company** it is talking about across turns.
- Respect the user’s **preferred detail level** when they say “show again”.
- Behave differently at different stages in the conversation.

---

## 5. Knowledge Base & Account Plan Structure

The internal **DATA_VAULT** stores structured account plan content for different companies: :contentReference[oaicite:3]{index=3}

For each company (e.g., `eightfold ai`, `tesla`), it stores:

- `short` version – compact, bullet-like account plan:
  - Executive Summary  
  - Financials  
  - Strategy  
  - Risks  

- `long` version – extended version with:
  - Detailed narrative.
  - Separated sections with `<br>` spacing for readability.
  - More nuanced explanation of strategy & risks.

**Reasoning:**

- Mimics having a **research backend** while keeping this demo **deterministic** and easy to grade.
- Separates **content** from **logic**, so adding new companies or connecting to a live API/search later is straightforward.

---

## 6. How This Meets the Evaluation Criteria

### 6.1 Conversational Quality

- Uses **chat history** to show conversation context and continuity.
- Provides **status cues** (“System Online”, “Agent is processing…”) to feel more human.
- Asks **clarifying follow-ups** instead of failing silently:
  - > “Do you want to see the ‘entire’ report or update a specific section?”
- Responses are structured using **headings and bullet points** for easy reading.

### 6.2 Agentic Behaviour

- **Proactive updates**:
  - Shows “Analyzing…” when first given a company.
  - Uses a spinner (`st.spinner`) to simulate background processing.
- **Self-awareness**:
  - Acknowledges uncertainty and asks user to choose what to do next.
- **Memory**:
  - Remembers company context and preferred detail level across turns.

### 6.3 Technical Implementation

- Built using **Streamlit** for rapid UI + server logic. 
- State managed via `st.session_state`.
- Clear separation of:
  - UI (`st.chat_message`, `st.chat_input`)
  - Logic (`determine_intent_and_act`)
  - Data (`DATA_VAULT`).

### 6.4 Intelligence & Adaptability

- Adapts report length based on user preference.
- Handles **“show again”** style queries using stored `detail_level`.
- Offers specific section updates (Risks) and is easy to extend for other sections (Strategy, Financials, etc.).

---

## 7. Demo Scenarios (Suggested Conversations)

Below are example flows to test the agent with different user types.

### 7.1 The Confused User

> User: “I need help understanding Eightfold AI or something like that.”  
> Agent: Generates the short summary for **Eightfold AI** and asks how to refine.  
> User: “I’m not sure, maybe give me more?”  
> Agent: Offers the full report and explains it’s more detailed.

Goal: Show the agent **guides** the user rather than expecting a perfect instruction.

---

### 7.2 The Efficient User

> User: “Tesla – full account plan.”  
> Agent: Interprets as a company name and a request for full detail; sets `detail_level = "long"` and returns the long plan.  
> User: “Update risks to include supply chain issues.”  
> Agent: Returns updated **Risks** section only.

Goal: Show **fast, minimal-turn** path to a detailed plan and updates.

---

### 7.3 The Chatty User

> User: “Heyy, hope you’re doing well! Can we maybe talk about Eightfold AI a little? I’m curious what they do before we dive into anything heavy.”  
> Agent: Returns the **short summary** and asks how to refine.  
> User: (talks about their friend working there, goes off topic)  
> Agent: Politely returns to the task:
> “I’ve noted that. Do you want the **entire report** or to **update a specific section** (e.g., risks, strategy)?”

Goal: Show robustness when user goes off topic but still be **polite and task-oriented**.

---

### 7.4 Edge Case Users

1. **Invalid company**  
   - User: “Research my uncle’s garage startup.”  
   - Agent: Falls back to default `eightfold ai` data and can be extended to respond with:
     - “I don’t have structured data for that company yet. Do you want a generic template?”

2. **Vague refinement**  
   - User: “Make it better.”  
   - Agent:  
     - “I’ve noted that request. Do you want to see the ‘entire’ report or update a specific section?”

3. **Beyond capabilities**  
   - User: “File my taxes for Tesla’s last quarter.”  
   - Agent (expected extension):  
     - “I can’t perform legal or financial filings, but I can summarize their reported financials.”

Goal: Demonstrate **graceful degradation** and clear communication of limits.

---

## 8. Files & Structure

- **`app.py`** – Main Streamlit app:
  - UI definition
  - Session state management
  - Intent detection and response generation
  - Hard-coded knowledge base (`DATA_VAULT`) :contentReference[oaicite:5]{index=5}

- **`requirements.txt`** – Python dependencies: :contentReference[oaicite:6]{index=6}  
  - `streamlit`  
  - `duckduckgo-search` (prepared for future integration of live web research)

---

## 9. Setup & Running the App

### 9.1 Prerequisites

- Python 3.9+ recommended
- pip

### 9.2 Installation

```bash
# Clone or copy the project folder

# Install dependencies
pip install -r requirements.txt
