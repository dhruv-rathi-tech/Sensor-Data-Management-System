import streamlit as st
import pandas as pd
import oracledb
import time

st.set_page_config(page_title="DBMS PROJECT", layout="wide")

if "sql_query" not in st.session_state:
    st.session_state["sql_query"] = "SELECT * FROM processed_data"
if "last_df" not in st.session_state:
    st.session_state["last_df"] = None

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Anton&display=swap');

#splash-screen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #000000, #434343);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    color: #00c4ff;
    font-family: 'Anton', sans-serif;
    font-size: 70px;
    text-align: center;
    text-transform: uppercase;
    opacity: 1;
    text-shadow: 2px 2px 6px #ffcc00; /* Mild yellow shadow */
    animation: liftUp 1s ease-out forwards, fadeOut 0.5s ease forwards 1.5s;
}

/* Lift effect */
@keyframes liftUp {
    0% { transform: translateY(40px); opacity: 0; }
    100% { transform: translateY(0); opacity: 1; }
}

/* Fade out */
@keyframes fadeOut {
    0% { opacity: 1; }
    100% { opacity: 0; display: none; }
}
</style>

<div id="splash-screen">DATA VISUALISATION</div>

<script>
setTimeout(function() {
    var splash = document.getElementById("splash-screen");
    if (splash) { splash.style.display = "none"; }
}, 4000);
</script>
""", unsafe_allow_html=True)

time.sleep(1.5) 

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap');

.stApp { background: linear-gradient(135deg, #434343, #000000); color: white; }

/* Header Zoom-In */
.header-box {
    background: linear-gradient(90deg, #1f1c2c, #928dab);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    animation: zoomIn 1.5s ease-out forwards;
}
@keyframes zoomIn {
    0% { transform: scale(0); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}
.project-title { font-family: 'Orbitron', sans-serif; font-size: 55px; color: #00c4ff; text-shadow: 3px 3px 8px #000000; }
.project-sub { font-size: 18px; margin: 4px 0; }
.label-text { color: white; font-weight: bold; }
.name-text { color: #ffcc00; font-weight: normal; }
.id-text { color: white; font-weight: normal; }
.faculty-text { color: #ffcc00; font-weight: normal; }

/* Buttons */
.stButton button {
    background-color: #2d2d3a;
    color: white;
    padding: 6px 16px;
    border-radius: 6px;
    border: 1px solid #444;
}
.stButton button:hover {
    background-color: #3d3d4a;
    color: #ffcc00;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <div class="project-title">DBMS PROJECT</div>
    <p class="project-sub"><span class="label-text">Done by:</span></p>
    <p class="project-sub"><span class="name-text">Aman Gupta</span> - <span class="id-text">23BLC1161</span></p>
    <p class="project-sub"><span class="name-text">Dhruv Rathi</span> - <span class="id-text">23BLC1164</span></p>
    <p class="project-sub"><span class="label-text">Submitted to -</span> <span class="faculty-text">Dr. Sobitha Ahila</span></p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR QUERIES ---
QUERY_SHORTCUTS = {
    "First 10 Rows": """SELECT * FROM (SELECT * FROM processed_data ORDER BY Date_Col DESC) WHERE ROWNUM <= 10""",
    "Total No. of Records": "SELECT COUNT(*) AS total_records FROM processed_data",
    "Unique No. of Sensors": "SELECT COUNT(DISTINCT Sensor_ID) AS unique_sensors FROM processed_data",
    "Average Temperature": "SELECT AVG(Temp) AS avg_temp FROM processed_data",
    "Average Humidity": "SELECT AVG(Humidity) AS avg_humidity FROM processed_data",
    "Last Updated Timestamp": "SELECT MAX(Date_Col || ' --- ' || Time_Col) AS last_update FROM processed_data",
    "Top 10 Sensors by Usage": """SELECT * FROM (SELECT Sensor_ID, COUNT(*) AS usage_count FROM processed_data GROUP BY Sensor_ID ORDER BY COUNT(*) DESC) WHERE ROWNUM <= 10""",
    "Top 10 Sensors by Latest Activity": """SELECT * FROM (SELECT Sensor_ID, MAX(Date_Col || ' --- ' || Time_Col) AS last_seen FROM processed_data GROUP BY Sensor_ID ORDER BY MAX(Date_Col || ' ' || Time_Col) DESC) WHERE ROWNUM <= 10""",
}
st.sidebar.header("📌 Query Shortcuts")
for label, query in QUERY_SHORTCUTS.items():
    if st.sidebar.button(label):
        st.session_state["sql_query"] = query

st.markdown('<div class="split-container">', unsafe_allow_html=True)

# Left side: SQL box
st.markdown('<div class="split-left">', unsafe_allow_html=True)
st.markdown("## 📊 Smart Home Sensors Data")
sql_query = st.text_area("💻 Enter Your SQL Query:", value=st.session_state["sql_query"], height=150, key="sqlQueryBox")
st.markdown('</div>', unsafe_allow_html=True)

# Right side: buttons
st.markdown('<div class="split-right">', unsafe_allow_html=True)
col1, col2 = st.columns([1,1])
with col1:
    run_query = st.button("▶ Run Query")
with col2:
    st.markdown('<div style="text-align:right;">', unsafe_allow_html=True)
    export_csv = st.button("📥 Export CSV")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)  


if run_query:
    try:
        oracledb.init_oracle_client(lib_dir=r"C:\\oraclexe\\instantclient-basic-windows.x64-23.9.0.25.07\\instantclient_23_9")
        conn = oracledb.connect(user="system", password="your_password_here", dsn="localhost/XE")
        df = pd.read_sql(sql_query, conn)
        st.session_state["last_df"] = df
        conn.close()
        st.success("✅ Query executed successfully!")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error: {e}")

if export_csv:
    if st.session_state["last_df"] is not None and not st.session_state["last_df"].empty:
        csv = st.session_state["last_df"].to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", data=csv, file_name="query_results.csv", mime="text/csv")
    else:
        st.warning("⚠️ No query results to export yet.")
