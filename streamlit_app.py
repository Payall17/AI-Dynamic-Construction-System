import streamlit as st
from core_engine import optimize_beam
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="AI Construction Command Center", layout="wide")

st.title(" AI Dynamic Construction Command Center")
st.markdown("Real-Time Generative Structural Recalibration & Digital Twin System")

# -----------------------------
# INPUT SECTION
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("Design Inputs")
    span = st.number_input("Span (m)", value=5.0)
    expected_load = st.number_input("Expected Load (N/m)", value=20000.0)
    material = st.selectbox("Material", ["Concrete", "Steel"])

# -----------------------------
# INITIAL DESIGN
# -----------------------------

initial_design = optimize_beam(span, expected_load, material)

with col2:
    st.subheader("Initial Optimized Design")
    if initial_design:
        st.metric("Beam Depth (m)", initial_design["depth"])
        st.metric("Safety Factor", initial_design["safety_factor"])
        st.metric("Estimated Cost (₹)", initial_design["cost"])

# -----------------------------
# SENSOR SLIDER
# -----------------------------

st.markdown("---")
st.subheader("📡 Real-Time Load Monitoring")

actual_load = st.slider(
    "Actual Load Detected (N/m)",
    min_value=int(expected_load * 0.5),
    max_value=int(expected_load * 1.5),
    value=int(expected_load)
)

# -----------------------------
# RECALIBRATION
# -----------------------------

updated_design = optimize_beam(span, actual_load, material)

st.markdown("---")
st.subheader("🔁 AI Recalibrated Design")

col3, col4 = st.columns(2)

with col3:
    st.markdown("### Initial Design")
    st.write(initial_design)

with col4:
    st.markdown("### Updated Design")
    st.write(updated_design)

# -----------------------------
# RISK INDICATOR
# -----------------------------

if updated_design:
    if updated_design["safety_factor"] < 1.5:
        st.error("⚠ Structural Risk Detected!")
    else:
        st.success("✅ Structure Within Safe Limits")

# =====================================================
# VISUAL SECTION STARTS HERE
# =====================================================

st.markdown("---")
st.header("📊 Structural Intelligence Visualizations")

# -----------------------------
# 1️⃣ Animated Load Graph
# -----------------------------

st.subheader("📈 Load Fluctuation Simulation")

chart_placeholder = st.empty()
load_data = []

for i in range(30):
    simulated = actual_load * (1 + np.random.uniform(-0.05, 0.05))
    load_data.append(simulated)

    fig, ax = plt.subplots(figsize=(6, 3))  # width, height in inches
    ax.plot(load_data)
    ax.set_title("Real-Time Load Variation")
    ax.set_ylabel("Load (N/m)")
    ax.set_xlabel("Time Step")

    chart_placeholder.pyplot(fig)
    time.sleep(0.05)

# -----------------------------
# 2️⃣ Cost Comparison Bar Chart
# -----------------------------

st.subheader("💰 Cost Comparison")

if initial_design and updated_design:
    fig2, ax2 = plt.subplots(figsize=(6, 3))  # width, height in inches
    ax2.bar(["Initial", "Updated"], 
            [initial_design["cost"], updated_design["cost"]])
    ax2.set_ylabel("Cost (₹)")
    ax2.set_title("Cost Before vs After Recalibration")

    st.pyplot(fig2)

# -----------------------------
# 3️⃣ Depth Visualization
# -----------------------------

st.subheader("📐 Beam Depth Comparison")

if initial_design and updated_design:

    fig3, ax3 = plt.subplots(figsize=(6, 3))  # width, height in inches

    ax3.bar(["Initial Depth", "Updated Depth"],
            [initial_design["depth"], updated_design["depth"]])

    ax3.set_ylabel("Depth (m)")
    ax3.set_title("Structural Adaptation - Depth Adjustment")

    st.pyplot(fig3)

# -----------------------------
# 4️⃣ Digital Twin Beam Schematic
# -----------------------------

st.subheader("🏗 Digital Twin Beam Representation")

if updated_design:

    fig4, ax4 = plt.subplots(figsize=(6, 3))  # width, height in inches

    # Draw beam
    ax4.add_patch(plt.Rectangle((0, 0),
                                span,
                                updated_design["depth"],
                                fill=True))

    ax4.set_xlim(0, span)
    ax4.set_ylim(0, updated_design["depth"] * 1.5)

    ax4.set_title("Digital Twin Beam Model")
    ax4.set_xlabel("Span (m)")
    ax4.set_ylabel("Depth (m)")

    st.pyplot(fig4)

