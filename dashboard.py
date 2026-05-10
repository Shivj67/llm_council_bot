import streamlit as st
import pandas as pd
import plotly.express as px
from app.database import get_session, AuditLog, Message, User
import time

st.set_page_config(page_title="Council Admin Dashboard", layout="wide")

st.title("🏛️ Council V2 Admin Dashboard")
st.markdown("---")

# Sidebar Stats
session = get_session()
total_users = session.query(User).count()
total_messages = session.query(Message).count()
total_audit_steps = session.query(AuditLog).count()

st.sidebar.metric("Total Users", total_users)
st.sidebar.metric("Total Messages", total_messages)
st.sidebar.metric("Audit Steps", total_audit_steps)

# --- LIVE AUDIT LOGS ---
st.subheader("🕵️ Live Council Deliberations")
refresh = st.button("Refresh Logs")

logs = session.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(50).all()
if logs:
    df_logs = pd.DataFrame([{
        "Time": l.timestamp.strftime("%H:%M:%S"),
        "User ID": l.user_id,
        "Agent": l.agent_name,
        "Query": l.query[:50] + "...",
        "Output": l.agent_output[:100] + "..."
    } for l in logs])
    st.dataframe(df_logs, use_container_width=True)
else:
    st.info("No audit logs yet. Start chatting with the bot!")

# --- USAGE CHART ---
st.markdown("---")
st.subheader("📈 Agent Activity Distribution")
if logs:
    agent_counts = df_logs['Agent'].value_counts().reset_index()
    agent_counts.columns = ['Agent', 'Requests']
    fig = px.pie(agent_counts, values='Requests', names='Agent', hole=0.4, 
                 color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig, use_container_width=True)

# --- USER EXPLORER ---
st.markdown("---")
st.subheader("👥 User Explorer")
users = session.query(User).all()
if users:
    df_users = pd.DataFrame([{
        "ID": u.id,
        "Mode": u.mode,
        "Depth": u.council_depth,
        "Persona": u.persona
    } for u in users])
    st.table(df_users)

session.close()
