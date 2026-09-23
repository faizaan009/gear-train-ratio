"""
Simple & Compound Gear Train Ratio & Speed Calculator
Diploma in Mechanical Engineering – Semester 3 Mini Project
Framework: Streamlit + NumPy + Matplotlib
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Gear Train Calculator",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# Custom CSS for a cleaner look
# ------------------------------------------------------------------
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1e3a5f;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #5a6a7a;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .result-box {
        background: linear-gradient(135deg, #e8f4fd 0%, #f0f7ff 100%);
        border: 1px solid #b6d4f0;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .result-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0d47a1;
    }
    .result-label {
        font-size: 0.85rem;
        color: #546e7a;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .formula-box {
        background: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        font-family: 'Courier New', monospace;
        font-size: 0.95rem;
    }
    .stAlert { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Header & Team details (edit these for your group)
# ------------------------------------------------------------------
st.markdown('<p class="main-header">⚙️ Simple & Compound Gear Train Calculator</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Diploma in Mechanical Engineering · Semester 3 Mini Project</p>',
    unsafe_allow_html=True,
)

with st.expander("👥 Group / Team Details", expanded=False):
    st.markdown("""
    | Field | Value |
    |-------|-------|
    | **Group Number** | *(Mr. Pythons)* |
    | **Member 1** | Abdul Mukhtadir Faizaan – 25012250610060 |
    | **Member 2** | Shaikh Mohammed Jalis Sarfaraz  – 25012250670909 |
    | **Member 3** | Talsaniya Daksh – 25012251210006 |
    | **Member 4** | Valand Akshit – 25012251210007 |
    | **Guide / Faculty** | **MohammedAzim Shaikh** |
    """)

st.divider()

# ------------------------------------------------------------------
# Sidebar – User Inputs
# ------------------------------------------------------------------
st.sidebar.header("📥 Input Parameters")

train_type = st.sidebar.radio(
    "Gear Train Type",
    options=["Compound", "Simple"],
    index=0,
    help="Compound: intermediate shafts carry two gears (ratios multiply). "
         "Simple: all gears on separate shafts (idlers cancel in ratio magnitude).",
)

st.sidebar.subheader("Motor / Input")
input_rpm = st.sidebar.number_input(
    "Input Speed  Nᵢₙ  (RPM)",
    min_value=0.0,
    value=1500.0,
    step=50.0,
    format="%.1f",
)
input_torque = st.sidebar.number_input(
    "Input Torque  Tᵢₙ  (N·m)  [optional]",
    min_value=0.0,
    value=10.0,
    step=0.5,
    format="%.2f",
    help="Leave at 0 if you only need speed ratio.",
)
efficiency = st.sidebar.slider(
    "Mechanical Efficiency  η  (%)",
    min_value=50,
    max_value=100,
    value=95,
    step=1,
    help="Typical spur-gear efficiency ≈ 96–99 % per stage. Overall value used here.",
)

st.sidebar.subheader("Gear Stages (Tooth Counts)")
num_stages = st.sidebar.number_input(
    "Number of Stages",
    min_value=1,
    max_value=6,
    value=2,
    step=1,
)

stages = []
for i in range(int(num_stages)):
    st.sidebar.markdown(f"**Stage {i+1}**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        driver = st.number_input(
            f"Driver T{i+1}",
            min_value=1,
            value=20 if i == 0 else 25,
            step=1,
            key=f"driver_{i}",
        )
    with col2:
        driven = st.number_input(
            f"Driven T{i+1}",
            min_value=1,
            value=60 if i == 0 else 75,
            step=1,
            key=f"driven_{i}",
        )
    stages.append({"driver": driver, "driven": driven})

# ------------------------------------------------------------------
# Validation
# ------------------------------------------------------------------
errors = []
if input_rpm < 0:
    errors.append("Input speed cannot be negative.")
if efficiency <= 0 or efficiency > 100:
    errors.append("Efficiency must be between 1 % and 100 %.")
for i, s in enumerate(stages):
    if s["driver"] < 1 or s["driven"] < 1:
        errors.append(f"Stage {i+1}: Tooth counts must be ≥ 1.")
    if s["driver"] == s["driven"] and train_type == "Compound":
        pass  # 1:1 is allowed

if errors:
    for e in errors:
        st.error(f"⚠️ {e}")
    st.stop()

# ------------------------------------------------------------------
# Calculations
# ------------------------------------------------------------------
eta = efficiency / 100.0
stage_ratios = []
mesh_count = 0

if train_type == "Compound":
    overall_GR = 1.0
    for s in stages:
        gr = s["driven"] / s["driver"]
        stage_ratios.append(gr)
        overall_GR *= gr
        mesh_count += 1
else:
    # Simple train: ratio depends only on first driver & last driven
    first_driver = stages[0]["driver"]
    last_driven = stages[-1]["driven"]
    overall_GR = last_driven / first_driver
    for s in stages:
        stage_ratios.append(s["driven"] / s["driver"])
    mesh_count = len(stages)  # each listed pair counts as one mesh for direction

output_rpm = input_rpm / overall_GR if overall_GR > 0 else 0.0
output_torque = input_torque * overall_GR * eta if input_torque > 0 else None
same_direction = (mesh_count % 2 == 0)

# ------------------------------------------------------------------
# Results Display
# ------------------------------------------------------------------
st.subheader("📊 Calculated Results")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="result-box">
            <div class="result-label">Overall Gear Ratio</div>
            <div class="result-value">{overall_GR:.4g} : 1</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if overall_GR > 1.001:
        st.caption("Speed reduction · Torque increase")
    elif overall_GR < 0.999:
        st.caption("Speed increase · Torque decrease")
    else:
        st.caption("1 : 1 transmission")

with c2:
    st.markdown(
        f"""
        <div class="result-box">
            <div class="result-label">Output Speed</div>
            <div class="result-value">{output_rpm:.2f}</div>
            <div style="font-size:0.85rem;color:#546e7a;">RPM</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    if output_torque is not None:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-label">Output Torque</div>
                <div class="result-value">{output_torque:.3f}</div>
                <div style="font-size:0.85rem;color:#546e7a;">N·m  (η = {efficiency} %)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="result-box">
                <div class="result-label">Output Torque</div>
                <div class="result-value">—</div>
                <div style="font-size:0.85rem;color:#546e7a;">Enter Tᵢₙ</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with c4:
    dir_text = "Same" if same_direction else "Opposite"
    dir_color = "#2e7d32" if same_direction else "#e65100"
    st.markdown(
        f"""
        <div class="result-box">
            <div class="result-label">Final Direction</div>
            <div class="result-value" style="color:{dir_color};">{dir_text}</div>
            <div style="font-size:0.85rem;color:#546e7a;">as input shaft</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------
# Formulas Used
# ------------------------------------------------------------------
with st.expander("📐 Engineering Formulas Used", expanded=False):
    st.markdown("""
    **Single stage gear ratio**
    $$
    GR_i = \\frac{T_{\\text{driven},i}}{T_{\\text{driver},i}}
    $$

    **Compound train (overall)**
    $$
    GR_{\\text{overall}} = \\prod_{i=1}^{n} GR_i = \\frac{\\text{product of all driven teeth}}{\\text{product of all driver teeth}}
    $$

    **Simple train (overall)**
    $$
    GR_{\\text{overall}} = \\frac{T_{\\text{last driven}}}{T_{\\text{first driver}}}
    $$
    (Intermediate idler gears cancel out for the magnitude of the ratio.)

    **Output speed**
    $$
    N_{\\text{out}} = \\frac{N_{\\text{in}}}{GR_{\\text{overall}}}
    $$

    **Output torque (with efficiency)**
    $$
    T_{\\text{out}} = T_{\\text{in}} \\times GR_{\\text{overall}} \\times \\eta
    $$

    **Direction of rotation**  
    Each external mesh reverses direction.  
    Odd number of meshes → opposite to input; even number → same as input.
    """)

# ------------------------------------------------------------------
# Stage-wise breakdown table
# ------------------------------------------------------------------
st.subheader("🔍 Stage-wise Breakdown")
table_data = []
for i, s in enumerate(stages):
    gr = stage_ratios[i]
    table_data.append({
        "Stage": i + 1,
        "Driver Teeth": s["driver"],
        "Driven Teeth": s["driven"],
        "Stage GR": round(gr, 4),
        "Type": "Reduction" if gr > 1 else ("Increase" if gr < 1 else "1:1"),
    })
st.dataframe(table_data, use_container_width=True, hide_index=True)

if train_type == "Compound":
    st.info(f"**Overall GR** = product of stage ratios = **{overall_GR:.4g} : 1**")
else:
    st.info(
        f"**Simple train**: Overall GR depends only on first driver ({stages[0]['driver']} T) "
        f"and last driven ({stages[-1]['driven']} T) → **{overall_GR:.4g} : 1**"
    )

# ------------------------------------------------------------------
# Visualization (required)
# ------------------------------------------------------------------
st.subheader("📈 Visualization")

tab1, tab2 = st.tabs(["Stage Gear Ratios", "Speed & Torque Comparison"])

with tab1:
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    stage_labels = [f"Stage {i+1}" for i in range(len(stage_ratios))]
    colors = ["#3b82f6" if r >= 1 else "#f59e0b" for r in stage_ratios]
    bars = ax1.bar(stage_labels, stage_ratios, color=colors, edgecolor="white", width=0.55)
    ax1.axhline(1.0, color="#94a3b8", linestyle="--", linewidth=1, label="1 : 1")
    ax1.set_ylabel("Gear Ratio (Driven / Driver)", fontsize=11)
    ax1.set_xlabel("Stage", fontsize=11)
    ax1.set_title(f"Stage-wise Gear Ratios  |  Overall GR = {overall_GR:.3g} : 1", fontsize=12, pad=10)
    ax1.grid(axis="y", linestyle=":", alpha=0.6)
    ax1.legend(loc="upper right")
    for bar, r in zip(bars, stage_ratios):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.03,
            f"{r:.3g}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )
    ax1.set_ylim(0, max(stage_ratios) * 1.25 if stage_ratios else 2)
    st.pyplot(fig1)
    plt.close(fig1)

with tab2:
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    categories = ["Input Speed\n(RPM)", "Output Speed\n(RPM)"]
    values = [input_rpm, output_rpm]
    bar_colors = ["#6366f1", "#22c55e"]
    bars2 = ax2.bar(categories, values, color=bar_colors, edgecolor="white", width=0.5)
    ax2.set_ylabel("Speed (RPM)", fontsize=11)
    ax2.set_title("Input vs Output Speed", fontsize=12, pad=10)
    ax2.grid(axis="y", linestyle=":", alpha=0.6)
    for bar, v in zip(bars2, values):
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(values) * 0.02,
            f"{v:.1f}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )
    if output_torque is not None:
        # Twin axis for torque
        ax2b = ax2.twinx()
        ax2b.bar(
            ["Input Torque\n(N·m)", "Output Torque\n(N·m)"],
            [input_torque, output_torque],
            color=["#a5b4fc", "#86efac"],
            alpha=0.7,
            width=0.35,
            align="edge",
        )
        ax2b.set_ylabel("Torque (N·m)", fontsize=11, color="#166534")
        ax2b.tick_params(axis="y", labelcolor="#166534")
    st.pyplot(fig2)
    plt.close(fig2)

# ------------------------------------------------------------------
# Sample Verification (Paper vs App)
# ------------------------------------------------------------------
st.subheader("✅ Sample Problem Verification (Paper vs App)")
st.markdown(r"""
**Textbook-style numerical (Compound train)**  

| Parameter | Value |
|-----------|-------|
| Stage 1 | Driver = 20 T, Driven = 60 T |
| Stage 2 | Driver = 25 T, Driven = 75 T |
| Input speed | 1500 RPM |
| Input torque | 10 N·m |
| Efficiency | 95 % |

**Manual calculation**  
- \( GR_1 = 60/20 = 3 \)  
- \( GR_2 = 75/25 = 3 \)  
- \( GR_{overall} = 3 \times 3 = 9 \)  
- \( N_{out} = 1500 / 9 = 166.67 \) RPM  
- \( T_{out} = 10 \times 9 \times 0.95 = 85.5 \) N·m  
- 2 external meshes → **Same direction** as input  

**App result (with default sidebar values above)** should match the numbers shown in the Results section.
""")

# ------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------
st.divider()
st.caption(
    "Simple & Compound Gear Train Ratio & Speed Calculator · "
    "Built with Streamlit · Diploma ME Sem-3 Mini Project"
)
