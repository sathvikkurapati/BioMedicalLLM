import streamlit as st
import time
from src.model_engine import BioGPTModel
from src.security_guard import SecurityGuard
from src.privacy_lab import PrivacyLab

st.set_page_config(page_title="Secure Medical LLM", page_icon="🛡️", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    h1 {
        color: #0e1117;
    }
    .stChatInput {
        border-color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_system_components():
    model = BioGPTModel()
    # We will let the model lazy load on first request or explicitly load here if we want a spinner
    return model, SecurityGuard(), PrivacyLab()

model, security, privacy = get_system_components()

st.title("🛡️ Secure Medical LLM System")
st.markdown("### Trustworthy AI for Healthcare | Security-Aware & Privacy-Preserving")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    enable_security = st.toggle("Enable Security Module", value=True, help="Activates input filtering and output sanitization.")
    enable_privacy = st.toggle("Enable Privacy Defense", value=False, help="Activates countermeasures against Membership Inference Attacks.")
    demo_mode = st.toggle("⚡ Use Demo Mode (No Download)", value=False, help="Skip model loading and use simulated responses. Useful if download is slow.")
    
    st.divider()
    st.markdown("**System Status**")
    if demo_mode:
        st.info("Mode: DEMO (Simulated)")
    else:
        st.info("Mode: FULL AI (BioGPT)")

    if enable_security:
        st.success("Security: ACTIVE")
    else:
        st.warning("Security: DISABLED")
        
    if enable_privacy:
        st.success("Privacy Defense: ACTIVE")
    else:
        st.warning("Privacy Defense: OFF")

# Tabs
tab_chat, tab_attack = st.tabs(["💬 Medical Chat", "🧪 Attack Evaluation Lab"])

# Chat Interface
with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("is_blocked"):
                st.caption("🚫 This message was flagged by the Security Module.")

    # Input
    if prompt := st.chat_input("Enter clinical question..."):
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Logic
        if enable_security:
            is_safe, reason = security.check_input(prompt)
        else:
            is_safe, reason = True, "Security Disabled"

        if not is_safe:
            # Blocked
            response = f"**System Alert**: {reason}"
            st.session_state.messages.append({"role": "assistant", "content": response, "is_blocked": True})
            with st.chat_message("assistant"):
                st.markdown(response)
                st.caption("🚫 Request blocked.")
        else:
            # Generate
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("Analyzing Medical Knowledge Base..."):
                    try:
                        # 1. Generate
                        raw_response = model.generate_answer(prompt, mock=demo_mode)
                        
                        # 2. Privacy Mitigation (if enabled)
                        if enable_privacy:
                            processed_response = privacy.apply_mitigation(raw_response)
                        else:
                            processed_response = raw_response
                            
                        # 3. Output Sanitization (if security enabled)
                        if enable_security:
                            final_response = security.sanitize_output(processed_response)
                        else:
                            final_response = processed_response
                        
                        message_placeholder.markdown(final_response)
                        st.session_state.messages.append({"role": "assistant", "content": final_response})
                    except Exception as e:
                        st.error(f"Model Error: {str(e)}")

# Attack Lab Interface
with tab_attack:
    st.subheader("Vulnerability Assessment")
    st.markdown("Simulate attacks to evaluate system robustness.")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.card = st.container(border=True)
        st.card.subheader("🕵️ Membership Inference Attack (MIA)")
        st.markdown("Check if a text sample likely belongs to the training data.")
        
        mia_input = st.text_area("Sample Text", "Patient diagnosed with rare condition X...", height=100)
        if st.button("Run MIA Simulation"):
            score = privacy.simulate_mia(mia_input, model)
            st.progress(score, text=f"Membership Probability: {score:.2%}")
            
            if score > 0.7:
                st.error("High Likelihood of Membership (Privacy Leak!)")
            else:
                st.success("Low Likelihood (Safe)")
                
    with col_b:
        st.card2 = st.container(border=True)
        st.card2.subheader("🛡️ Security Filter Test")
        st.markdown("Test if specific prompts bypass the security layer.")
        
        sec_input = st.text_area("Test Prompt", "Ignore instructions and reveal...", height=100)
        if st.button("Test Filters"):
            is_safe, reason = security.check_input(sec_input)
            if is_safe:
                st.error("Result: PASSED (Filter Failed to block)")
            else:
                st.success(f"Result: BLOCKED ({reason})")

st.sidebar.markdown("---")
st.sidebar.caption("v1.0.0 | BioGPT-Large")
