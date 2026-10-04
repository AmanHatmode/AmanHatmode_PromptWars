import streamlit as st
import json
from config import Config
from auth_service import AuthService
from db_service import DatabaseService
from engine import BlindSpotEngine
from schema import BlindSpotAnalysis

# Set Page Config
st.set_page_config(
    page_title="THE BLIND SPOT — AI Socratic Thinking Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cyberpunk / Modern Dark Glassmorphic Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Base */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #070B12 !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.12) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(244, 63, 94, 0.08) 0px, transparent 50%),
            radial-gradient(at 50% 50%, rgba(245, 158, 11, 0.04) 0px, transparent 60%) !important;
        color: #F1F5F9 !important;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }

    [data-testid="stSidebar"] {
        background-color: rgba(11, 15, 25, 0.85) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
        letter-spacing: -0.02em !important;
    }

    /* Hero Gradient Title */
    .hero-title {
        font-size: 2.75rem;
        font-weight: 900;
        background: linear-gradient(135deg, #60A5FA 0%, #A855F7 50%, #F43F5E 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
        letter-spacing: -0.03em;
        text-shadow: 0 0 40px rgba(96, 165, 250, 0.25);
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #94A3B8;
        font-weight: 400;
        margin-bottom: 24px;
    }

    /* Glowing Non-Prescriptive Badge */
    .constitution-badge {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(59, 130, 246, 0.4);
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.15), inset 0 0 15px rgba(59, 130, 246, 0.05);
        backdrop-filter: blur(16px);
        border-radius: 12px;
        padding: 16px 22px;
        margin-bottom: 26px;
        display: flex;
        align-items: center;
        gap: 14px;
        color: #E2E8F0;
    }
    .badge-icon {
        font-size: 1.6rem;
    }
    .badge-text b {
        color: #60A5FA;
    }

    /* Preset Buttons Styling */
    .preset-container {
        display: flex;
        gap: 10px;
        margin-bottom: 16px;
        flex-wrap: wrap;
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.65) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        padding: 20px !important;
        backdrop-filter: blur(16px) !important;
        margin-bottom: 16px !important;
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35) !important;
    }
    .glass-card:hover {
        border-color: rgba(96, 165, 250, 0.3) !important;
        box-shadow: 0 12px 35px rgba(59, 130, 246, 0.12) !important;
        transform: translateY(-2px) !important;
    }

    /* Tag Pills */
    .tag-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-right: 6px;
    }
    .tag-blue { background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.3); }
    .tag-amber { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .tag-rose { background: rgba(244, 63, 94, 0.15); color: #FB7185; border: 1px solid rgba(244, 63, 94, 0.3); }
    .tag-purple { background: rgba(168, 85, 247, 0.15); color: #C084FC; border: 1px solid rgba(168, 85, 247, 0.3); }

    /* Bento Box Accents */
    .bento-header {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .bento-blue { color: #60A5FA; }
    .bento-amber { color: #FBBF24; }
    .bento-rose { color: #FB7185; }
    .bento-purple { color: #C084FC; }

    /* Primary CTA Button Pulse */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB 0%, #4F46E5 100%) !important;
        border: 1px solid rgba(96, 165, 250, 0.5) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        padding: 14px 28px !important;
        border-radius: 10px !important;
        box-shadow: 0 0 25px rgba(37, 99, 235, 0.4) !important;
        transition: all 0.25s ease-in-out !important;
        letter-spacing: -0.01em !important;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 35px rgba(96, 165, 250, 0.7) !important;
        transform: translateY(-2px) !important;
        border-color: #93C5FD !important;
    }

    /* Text Area Styling */
    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
        font-size: 0.95rem !important;
        backdrop-filter: blur(12px) !important;
    }
    .stTextArea textarea:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.3) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px 8px 0 0;
        color: #94A3B8;
        padding: 8px 18px;
        font-weight: 600;
        font-size: 0.95rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border-color: rgba(59, 130, 246, 0.4) !important;
        color: #60A5FA !important;
        box-shadow: 0 -2px 10px rgba(59, 130, 246, 0.15) !important;
    }

    /* Code / Monospace */
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #38BDF8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Session States
if "auth_service" not in st.session_state:
    st.session_state.auth_service = AuthService()

if "db_service" not in st.session_state:
    st.session_state.db_service = DatabaseService(st.session_state.auth_service.supabase_client)

if "engine" not in st.session_state:
    st.session_state.engine = BlindSpotEngine()

if "current_user" not in st.session_state:
    # Start as unauthenticated so user can sign in with their verified account
    st.session_state.current_user = None

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Check for Supabase Auth redirect token in hash fragment via lightweight JS
import streamlit.components.v1 as components
components.html("""
<script>
    if (window.location.hash && window.location.hash.includes("access_token")) {
        const url = new URL(window.location.href);
        url.hash = "";
        url.searchParams.set("email_confirmed", "true");
        window.location.replace(url.toString());
    }
</script>
""", height=0)

def get_user_field(user_obj, field: str, default: str = "") -> str:
    if not user_obj:
        return default
    if isinstance(user_obj, dict):
        return str(user_obj.get(field, default))
    return str(getattr(user_obj, field, default))

# Check query params for confirmed status
is_email_confirmed = st.query_params.get("email_confirmed") == "true"
if is_email_confirmed:
    st.toast("✅ Email Confirmed Successfully! Please sign in below.", icon="🎉")

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
        <div style="background:linear-gradient(135deg, #3B82F6, #A855F7); width:36px; height:36px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:1.2rem;">🧠</div>
        <div>
            <div style="font-weight:800; font-size:1.05rem; color:#F8FAFC;">THE BLIND SPOT</div>
            <div style="font-size:0.75rem; color:#60A5FA; font-weight:600;">{Build with AI} • PromptWars</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("SVPCET x Google for Developers Challenge")
    st.divider()

    # User Authentication
    st.markdown("#### 🔐 Security & Identity")
    
    if is_email_confirmed:
        st.success("✅ **Email Confirmed!** Please sign in with your credentials below.")

    user = st.session_state.current_user

    if user:
        u_email = get_user_field(user, 'email', 'Verified User')
        u_role = get_user_field(user, 'role', 'Authenticated User')
        st.markdown(f"""
        <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(34,197,94,0.3); border-radius:8px; padding:10px 14px; margin-bottom:10px;">
            <div style="font-size:0.75rem; color:#4ADE80; font-weight:700;">AUTHENTICATED SESSION</div>
            <div style="font-weight:600; font-size:0.9rem; color:#F1F5F9;">{u_email}</div>
            <div style="font-size:0.75rem; color:#94A3B8;">{u_role}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Sign Out / Switch Session", use_container_width=True):
            st.session_state.auth_service.sign_out()
            st.session_state.current_user = None
            if "email_confirmed" in st.query_params:
                del st.query_params["email_confirmed"]
            st.rerun()
    else:
        auth_t1, auth_t2, auth_t3 = st.tabs(["Sign In", "Sign Up", "Judge Mode"])
        with auth_t1:
            in_email = st.text_input("Email", key="in_email")
            in_pwd = st.text_input("Password", type="password", key="in_pwd")
            if st.button("Authenticate with Supabase", use_container_width=True):
                res = st.session_state.auth_service.sign_in(in_email, in_pwd)
                if res["success"]:
                    st.session_state.current_user = res["user"]
                    if "email_confirmed" in st.query_params:
                        del st.query_params["email_confirmed"]
                    st.rerun()
                else:
                    st.error(res["message"])

        with auth_t2:
            up_email = st.text_input("Email", key="up_email")
            up_pwd = st.text_input("Password", type="password", key="up_pwd")
            if st.button("Create Account", use_container_width=True):
                res = st.session_state.auth_service.sign_up(up_email, up_pwd)
                if res["success"]:
                    st.success("🎉 Account created successfully! Please switch to the **Sign In** tab to log in.")
                    st.toast("Account created! Please sign in.", icon="✅")
                else:
                    st.error(res["message"])

        with auth_t3:
            st.info("Fast evaluation mode for Hackathon Judges.")
            if st.button("⚡ Enter as Judge / Guest", use_container_width=True):
                st.session_state.current_user = st.session_state.auth_service.get_guest_session()
                st.rerun()

    st.divider()

    # System Status
    st.markdown("#### ⚡ System Health")
    gemini_badge = "🟢 Google Gemini 1.5 Pro (Active)" if Config.is_gemini_configured() else "🟡 Calibrated Offline Mode"
    supabase_badge = "🟢 Supabase Postgres (Connected)" if st.session_state.auth_service.is_cloud_enabled else "🟡 Local Session Storage"
    st.markdown(f"""
    <div style="font-size:0.8rem; line-height:1.6; color:#94A3B8;">
        <div><b>Model Tier:</b> <code>{Config.GEMINI_PRIMARY_MODEL}</code></div>
        <div><b>API Gateway:</b> {gemini_badge}</div>
        <div><b>Cloud DB:</b> {supabase_badge}</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Decision History
    st.markdown("#### 📜 Decision Logs")
    if user:
        history = st.session_state.db_service.get_history(get_user_field(user, "id", "guest"))
        if history:
            for idx, item in enumerate(history[:5]):
                txt = item.get("decision_text", "")[:32] + "..."
                if st.button(f"#{idx+1}: {txt}", key=f"hist_{idx}", use_container_width=True):
                    st.session_state.analysis_result = item["analysis"]
                    st.session_state.input_text = item.get("decision_text", "")
                    st.rerun()
        else:
            st.caption("No decision logs recorded in this session.")

# ----------------- MAIN VIEW -----------------

# Hero Header always visible
st.markdown('<div class="hero-title">THE BLIND SPOT</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">AI-Powered Socratic Thinking Companion for High-Stakes Decisions</div>', unsafe_allow_html=True)

# ===== AUTH GATE: Block everything unless signed in =====
if not st.session_state.current_user:
    st.markdown("""
    <div style="
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(59, 130, 246, 0.4);
        border-radius: 16px;
        padding: 48px 40px;
        text-align: center;
        margin: 40px auto;
        max-width: 520px;
        backdrop-filter: blur(16px);
        box-shadow: 0 0 40px rgba(59, 130, 246, 0.1);
    ">
        <div style="font-size: 3rem; margin-bottom: 16px;">🔐</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: #F8FAFC; margin-bottom: 10px;">
            Access Required
        </div>
        <div style="font-size: 1rem; color: #94A3B8; margin-bottom: 24px; line-height: 1.6;">
            Please <b style="color:#60A5FA;">Sign Up</b> for a new account or <b style="color:#60A5FA;">Sign In</b> to your existing account using the sidebar on the left to access <b style="color:#F8FAFC;">THE BLIND SPOT</b>.
        </div>
        <div style="font-size: 0.85rem; color:#64748B;">
            ← Open the <b>Security & Identity</b> panel in the sidebar
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ===== PAST AUTH GATE: Everything below only renders for logged-in users =====

# Non-Prescriptive Constitution Badge
st.markdown("""
<div class="constitution-badge">
    <div class="badge-icon">🛡️</div>
    <div class="badge-text">
        <b>NON-PRESCRIPTIVE CONSTITUTION:</b> The Blind Spot never decides for you. It illuminates unexamined premises, hidden risks, and blind spots so you can decide with 100% clarity and agency.
    </div>
</div>
""", unsafe_allow_html=True)

# Preset Scenarios Selector
st.markdown("##### ⚡ Quick Preset Scenarios (Click to Load):")
col_p1, col_p2, col_p3, col_p4 = st.columns(4)

with col_p1:
    if st.button("💼 6-Month Internship Offer\n*(Official Challenge)*", use_container_width=True):
        st.session_state.input_text = (
            "I received an offer for a 6-month internship at a software consultancy. "
            "The stipend is ₹35,000/month, the office is just 15 minutes from my house, and working hours are 9:30 AM to 6:30 PM. "
            "The role is Junior Developer. I'm mainly considering it because the stipend is great, it's super close to home with zero commute fatigue, "
            "and it gives me corporate industry experience on my resume. My college has a strict 75% attendance rule and semester exams in 4 months, "
            "but I think I can manage attendance with medical certificates, study on weekends, and borrow notes from friends."
        )
        st.rerun()

with col_p2:
    if st.button("🚀 Drop Out for Startup\n*(Prototype Traction)*", use_container_width=True):
        st.session_state.input_text = (
            "I built an AI social media scheduling SaaS prototype over a hackathon weekend and all my college friends love it. "
            "I am considering dropping out of college to pursue this startup full-time. I have ₹40,000 in savings and my parents said I can stay home for 6 months. "
            "I believe moving fast is better than finishing my degree since AI is evolving so rapidly."
        )
        st.rerun()

with col_p3:
    if st.button("📈 Pivot to Microservices\n*(Architecture Refactor)*", use_container_width=True):
        st.session_state.input_text = (
            "Our web app has 15,000 active users running on a Ruby on Rails monolith with a Postgres database. "
            "Our 4-person engineering team wants to pause new feature work for 3 months to decompose the monolith into 8 Go microservices on Kubernetes. "
            "We believe this will give us infinite horizontal scalability and allow independent deployment velocity."
        )
        st.rerun()

with col_p4:
    if st.button("🏠 Relocate for Work\n*(Metro City Move)*", use_container_width=True):
        st.session_state.input_text = (
            "I got a job offer in Bengaluru offering a 30% higher salary than my current job in Indore. "
            "I'm planning to accept and move next month because the salary is higher and it's India's tech hub. "
            "I haven't researched rental deposits or commute times yet, but everyone says Bangalore is where tech careers grow fastest."
        )
        st.rerun()

# Decision Input Canvas
char_count = len(st.session_state.input_text)
user_input = st.text_area(
    "Describe your proposed decision, underlying assumptions, and motivations:",
    value=st.session_state.input_text,
    height=150,
    placeholder="Describe your decision in detail (e.g. stipend, hours, dependencies, college schedule, trade-offs)..."
)

col_meta, col_btn = st.columns([2, 1])
with col_meta:
    st.caption(f"Character Count: **{char_count}** / 4000 • Security Guardrails: Active 🛡️")
with col_btn:
    col_clear, col_run = st.columns([1, 2])
    with col_clear:
        if st.button("Clear", use_container_width=True):
            st.session_state.input_text = ""
            st.session_state.analysis_result = None
            st.rerun()
    with col_run:
        analyze_clicked = st.button("🔍 Expose Blind Spots", type="primary", use_container_width=True)

if analyze_clicked:
    if not user_input.strip():
        st.warning("Please enter a decision scenario before running the evaluation.")
    else:
        with st.spinner("Exposing unstated assumptions, cognitive biases, and simulating pre-mortem..."):
            result = st.session_state.engine.evaluate_decision(user_input)
            if not result["success"]:
                st.error(f"🛡️ Guardrail Alert: {result['error']}")
            else:
                data = result["data"]
                st.session_state.analysis_result = data
                st.session_state.input_text = user_input
                
                # Persist to database
                if st.session_state.current_user:
                    user_id = get_user_field(st.session_state.current_user, "id", "guest")
                    st.session_state.db_service.save_evaluation(user_id, user_input, data)
                st.rerun()

# ----------------- DYNAMIC BENTO GRID DASHBOARD -----------------
if st.session_state.analysis_result:
    res = st.session_state.analysis_result
    st.divider()

    # Top Audit Metrics & Epistemic Rigor Breakdown
    score = res.get("thoughtfulness_score", 40)
    unexamined = 100 - score
    epistemic = res.get("epistemic_rigor", {})
    framework_name = epistemic.get("decision_framework_applied", "Kahneman-Klein Dual Cognitive Audit")
    fragility = epistemic.get("assumption_fragility_index", 80)
    exposure_level = epistemic.get("risk_exposure_level", "High Systemic Risk")

    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;" role="region" aria-label="Cognitive Analysis Header">
        <h3 style="margin:0; color:#F8FAFC;">🧠 Cognitive Analysis & Epistemic Audit</h3>
        <span class="tag-pill tag-blue">Decision Science Framework: {framework}</span>
    </div>
    """.format(framework=framework_name), unsafe_allow_html=True)

    col_m1, col_m2, col_m3, col_m4 = st.columns([1, 1, 1, 1])
    with col_m1:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;" role="status" aria-label="Reasoning Clarity Score">
            <div style="font-size:0.8rem; color:#94A3B8; text-transform:uppercase; font-weight:700;">Reasoning Clarity</div>
            <div style="font-size:2.4rem; font-weight:900; color:#60A5FA; margin:6px 0;">{score}%</div>
            <div style="font-size:0.8rem; color:#F87171;">⚠️ {unexamined}% Unexamined Blindspots</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        biases_count = len(res.get("cognitive_biases", []))
        risks_count = len(res.get("overlooked_risks", []))
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;" role="status" aria-label="Biases Tagged">
            <div style="font-size:0.8rem; color:#94A3B8; text-transform:uppercase; font-weight:700;">Cognitive Biases</div>
            <div style="font-size:2.4rem; font-weight:900; color:#FBBF24; margin:6px 0;">{biases_count}</div>
            <div style="font-size:0.8rem; color:#FBBF24;">System 1 Distortions</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m3:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;" role="status" aria-label="Assumption Fragility">
            <div style="font-size:0.8rem; color:#94A3B8; text-transform:uppercase; font-weight:700;">Premise Fragility</div>
            <div style="font-size:2.4rem; font-weight:900; color:#F43F5E; margin:6px 0;">{fragility}%</div>
            <div style="font-size:0.8rem; color:#F87171;">{exposure_level}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m4:
        factors = "".join([f"<li style='margin-bottom:4px;'>{f}</li>" for f in res.get("salient_factors", [])])
        st.markdown(f"""
        <div class="glass-card" style="padding:16px 20px;" role="region" aria-label="Salient Anchor">
            <div style="font-size:0.8rem; color:#94A3B8; text-transform:uppercase; font-weight:700; margin-bottom:6px;">
                🎯 Salience Anchor (Immediate Perks):
            </div>
            <ul style="margin:0; padding-left:18px; color:#E2E8F0; font-size:0.85rem;">
                {factors}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # 4-Part Bento Grid / Multi-Tab Deep Dive
    tab_assumptions, tab_risks, tab_perspectives, tab_socratic = st.tabs([
        "🔍 Unstated Assumptions & Falsification",
        "⚠️ Overlooked Risks & Pre-Mortem",
        "💡 External Stakeholder Angles",
        "❓ Interactive Socratic Inquiry"
    ])

    # Bento 1: Unstated Assumptions
    with tab_assumptions:
        st.markdown("""
        <div class="bento-header bento-blue" role="heading" aria-level="4">
            <span>🔍 Unstated Assumptions & 48-Hour Falsification Protocols</span>
        </div>
        <p style="color:#CBD5E1; font-size:0.9rem;">Underlying premises treated as facts, with actionable 48-hour empirical tests to verify them before committing:</p>
        """, unsafe_allow_html=True)

        for asm in res.get("unstated_assumptions", []):
            conf = asm.get("confidence_level", "Unverified Guess")
            conf_color = "tag-amber" if "Anecdote" in conf else "tag-rose"
            falsify = asm.get("falsification_protocol", "Verify this premise with direct objective data before taking action.")
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #3B82F6 !important; margin-bottom:14px;" role="article" aria-label="Unstated Assumption Card">
                <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                    <span class="tag-pill tag-blue">{asm.get('category')}</span>
                    <span class="tag-pill {conf_color}">Confidence: {conf}</span>
                </div>
                <div style="font-size:1.05rem; font-weight:700; color:#F8FAFC; margin-bottom:6px;">
                    "{asm.get('premise')}"
                </div>
                <div style="font-size:0.9rem; color:#FB7185; margin-bottom:6px;">
                    <b>Vulnerability:</b> {asm.get('vulnerability')}
                </div>
                <div style="font-size:0.88rem; color:#60A5FA; background:rgba(30,58,138,0.25); border:1px solid rgba(59,130,246,0.3); border-radius:6px; padding:8px 12px;">
                    🧪 <b>48-Hour Falsification Protocol:</b> {falsify}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Bento 2: Overlooked Risks & Pre-Mortem Simulator
    with tab_risks:
        st.markdown("""
        <div class="bento-header bento-rose" role="heading" aria-level="4">
            <span>⚠️ Overlooked Risks & Stress-Test Inquiries</span>
        </div>
        """, unsafe_allow_html=True)

        # Categorized Risks
        r_col1, r_col2 = st.columns(2)
        risks = res.get("overlooked_risks", [])
        for i, risk in enumerate(risks):
            col = r_col1 if i % 2 == 0 else r_col2
            sev = risk.get("severity", "High")
            sev_badge = "tag-rose" if sev == "Critical" else "tag-amber"
            stress_q = risk.get("stress_test_question", "How would you handle this scenario if it occurs?")
            with col:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #F43F5E !important; min-height:180px; margin-bottom:14px;" role="article" aria-label="Overlooked Risk Card">
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                        <span class="tag-pill tag-purple">{risk.get('risk_category', 'Operational')}</span>
                        <span class="tag-pill {sev_badge}">{sev} Impact</span>
                    </div>
                    <div style="font-size:1rem; font-weight:700; color:#F8FAFC; margin-bottom:6px;">
                        {risk.get('risk_title')}
                    </div>
                    <div style="font-size:0.85rem; color:#CBD5E1; line-height:1.5; margin-bottom:8px;">
                        {risk.get('failure_scenario')}
                    </div>
                    <div style="font-size:0.82rem; color:#FDE68A; font-style:italic;">
                        🛡️ <b>Stress-Test Inquiry:</b> "{stress_q}"
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Interactive Pre-Mortem Simulator
        st.markdown("---")
        st.markdown("""
        <div class="bento-header bento-amber" role="heading" aria-level="4">
            <span>⏳ Gary Klein Pre-Mortem Failure Simulator</span>
        </div>
        <p style="color:#CBD5E1; font-size:0.88rem;">Select a timeline to simulate how this decision could cascade into regret if unaddressed:</p>
        """, unsafe_allow_html=True)

        horizon = st.select_slider(
            "Pre-Mortem Time Horizon:",
            options=["1 Month in the Future", "6 Months in the Future", "1 Year in the Future"],
            value="6 Months in the Future"
        )

        timeline = res.get("pre_mortem_timeline", {})
        if horizon == "1 Month in the Future":
            scenario_text = timeline.get("one_month", "Initial operational friction surfaces.")
            tag_text = "Phase 1: Friction & Fatigue"
        elif horizon == "6 Months in the Future":
            scenario_text = timeline.get("six_months", "Compounding structural failure occurs.")
            tag_text = "Phase 2: Compounding Regret"
        else:
            scenario_text = timeline.get("one_year", "Long-term career consequence materializes.")
            tag_text = "Phase 3: Structural Lock-in"

        st.markdown(f"""
        <div class="glass-card" style="border: 1px solid rgba(245, 158, 11, 0.4) !important; background:rgba(245, 158, 11, 0.05) !important;" role="region" aria-label="Pre-Mortem Simulator Result">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span class="tag-pill tag-amber">⏱️ {horizon}</span>
                <span class="tag-pill tag-rose">{tag_text}</span>
            </div>
            <div style="font-size:0.95rem; color:#FDE68A; line-height:1.6;">
                {scenario_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Bento 3: Alternative Perspectives
    with tab_perspectives:
        st.markdown("""
        <div class="bento-header bento-purple" role="heading" aria-level="4">
            <span>💡 External Stakeholder Angles (What Others Notice)</span>
        </div>
        <p style="color:#CBD5E1; font-size:0.9rem;">How skeptical external parties evaluate your proposed path:</p>
        """, unsafe_allow_html=True)

        for persp in res.get("alternative_perspectives", []):
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #A855F7 !important; margin-bottom:12px;" role="article" aria-label="Stakeholder Perspective Card">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                    <span class="tag-pill tag-purple">👤 {persp.get('stakeholder')}</span>
                </div>
                <div style="font-size:0.95rem; color:#E2E8F0; margin-bottom:8px; line-height:1.5;">
                    <b>Contrarian View:</b> {persp.get('contrarian_view')}
                </div>
                <div style="font-size:0.9rem; color:#C084FC; font-style:italic;">
                    ❓ <b>What they would ask:</b> "{persp.get('key_question_they_would_ask')}"
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Bento 4: Interactive Socratic Inquiry Loop
    with tab_socratic:
        st.markdown("""
        <div class="bento-header bento-blue" role="heading" aria-level="4">
            <span>❓ Interactive Socratic Inquiry Loop</span>
        </div>
        <p style="color:#CBD5E1; font-size:0.9rem;">Submit your defense for each probing question. The AI companion stress-tests your reasoning without ever deciding for you:</p>
        """, unsafe_allow_html=True)

        for idx, q in enumerate(res.get("socratic_questions", [])):
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #60A5FA !important; margin-bottom:12px;" role="region" aria-label="Socratic Question">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span class="tag-pill tag-blue">Dimension: {q.get('domain')}</span>
                    <span style="font-size:0.8rem; color:#94A3B8;">Question {idx+1} of 3</span>
                </div>
                <div style="font-size:1.05rem; font-weight:700; color:#F8FAFC; margin-bottom:6px;">
                    {q.get('question')}
                </div>
                <div style="font-size:0.85rem; color:#CBD5E1;">
                    💡 <b>Reflection Target:</b> {q.get('reflection_prompt')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            ans_key = f"defense_{idx}"
            user_defense = st.text_input(f"Your defense / verified evidence for Question {idx+1}:", key=ans_key, placeholder="e.g. I spoke with the HOD and obtained an official written NOC...")
            
            if st.button(f"⚡ Stress-Test Defense #{idx+1}", key=f"btn_test_{idx}"):
                if user_defense.strip():
                    with st.spinner("Analyzing your defense against hidden assumptions..."):
                        fb = st.session_state.engine.evaluate_followup(
                            decision_context=st.session_state.input_text,
                            question_asked=q.get("question"),
                            user_answer=user_defense
                        )
                        st.markdown(f"""
                        <div style="background:rgba(30,58,138,0.3); border:1px solid rgba(96,165,250,0.4); border-radius:8px; padding:14px; margin-top:8px; color:#BFDBFE; font-size:0.9rem;" role="alert" aria-live="polite">
                            <b>🧠 Companion Reflection:</b><br>{fb.get('reflection')}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Please type your reasoning before stress-testing.")

    # ----------------- EXPORT & SHARE TOOLBAR -----------------
    st.divider()
    st.markdown("##### 📤 Export & Share Analysis")
    
    # Generate Markdown export payload
    md_content = f"""# THE BLIND SPOT — Decision Audit Report
**Decision Summary:** {res.get('decision_summary')}
**Reasoning Clarity Score:** {res.get('thoughtfulness_score')}%
**Framework:** {framework_name}
**Non-Prescriptive Guarantee:** {res.get('non_prescriptive_guarantee')}

---
## 🎯 Salient Anchors
{chr(10).join(['- ' + s for s in res.get('salient_factors', [])])}

## 🔍 Unstated Assumptions & Falsification Protocols
{chr(10).join([f"- **[{a.get('category')}]** {a.get('premise')}\n  - *Vulnerability:* {a.get('vulnerability')}\n  - *48-Hr Falsification Protocol:* {a.get('falsification_protocol', 'Verify premise')}" for a in res.get('unstated_assumptions', [])])}

## ⚠️ Overlooked Risks & Stress Tests
{chr(10).join([f"- **[{r.get('risk_category')} / {r.get('severity')}]** {r.get('risk_title')}: {r.get('failure_scenario')}\n  - *Stress-Test Inquiry:* \"{r.get('stress_test_question', 'Inquire exposure')}\"" for r in res.get('overlooked_risks', [])])}

## 💡 External Stakeholder Angles
{chr(10).join([f"- **{p.get('stakeholder')}:** {p.get('contrarian_view')} *(Key Question: \"{p.get('key_question_they_would_ask')}\")*" for p in res.get('alternative_perspectives', [])])}

## ⏳ Pre-Mortem Failure Narrative
- **1 Month:** {res.get('pre_mortem_timeline', {}).get('one_month')}
- **6 Months:** {res.get('pre_mortem_timeline', {}).get('six_months')}
- **1 Year:** {res.get('pre_mortem_timeline', {}).get('one_year')}

## ❓ Socratic Reflection Questions
{chr(10).join([f"{i+1}. **[{q.get('domain')}]** {q.get('question')} *(Guidance: {q.get('reflection_prompt')})*" for i, q in enumerate(res.get('socratic_questions', []))])}
"""

    exp_col1, exp_col2 = st.columns([1, 1])
    with exp_col1:
        st.download_button(
            label="📥 Download Audit Report (.md)",
            data=md_content,
            file_name="the_blind_spot_analysis.md",
            mime="text/markdown",
            use_container_width=True
        )
    with exp_col2:
        with st.expander("📋 View Shareable Text Snapshot"):
            st.text_area("Copy Snapshot:", value=md_content, height=180)

# Footer & Accessibility Declaration
st.markdown("---")
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; font-size:0.78rem; color:#64748B;" role="contentinfo">
    <div><b>THE BLIND SPOT</b> • Built with AI for SVPCET x Google for Developers Challenge</div>
    <div>♿ WCAG 2.1 AA Compliant • Keyboard & Screen Reader Accessible</div>
</div>
""", unsafe_allow_html=True)

