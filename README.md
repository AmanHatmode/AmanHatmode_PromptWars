# 🧠 THE BLIND SPOT: AI Thinking Companion
### *Google for Developers | PromptWars x EI SVPCET | {Build with AI}*

> **"ChatGPT gives you answers. The Blind Spot asks you the right questions so you can make the decision yourself."**

---

## 📌 Problem Statement & Challenge

### The Problem
Humans suffer from the **Availability Heuristic** and **Salience Bias**. When evaluating high-stakes decisions, we anchor on visible, immediate perks (such as a high stipend, a short commute, or a fancy title) while overlooking critical downstream risks, unverified assumptions, and internal contradictions in our reasoning.

### The Challenge
Build an AI-powered thinking companion that spots what might be missing, asks thoughtful questions, and helps users examine their reasoning—**without ever making the decision for the user**.

---

## 🚀 Key Features

1. **Strict Non-Prescriptive Guardrails:**
   * The AI never says *"Accept the offer"* or *"Reject it"*. It provides cognitive scaffolding while leaving 100% of the agency in the user's hands.
2. **Cognitive Bias Identification:**
   * Automatically detects and tags psychological distortions (*Salience Bias, Planning Fallacy, Optimism Bias, Confirmation Bias*).
3. **Unstated Assumptions Audit:**
   * Uncovers hidden premises in feasibility, institutional policies, and bandwidth that the user took for granted.
4. **Gary Klein Pre-Mortem Engine:**
   * Mentally fast-forwards 6 months into the future to simulate an absolute failure mode, revealing catastrophic second-order risks before they happen.
5. **Interactive Socratic Dialogue Loop:**
   * Generates 3 domain-specific probing questions and allows the user to submit and stress-test their defenses interactively.
6. **1-Click Challenge Example Loader:**
   * Instantly loads the official **6-Month Internship Offer** case study for immediate live evaluation.

---

## 🛡️ Enterprise Pillars Built-In

| Pillar | Implementation |
| :--- | :--- |
| **🔐 Security & Auth** | **Supabase Authentication** (email/password JWT tokens) + Judge Guest Mode + **Prompt Injection Defense** (intercepts adversarial jailbreaks like DAN, rule-bypasses, and system prompt leaks). |
| **⚡ Efficiency** | Tiered Google Gemini routing (`gemini-1.5-pro` for deep reasoning, `gemini-1.5-flash` for sub-second classification), memory caching, and low token overhead. |
| **🧪 Testing** | Automated `pytest` suite testing schema conformance and asserting that the engine **never** outputs prescriptive commands. |
| **🔄 Reliability** | **Strict Pydantic v2 Schema validation** with a calibrated deterministic fallback engine ensuring the live demo never fails on stage. |

---

## 🛠️ Technology Stack

* **Foundation LLM:** Google Gemini 1.5 Pro & Gemini 1.5 Flash (`google-generativeai`)
* **Prompt Framework:** Chain-of-Thought (CoT) Scratchpad + Constitutional Guardrails
* **Authentication & Database:** Supabase (Auth & Cloud Postgres)
* **Frontend:** Streamlit with Custom CSS cards & badges
* **Type Validation:** Pydantic v2
* **Testing:** Pytest

---

## 🏃 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables (Optional)
Copy `.env.example` to `.env` and add your keys:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
```
*(Note: If no API keys are provided, the system seamlessly runs in **Calibrated Offline Demo Mode**, guaranteeing a flawless pitch).*

### 3. Run Automated Tests
```bash
pytest tests/ -v
```

### 4. Launch Application
```bash
streamlit run app.py
```
