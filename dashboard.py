import sqlite3
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import streamlit as st



DB_PATH = "data/sessions.db"

if not os.path.exists(DB_PATH):
    st.error("No session database found.")
else:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT 
            message, 
            start_time, 
            end_time, 
            duration,
            summary
        FROM sessions
        WHERE end_time IS NOT NULL
        ORDER BY start_time DESC
    """, conn)
    conn.close()

    df['start'] = pd.to_datetime(df['start_time'], unit='s')
    df['end'] = pd.to_datetime(df['end_time'], unit='s')
    df['duration_hours'] = df['duration'] / 3600

    st.title("📊 Timecraft Dashboard")

    st.subheader("🧠 Feature Log")
    st.dataframe(df[['start', 'message', 'duration_hours', 'summary']])

    st.subheader("⏱️ Time per Feature (hrs)")
    fig = px.bar(df, x='start', y='duration_hours', color='message', title='Duration per Feature')
    st.plotly_chart(fig)

    st.subheader("📈 Speed Trend (hrs per session)")
    fig2 = px.line(df.sort_values('start'), x='start', y='duration_hours', markers=True, title='Velocity Over Time')
    st.plotly_chart(fig2)
