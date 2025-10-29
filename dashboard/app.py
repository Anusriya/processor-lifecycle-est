import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
from pymongo import MongoClient
import os
import json

st.set_page_config(
    page_title="Processor Lifecycle Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
<style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    .stMetric {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    h1 {
        background: linear-gradient(135deg, #3b82f6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.25rem !important;
        font-weight: bold;
    }
    .uploadedFile {
        border: 2px dashed #3b82f6;
        border-radius: 10px;
        padding: 20px;
    }
    .js-plotly-plot .plotly {
        background: transparent !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


MODELS_LOADED = False
kmeans = None
scaler = None
label_map = None
models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "models"))

try:
    kmeans_path = os.path.join(models_dir, "kmeans_model.joblib")
    scaler_path = os.path.join(models_dir, "scaler.joblib")
    label_map_path = os.path.join(models_dir, "label_mapping.joblib")

    if os.path.exists(kmeans_path) and os.path.exists(scaler_path) and os.path.exists(label_map_path):
        kmeans = joblib.load(kmeans_path)
        scaler = joblib.load(scaler_path)
        label_map = joblib.load(label_map_path)
        MODELS_LOADED = True
except Exception as e:
    MODELS_LOADED = False

USE_MONGO = True
try:
    MONGO_URI = os.getenv("MONGODB_URI", "")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    db = client["recore_db"]
    collection = db["classified_results"]
    client.server_info()
except Exception:
    USE_MONGO = False
    collection = None



st.sidebar.title(" Navigation")
st.sidebar.markdown("Use the sections below to jump to parts of the dashboard:")

sections = {
    "Health Summary": "#health-summary",
    "Charts & Insights": "#charts",
    "AI Insights": "#ai-insights",
    "Maintenance & Recycling": "#maintenance",
    "GPU Comparison": "#comparison"
}

for label, anchor in sections.items():
    st.sidebar.markdown(f"[{label}]({anchor})")

st.title(" Processor Lifecycle & Health Dashboard")
st.markdown("---")

df = None

if USE_MONGO:
    batches = collection.distinct("batch_id")
    if len(batches) > 0:
        latest_batch = sorted(batches)[-1]
        records = list(collection.find({"batch_id": latest_batch}, {"_id": 0}))
        df = pd.DataFrame(records)

if USE_MONGO and collection is not None:
    try:
        data = list(collection.find({}, {"_id": 0}))
        if len(data) > 0:
            df = pd.DataFrame(data)
            st.success("✅ Data loaded from MongoDB Atlas!")
        else:
            st.warning("⚠️ No data found. Upload a CSV from the React app first.")
            st.stop()
    except Exception as e:
        st.error(f"❌ MongoDB query failed: {e}")
        st.stop()
else:
    st.info("⏳ Waiting for data from the React application...")
    st.stop()


if df is None:
    st.warning("No lifecycle data is available yet.")
    st.stop()

expected_cols = ["overclock_proxy", "usage_hours", "avg_power_watts", "peak_power_watts",
                 "avg_sm_pct", "avg_mem_pct", "thermal_score"]
for c in expected_cols:
    if c not in df.columns:
        df[c] = 0

if "GPU_ID" not in df.columns:
    df["GPU_ID"] = df.index + 1

if "health_class" not in df.columns and "Predicted_Class" in df.columns:
    df["health_class"] = df["Predicted_Class"]

if "life_score" not in df.columns:
    df["life_score"] = (100 - (df["thermal_score"] + df["avg_sm_pct"] / 2)).clip(0, 100)

# -------- Health Summary ----------
st.markdown("<a name='health-summary'></a>", unsafe_allow_html=True)
st.markdown("#### Health Summary")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Average Life Score", f"{df['life_score'].mean():.1f} / 100")
with col2:
    try:
        most_common = df["health_class"].mode()[0]
    except Exception:
        most_common = "N/A"
    st.metric("Most Common Condition", most_common)
with col3:
    high_risk = int(df[df["life_score"] < 30].shape[0])
    st.metric("High-Risk Units", high_risk, delta=f"-{high_risk}" if high_risk > 0 else "0")

st.markdown("---")
# -------- 📄 Download Lifecycle Report ----------
st.markdown("### 🧾 Download Lifecycle Report")

if st.button("📄 Generate Full Report", key="generate_full_report"):
    import io
    from sklearn.ensemble import IsolationForest

    # create in-memory buffer
    pdf_buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter

    # Title
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawString(160, height - 50, "Processor Lifecycle Summary Report")

    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(50, height - 80, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    pdf_canvas.drawString(50, height - 100, f"Total GPUs Analyzed: {len(df)}")

    # Key metrics
    avg_life = df['life_score'].mean() if not df['life_score'].empty else 0.0
    most_common = df['health_class'].mode()[0] if "health_class" in df.columns and not df['health_class'].empty else "N/A"
    high_risk = int(df[df['life_score'] < 30].shape[0])
    pdf_canvas.drawString(50, height - 130, f"Average Life Score: {avg_life:.2f} / 100")
    pdf_canvas.drawString(50, height - 150, f"Most Common Condition: {most_common}")
    pdf_canvas.drawString(50, height - 170, f"High-Risk Units: {high_risk}")

    # --- Detect anomalies and list GPU IDs ---
    features = ["avg_power_watts", "avg_sm_pct", "avg_mem_pct"]
    # guard: ensure features exist and have no NaNs
    for feat in features:
        if feat not in df.columns:
            df[feat] = 0
    iso = IsolationForest(contamination=0.1, random_state=42)
    try:
        iso_vals = iso.fit_predict(df[features])
        df = df.copy()
        df["Anomaly"] = iso_vals
        df["Anomaly_Label"] = df["Anomaly"].apply(lambda x: "Anomaly" if x == -1 else "Normal")
        anomaly_gpus = df.loc[df["Anomaly_Label"] == "Anomaly", "GPU_ID"].tolist()
    except Exception:
        anomaly_gpus = []

    # Add anomaly summary to report
    y_anom = height - 200
    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(50, y_anom, f"Detected Anomalies: {len(anomaly_gpus)}")
    pdf_canvas.setFont("Helvetica", 10)
    y_anom -= 18
    if anomaly_gpus:
        for gpu_id in anomaly_gpus:
            pdf_canvas.drawString(60, y_anom, f"⚠️ GPU_ID: {gpu_id}")
            y_anom -= 14
            if y_anom < 100:
                pdf_canvas.showPage()
                y_anom = height - 50
    else:
        pdf_canvas.drawString(60, y_anom, "No anomalies detected.")
        y_anom -= 18

    # GPU per-row summary (paginate if necessary)
    pdf_canvas.setFont("Helvetica-Bold", 12)
    y = y_anom - 10
    pdf_canvas.drawString(50, y, "GPU Summary:")
    y -= 18
    pdf_canvas.setFont("Helvetica", 10)
    for _, row in df.iterrows():
        gpu_id = row.get("GPU_ID", "N/A")
        health = row.get("health_class", row.get("Predicted_Class", "N/A"))
        life = row.get("life_score", 0.0)
        pdf_canvas.drawString(50, y, f"GPU_ID: {gpu_id} | Class: {health} | Life Score: {life:.1f}")
        y -= 14
        if y < 100:
            pdf_canvas.showPage()
            y = height - 50

    # finalize PDF
    pdf_canvas.save()
    pdf_buffer.seek(0)

    st.download_button(
        label="⬇️ Download PDF Report",
        data=pdf_buffer,
        file_name="Processor_Lifecycle_Report.pdf",
        mime="application/pdf",
        key="download_full_pdf"
    )
    st.success("✅ Report generated successfully!")

st.markdown("---")
# -------- Charts ----------
st.markdown("<a name='charts'></a>", unsafe_allow_html=True)
st.markdown("### Charts & Insights")

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### GPU Stress Profile")
    numeric_cols = ["avg_power_watts", "avg_sm_pct", "avg_mem_pct", "usage_hours"]
    radar_sample = df[numeric_cols].mean()
    radar = go.Figure(data=go.Scatterpolar(
        r=radar_sample.values,
        theta=numeric_cols,
        fill='toself',
        fillcolor='rgba(59, 130, 246, 0.3)',
        line=dict(color='rgb(59, 130, 246)', width=2)
    ))
    radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max(radar_sample.values) if radar_sample.values.max() > 0 else 1])),
        showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(radar, use_container_width=True, key="radar_chart")

with col2:
    st.markdown("#### Remaining Life Gauge")
    avg_life = float(df["life_score"].mean())
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_life,
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "rgb(16,185,129)" if avg_life >= 70 else "rgb(251,191,36)" if avg_life >= 40 else "rgb(239,68,68)"},
            'steps': [
                {'range': [0, 40], 'color': "rgba(239, 68, 68, 0.2)"},
                {'range': [40, 70], 'color': "rgba(251, 191, 36, 0.2)"},
                {'range': [70, 100], 'color': "rgba(16, 185, 129, 0.2)"}
            ]
        },
        number={'suffix': " / 100", 'font': {'size': 36, 'color': 'white'}}
    ))
    gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=300)
    st.plotly_chart(gauge, use_container_width=True, key="gauge_chart")

st.markdown("---")

# -------- Cluster scatter and pie ----------
col3, col4 = st.columns(2)
with col3:
    st.markdown("#### Cluster Positioning")
    fig = px.scatter(df, x="avg_power_watts", y="thermal_score", color="health_class",
                     color_discrete_map={"Healthy": "rgb(16,185,129)", "Moderate": "rgb(251,191,36)", "Critical": "rgb(239,68,68)"},
                     hover_data=["GPU_ID", "life_score"])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(30,41,59,0.5)', font=dict(color='white'))
    st.plotly_chart(fig, use_container_width=True, key="scatter_chart")
with col4:
    st.markdown("#### Health Distribution")
    pie = px.pie(df, names="health_class", color="health_class",
                 color_discrete_map={"Healthy": "rgb(16,185,129)", "Moderate": "rgb(251,191,36)", "Critical": "rgb(239,68,68)"})
    pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
    st.plotly_chart(pie, use_container_width=True, key="pie_chart")

st.markdown("---")

# -------- Maintenance & Recycling ----------
st.markdown("<a name='maintenance'></a>", unsafe_allow_html=True)
st.markdown("### 🔧 Maintenance & Recycling Recommendations")

def get_recommendations(row):
    recs = []
    if row.get("thermal_score", 0) > 18: recs.append("Clean fans, reapply thermal paste")
    if row.get("avg_power_watts", 0) > 180: recs.append("Lower power limit or increase cooling")
    if row.get("avg_sm_pct", 0) > 70 and row.get("overclock_proxy", 0) == 1: recs.append("Reduce overclock or enforce power cap")
    return ", ".join(recs) if recs else "None"

def recycling_category(row):
    if row.get("life_score", 0) > 70: return "✅ Can continue use"
    elif row.get("life_score", 0) > 40: return "⚠️ Consider partial recycling"
    else: return "🔴 Recycle / Retire"

df["Maintenance"] = df.apply(get_recommendations, axis=1)
df["Recycling"] = df.apply(recycling_category, axis=1)

display_cols = ["GPU_ID","cluster","health_class","life_score","Maintenance","Recycling",
                "usage_hours","avg_power_watts","peak_power_watts","avg_sm_pct","avg_mem_pct","thermal_score"]
display_cols = [c for c in display_cols if c in df.columns]
st.dataframe(df[display_cols].reset_index(drop=True), use_container_width=True, height=400)

st.markdown("---")

# -------- AI Insights Section ----------
st.markdown("<a name='ai-insights'></a>", unsafe_allow_html=True)
st.markdown("## AI Insights & Advanced Analytics")

# --- GPU Filter Panel ---
st.sidebar.markdown("### AI Insights")
st.sidebar.markdown("[GPU Filter Panel](#ai-insights)")
st.sidebar.markdown("[Correlation Heatmap](#ai-insights)")
st.sidebar.markdown("[Anomaly Detection](#ai-insights)")
st.sidebar.markdown("[3D Cluster Visualization](#ai-insights)")
st.sidebar.markdown("---")

st.markdown("### GPU Filter Panel")
gpu_filter = st.multiselect("Select specific GPUs to display", df["GPU_ID"].unique())
filtered_df = df[df["GPU_ID"].isin(gpu_filter)] if gpu_filter else df
st.dataframe(filtered_df, use_container_width=True, height=300)

# --- Correlation Heatmap ---
st.markdown("### Correlation Heatmap (Feature Relationships)")
import plotly.express as px
corr = filtered_df.corr(numeric_only=True)
fig_corr = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="RdBu_r",
    title="Metric Correlation Matrix"
)
fig_corr.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(30,41,59,0.6)',
    font=dict(color='white')
)
st.plotly_chart(fig_corr, use_container_width=True, key="corr_heatmap")

# --- Anomaly Detection ---
st.markdown("### AI-Powered Anomaly Detection")
from sklearn.ensemble import IsolationForest
iso = IsolationForest(contamination=0.1, random_state=42)
features = ["avg_power_watts", "avg_sm_pct", "avg_mem_pct"]
filtered_df["Anomaly"] = iso.fit_predict(filtered_df[features])
filtered_df["Anomaly_Label"] = filtered_df["Anomaly"].apply(lambda x: "Anomaly" if x == -1 else "Normal")

col_a1, col_a2 = st.columns(2)
with col_a1:
    st.metric("Detected Anomalies", int((filtered_df["Anomaly_Label"] == "Anomaly").sum()))
with col_a2:
    st.metric("Normal GPUs", int((filtered_df["Anomaly_Label"] == "Normal").sum()))

fig_anomaly = px.scatter(
    filtered_df,
    x="avg_power_watts",
    y="avg_sm_pct",
    color="Anomaly_Label",
    title="Anomaly Detection (AI-Based)",
    color_discrete_map={"Normal": "rgb(16,185,129)", "Anomaly": "rgb(239,68,68)"}
)
fig_anomaly.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(30,41,59,0.5)',
    font=dict(color='white')
)
st.plotly_chart(fig_anomaly, use_container_width=True, key="anomaly_chart")

# --- 3D Cluster Visualization ---
st.markdown("### 3D Cluster Visualization")
fig_3d = px.scatter_3d(
    filtered_df,
    x="avg_power_watts",
    y="avg_sm_pct",
    z="avg_mem_pct",
    color="health_class",
    title="GPU Clusters in 3D Space",
    color_discrete_map={"Healthy": "rgb(16,185,129)", "Moderate": "rgb(251,191,36)", "Critical": "rgb(239,68,68)"}
)
fig_3d.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white')
)
st.plotly_chart(fig_3d, use_container_width=True, key="3d_cluster_chart")

st.markdown("---")

# -------- Comparison ----------

st.markdown("<a name='comparison'></a>", unsafe_allow_html=True)
st.markdown("### GPU Comparison Mode")

gpu_list = df["GPU_ID"].tolist()
colA, colB = st.columns(2)
with colA:
    gpu1 = st.selectbox("Select GPU 1", gpu_list, key="gpu1_select")
with colB:
    gpu2 = st.selectbox("Select GPU 2", gpu_list, key="gpu2_select")

if gpu1 != gpu2:
    gpu_a = df[df["GPU_ID"] == gpu1].iloc[0]
    gpu_b = df[df["GPU_ID"] == gpu2].iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"#### 🟦 GPU {gpu1} Stats")
        st.write(gpu_a[["health_class","life_score","usage_hours","avg_power_watts","avg_sm_pct","avg_mem_pct","thermal_score"]])
    with col2:
        st.markdown(f"#### 🟩 GPU {gpu2} Stats")
        st.write(gpu_b[["health_class","life_score","usage_hours","avg_power_watts","avg_sm_pct","avg_mem_pct","thermal_score"]])

    gpu_a_eff = gpu_a.get("avg_sm_pct", 0) / max(gpu_a.get("avg_power_watts", 1), 1)
    gpu_b_eff = gpu_b.get("avg_sm_pct", 0) / max(gpu_b.get("avg_power_watts", 1), 1)
    eff_df = pd.DataFrame({"GPU":[f"GPU {gpu1}",f"GPU {gpu2}"], "Efficiency Score":[gpu_a_eff,gpu_b_eff]})
    eff_chart = px.bar(eff_df, x="GPU", y="Efficiency Score", title=" Performance vs Power Efficiency", color="GPU", color_discrete_sequence=["rgb(59,130,246)","rgb(16,185,129)"])
    eff_chart.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(30,41,59,0.4)', font=dict(color='white'))
    st.plotly_chart(eff_chart, use_container_width=True, key="eff_chart")

    def workload_recommendation(row):
        if row.get("avg_sm_pct", 0) > row.get("avg_mem_pct", 0): return "Compute-Intensive Workloads (AI/ML, HPC)"
        elif row.get("avg_mem_pct", 0) > row.get("avg_sm_pct", 0): return "Memory-Intensive Workloads (Rendering, Video Processing)"
        else: return "Balanced Workloads"

    rec1 = workload_recommendation(gpu_a)
    rec2 = workload_recommendation(gpu_b)
    st.markdown("### Recommended Optimal Usage Profiles")
    st.info(f"**GPU {gpu1} →** {rec1}\n\n**GPU {gpu2} →** {rec2}")

    st.markdown("### 📝 Export Comparison Report")

    def export_comparison_pdf(gpu1, gpu2, df_local):
        gpu_a = df_local[df_local["GPU_ID"] == gpu1].iloc[0]
        gpu_b = df_local[df_local["GPU_ID"] == gpu2].iloc[0]
        pdf_path = f"gpu_comparison_report_{gpu1}_vs_{gpu2}.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, f"GPU Comparison Report: GPU {gpu1} vs GPU {gpu2}")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        y_position = height - 120
        for col, label in [("health_class","Health"),("life_score","Life Score"),("usage_hours","Usage Hours"),
                           ("avg_power_watts","Avg Power (W)"),("peak_power_watts","Peak Power (W)"),
                           ("avg_sm_pct","Avg Compute (%)"),("avg_mem_pct","Avg Memory (%)"),
                           ("thermal_score","Thermal Score")]:
            a_val = gpu_a.get(col, "N/A")
            b_val = gpu_b.get(col, "N/A")
            c.drawString(50, y_position, f"{label} GPU {gpu1}: {a_val}")
            c.drawString(300, y_position, f"{label} GPU {gpu2}: {b_val}")
            y_position -= 20
        gpu_a_eff = gpu_a.get("avg_sm_pct", 0) / max(gpu_a.get("avg_power_watts", 1), 1)
        gpu_b_eff = gpu_b.get("avg_sm_pct", 0) / max(gpu_b.get("avg_power_watts", 1), 1)
        rec_a = workload_recommendation(gpu_a)
        rec_b = workload_recommendation(gpu_b)
        c.drawString(50, y_position-10, f"Efficiency Score GPU {gpu1}: {gpu_a_eff:.2f}")
        c.drawString(300, y_position-10, f"Efficiency Score GPU {gpu2}: {gpu_b_eff:.2f}")
        y_position -= 30
        c.drawString(50, y_position, f"Recommendation GPU {gpu1}: {rec_a}")
        c.drawString(300, y_position, f"Recommendation GPU {gpu2}: {rec_b}")
        c.save()
        return pdf_path

    if st.button("Generate PDF Report", key="gen_pdf"):
        pdf_path = export_comparison_pdf(gpu1, gpu2, df)
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(label="📥 Download PDF", data=pdf_bytes, file_name=f"GPU_Comparison_{gpu1}_vs_{gpu2}.pdf", mime="application/pdf", key="download_pdf")
        st.success("✅ PDF ready for download!")

    

st.markdown("---")
st.caption("Powered by ReCore • Sustainable GPU Lifecycle Management - Anusriya.S23BCE1360")
