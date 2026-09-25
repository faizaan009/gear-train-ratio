import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, FancyBboxPatch, Wedge
import pandas as pd
from matplotlib.animation import FuncAnimation
from io import BytesIO
import plotly.graph_objects as go
import plotly.express as px

# ============================================================================
# PAGE CONFIG & THEME
# ============================================================================
st.set_page_config(
    page_title="Gear Train Calculator | Mr. Pythons",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Black/White/Blue Theme
st.markdown("""
<style>
    :root {
        --primary-color: #1e3a8a;      /* Dark Blue */
        --secondary-color: #3b82f6;    /* Blue */
        --accent-color: #0f172a;       /* Near Black */
        --text-light: #f8fafc;         /* Light Gray/White */
        --text-dark: #1e293b;          /* Dark Gray */
        --success: #10b981;            /* Green */
        --warning: #f59e0b;            /* Orange */
        --error: #ef4444;              /* Red */
    }
    
    body {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    .main {
        background-color: #0f172a;
    }
    
    .stApp {
        background-color: #0f172a;
    }
    
    .header-title {
        color: #3b82f6;
        font-size: 3em;
        font-weight: 900;
        text-align: center;
        text-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
        margin: 20px 0;
    }
    
    .subheader {
        color: #93c5fd;
        font-size: 1.8em;
        font-weight: bold;
        margin: 30px 0 20px 0;
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 10px;
    }
    
    .info-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #60a5fa;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
        color: #f8fafc;
    }
    
    .result-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #3b82f6;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        color: #f8fafc;
    }
    
    .result-value {
        color: #60a5fa;
        font-size: 2em;
        font-weight: bold;
    }
    
    .warning-box {
        background: rgba(245, 158, 11, 0.1);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #f59e0b;
        margin: 10px 0;
        color: #fcd34d;
    }
    
    .error-box {
        background: rgba(239, 68, 68, 0.1);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ef4444;
        margin: 10px 0;
        color: #fca5a5;
    }
    
    .success-box {
        background: rgba(16, 185, 129, 0.1);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #10b981;
        margin: 10px 0;
        color: #86efac;
    }
    
    /* Streamlit Components */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1e3a8a 100%);
        color: #f8fafc;
        border: none;
        border-radius: 8px;
        padding: 12px 30px;
        font-weight: bold;
        font-size: 1.1em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
        box-shadow: 0 6px 20px rgba(96, 165, 250, 0.4);
        transform: translateY(-2px);
    }
    
    .stNumberInput, .stSlider, .stSelectbox, .stRadio {
        color: #f8fafc;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #1e3a8a;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_3d_rotating_gear(num_teeth=20, rotation=0):
    """Create 3D gear mesh data for animation"""
    theta = np.linspace(0, 2*np.pi, num_teeth*10, endpoint=False)
    
    # Gear profile
    r_outer = 1.0
    r_root = 0.6
    
    # Create tooth pattern
    tooth_profile = []
    for i in range(num_teeth):
        start_angle = (2*np.pi * i) / num_teeth
        end_angle = start_angle + (np.pi / num_teeth) * 0.6
        mid_angle = (start_angle + end_angle) / 2
        
        # Outer tooth
        tooth_profile.append([r_outer * np.cos(start_angle), r_outer * np.sin(start_angle), 0])
        tooth_profile.append([r_outer * np.cos(mid_angle), r_outer * np.sin(mid_angle), 0.1])
        tooth_profile.append([r_outer * np.cos(end_angle), r_outer * np.sin(end_angle), 0])
        
        # Root between teeth
        root_start = end_angle
        root_end = start_angle + (2*np.pi / num_teeth)
        root_mid = (root_start + root_end) / 2
        tooth_profile.append([r_root * np.cos(root_mid), r_root * np.sin(root_mid), 0])
    
    tooth_profile = np.array(tooth_profile)
    
    # Apply rotation
    rotation_angle = rotation
    cos_r = np.cos(rotation_angle)
    sin_r = np.sin(rotation_angle)
    
    x = tooth_profile[:, 0] * cos_r - tooth_profile[:, 1] * sin_r
    y = tooth_profile[:, 0] * sin_r + tooth_profile[:, 1] * cos_r
    z = tooth_profile[:, 2]
    
    return x, y, z

def create_animated_gear_plot():
    """Create an animated 3D gear visualization"""
    frames = []
    
    for frame in range(0, 360, 10):
        x1, y1, z1 = create_3d_rotating_gear(20, np.radians(frame))
        x2, y2, z2 = create_3d_rotating_gear(60, np.radians(-frame/3))
        
        # Offset second gear
        x2 += 3.0
        
        frames.append((x1, y1, z1, x2, y2, z2))
    
    return frames

def validate_gears(driver_teeth, driven_teeth):
    """Validate gear tooth counts"""
    errors = []
    warnings = []
    
    if driver_teeth <= 0 or driven_teeth <= 0:
        errors.append("Tooth count must be greater than 0")
    if driver_teeth < 12:
        warnings.append(f"Driver gear {driver_teeth}T: Risk of undercut (minimum 12T)")
    if driven_teeth < 12:
        warnings.append(f"Driven gear {driven_teeth}T: Risk of undercut (minimum 12T)")
    if driver_teeth > 500 or driven_teeth > 500:
        warnings.append("Tooth count exceeds 500 (unusually large)")
    
    return errors, warnings

def calculate_gear_train(motor_speed, motor_torque, stages, efficiency):
    """Calculate complete gear train parameters"""
    results = {
        'stage_ratios': [],
        'errors': [],
        'warnings': []
    }
    
    overall_ratio = 1.0
    current_speed = motor_speed
    current_torque = motor_torque
    
    for i, (driver, driven) in enumerate(stages):
        errors, warnings = validate_gears(driver, driven)
        results['errors'].extend(errors)
        results['warnings'].extend(warnings)
        
        ratio = driven / driver
        overall_ratio *= ratio
        stage_speed = current_speed / ratio
        stage_torque = current_torque * ratio * efficiency
        
        results['stage_ratios'].append({
            'stage': i + 1,
            'driver_teeth': driver,
            'driven_teeth': driven,
            'ratio': ratio,
            'output_speed': stage_speed,
            'output_torque': stage_torque
        })
        
        current_speed = stage_speed
        current_torque = stage_torque
    
    results['overall_ratio'] = overall_ratio
    results['output_speed'] = motor_speed / overall_ratio
    results['output_torque'] = motor_torque * overall_ratio * (efficiency ** len(stages))
    results['num_stages'] = len(stages)
    results['rotation_direction'] = "SAME" if len(stages) % 2 == 0 else "OPPOSITE"
    
    return results

# ============================================================================
# PAGE LAYOUT
# ============================================================================

# HEADER
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="header-title">⚙️ GEAR TRAIN CALCULATOR</h1>', unsafe_allow_html=True)

# GROUP INFO
st.markdown('<div class="subheader">👥 Team: Mr. Pythons</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="info-box">
    <b>Members:</b><br>
    • Abdul Mukhtadir Faizaan<br>
    • Valand Akshit<br>
    • Talsaniya Daksh<br>
    • Shaikh Mohammed Jalis
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-box">
    <b>Enrollment Numbers:</b><br>
    • 25012250610060<br>
    • 25012251210007<br>
    • 25012251210006<br>
    • 24012250670909
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# INPUT SECTION
# ============================================================================

st.markdown('<div class="subheader">⚙️ Configuration</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Motor Parameters")
    motor_speed = st.number_input(
        "Input Speed (RPM)",
        min_value=10, max_value=10000, value=1200, step=50,
        help="Rotation speed of input shaft"
    )
    motor_torque = st.number_input(
        "Input Torque (N⋅m)",
        min_value=0.1, max_value=1000.0, value=50.0, step=5.0,
        help="Torque delivered by input"
    )

with col2:
    st.subheader("System Parameters")
    efficiency = st.slider(
        "Mechanical Efficiency (%)",
        min_value=50, max_value=100, value=95, step=1
    ) / 100
    
    train_type = st.radio(
        "Gear Train Type:",
        ["Simple (1 Stage)", "Compound (2 Stages)", "Custom (Up to 4)"],
        horizontal=True
    )

st.markdown("---")

# ============================================================================
# GEAR CONFIGURATION
# ============================================================================

st.markdown('<div class="subheader">🔧 Gear Configuration</div>', unsafe_allow_html=True)

stages = []

if train_type == "Simple (1 Stage)":
    col1, col2 = st.columns(2)
    with col1:
        driver1 = st.number_input("Driver Teeth", min_value=1, max_value=500, value=20, key="s1d")
    with col2:
        driven1 = st.number_input("Driven Teeth", min_value=1, max_value=500, value=60, key="s1dd")
    stages = [(driver1, driven1)]

elif train_type == "Compound (2 Stages)":
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Stage 1")
        d1_driver = st.number_input("Driver", min_value=1, max_value=500, value=20, key="s2d1")
        d1_driven = st.number_input("Driven", min_value=1, max_value=500, value=60, key="s2d1d")
    with col2:
        st.subheader("Stage 2")
        d2_driver = st.number_input("Driver", min_value=1, max_value=500, value=30, key="s2d2")
        d2_driven = st.number_input("Driven", min_value=1, max_value=500, value=90, key="s2d2d")
    stages = [(d1_driver, d1_driven), (d2_driver, d2_driven)]

else:
    num_stages = st.number_input("Number of Stages", min_value=1, max_value=4, value=2)
    for i in range(num_stages):
        col1, col2 = st.columns(2)
        with col1:
            driver = st.number_input(f"Stage {i+1} - Driver", min_value=1, max_value=500, 
                                    value=20+(i*10), key=f"cd{i}")
        with col2:
            driven = st.number_input(f"Stage {i+1} - Driven", min_value=1, max_value=500, 
                                    value=60+(i*30), key=f"cdd{i}")
        stages.append((driver, driven))

st.markdown("---")

# ============================================================================
# CALCULATE BUTTON
# ============================================================================

if st.button("🚀 CALCULATE GEAR TRAIN", use_container_width=True, type="primary"):
    
    results = calculate_gear_train(motor_speed, motor_torque, stages, efficiency)
    
    # Show errors
    if results['errors']:
        for error in results['errors']:
            st.markdown(f'<div class="error-box">❌ {error}</div>', unsafe_allow_html=True)
    
    # Show warnings
    if results['warnings']:
        for warning in results['warnings']:
            st.markdown(f'<div class="warning-box">⚠️ {warning}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="subheader">📊 Results</div>', unsafe_allow_html=True)
    
    # MAIN RESULTS
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="result-box">
        <b>Train Value</b><br>
        <div class="result-value">{results['overall_ratio']:.4f}</div>
        <small>Gear Ratio</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="result-box">
        <b>Output Speed</b><br>
        <div class="result-value">{results['output_speed']:.2f}</div>
        <small>RPM</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="result-box">
        <b>Output Torque</b><br>
        <div class="result-value">{results['output_torque']:.2f}</div>
        <small>N⋅m</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        direction = "🔄 SAME" if results['rotation_direction'] == "SAME" else "🔁 OPPOSITE"
        st.markdown(f"""
        <div class="result-box">
        <b>Rotation</b><br>
        <div class="result-value">{direction}</div>
        <small>Direction</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ANIMATED 3D GEAR VISUALIZATION
    st.markdown('<div class="subheader">🎬 3D Animated Gear Train</div>', unsafe_allow_html=True)
    
    # Create 3D animation using plotly
    fig = go.Figure()
    
    # Animation frames
    frames_data = []
    for frame_num in range(0, 36):
        angle = frame_num * 10
        
        # First gear
        x1, y1, z1 = create_3d_rotating_gear(int(stages[0][0]), np.radians(angle))
        
        # Second gear (offset and rotated differently based on ratio)
        ratio = stages[0][1] / stages[0][0]
        x2, y2, z2 = create_3d_rotating_gear(int(stages[0][1]), np.radians(-angle * ratio))
        x2 += 3.0
        
        # Additional gears if compound
        if len(stages) > 1:
            x3, y3, z3 = create_3d_rotating_gear(int(stages[1][0]), np.radians(-angle * ratio))
            x3 += 3.0
            y3 += 2.0
            
            ratio2 = stages[1][1] / stages[1][0]
            x4, y4, z4 = create_3d_rotating_gear(int(stages[1][1]), np.radians(angle * ratio * ratio2))
            x4 += 6.0
            y4 += 2.0
        
        frame = go.Frame(
            data=[
                go.Scatter3d(x=x1, y=y1, z=z1, mode='markers', 
                           marker=dict(size=4, color='#3b82f6'), name='Gear 1'),
                go.Scatter3d(x=x2, y=y2, z=z2, mode='markers',
                           marker=dict(size=4, color='#60a5fa'), name='Gear 2'),
            ],
            name=str(frame_num)
        )
        
        if len(stages) > 1:
            frame.data += (
                go.Scatter3d(x=x3, y=y3, z=z3, mode='markers',
                           marker=dict(size=4, color='#93c5fd'), name='Gear 3'),
                go.Scatter3d(x=x4, y=y4, z=z4, mode='markers',
                           marker=dict(size=4, color='#dbeafe'), name='Gear 4'),
            )
        
        frames_data.append(frame)
    
    # Initial data
    angle = 0
    x1, y1, z1 = create_3d_rotating_gear(int(stages[0][0]), np.radians(angle))
    ratio = stages[0][1] / stages[0][0]
    x2, y2, z2 = create_3d_rotating_gear(int(stages[0][1]), np.radians(-angle * ratio))
    x2 += 3.0
    
    fig.add_trace(go.Scatter3d(x=x1, y=y1, z=z1, mode='markers',
                              marker=dict(size=4, color='#3b82f6'), name=f'Gear 1 ({stages[0][0]}T)'))
    fig.add_trace(go.Scatter3d(x=x2, y=y2, z=z2, mode='markers',
                              marker=dict(size=4, color='#60a5fa'), name=f'Gear 2 ({stages[0][1]}T)'))
    
    if len(stages) > 1:
        x3, y3, z3 = create_3d_rotating_gear(int(stages[1][0]), np.radians(-angle * ratio))
        x3 += 3.0
        y3 += 2.0
        ratio2 = stages[1][1] / stages[1][0]
        x4, y4, z4 = create_3d_rotating_gear(int(stages[1][1]), np.radians(angle * ratio * ratio2))
        x4 += 6.0
        y4 += 2.0
        
        fig.add_trace(go.Scatter3d(x=x3, y=y3, z=z3, mode='markers',
                                  marker=dict(size=4, color='#93c5fd'), name=f'Gear 3 ({stages[1][0]}T)'))
        fig.add_trace(go.Scatter3d(x=x4, y=y4, z=z4, mode='markers',
                                  marker=dict(size=4, color='#dbeafe'), name=f'Gear 4 ({stages[1][1]}T)'))
    
    fig.frames = frames_data
    
    fig.update_layout(
        title="3D Rotating Gear Train Animation",
        scene=dict(
            xaxis=dict(backgroundcolor="rgb(15, 23, 42)", gridcolor="rgb(30, 58, 138)", showbackground=True),
            yaxis=dict(backgroundcolor="rgb(15, 23, 42)", gridcolor="rgb(30, 58, 138)", showbackground=True),
            zaxis=dict(backgroundcolor="rgb(15, 23, 42)", gridcolor="rgb(30, 58, 138)", showbackground=True),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
        ),
        updatemenus=[
            dict(type='buttons', showactive=False, buttons=[
                dict(label='▶ PLAY', method='animate',
                     args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)]),
                dict(label='⏸ PAUSE', method='animate',
                     args=[[None], dict(frame=dict(duration=0, redraw=False), mode='immediate')])
            ])
        ],
        paper_bgcolor="rgb(15, 23, 42)",
        plot_bgcolor="rgb(15, 23, 42)",
        font=dict(color="rgb(248, 250, 252)"),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # STAGE BREAKDOWN TABLE
    st.markdown('<div class="subheader">📋 Stage-by-Stage Breakdown</div>', unsafe_allow_html=True)
    
    df_stages = pd.DataFrame(results['stage_ratios'])
    df_display = df_stages.copy()
    df_display.columns = ['Stage', 'Driver (T)', 'Driven (T)', 'Ratio', 'Speed (RPM)', 'Torque (N⋅m)']
    df_display['Ratio'] = df_display['Ratio'].apply(lambda x: f"{x:.4f}")
    df_display['Speed (RPM)'] = df_display['Speed (RPM)'].apply(lambda x: f"{x:.2f}")
    df_display['Torque (N⋅m)'] = df_display['Torque (N⋅m)'].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # SPEED & TORQUE GRAPHS
    st.markdown('<div class="subheader">📈 Performance Graphs</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    stages_labels = ['Input'] + [f'Stage {r["stage"]}' for r in results['stage_ratios']]
    speeds = [motor_speed] + [r['output_speed'] for r in results['stage_ratios']]
    torques = [motor_torque] + [r['output_torque'] for r in results['stage_ratios']]
    
    with col1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=stages_labels, y=speeds,
            mode='lines+markers+text',
            text=[f'{s:.1f}' for s in speeds],
            textposition='top center',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=12, color='#60a5fa'),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.2)',
            name='Speed'
        ))
        fig1.update_layout(
            title="Speed Reduction Through Stages",
            xaxis_title="Stage",
            yaxis_title="Speed (RPM)",
            paper_bgcolor="rgb(15, 23, 42)",
            plot_bgcolor="rgb(30, 58, 138)",
            font=dict(color="rgb(248, 250, 252)"),
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=stages_labels, y=torques,
            mode='lines+markers+text',
            text=[f'{t:.1f}' for t in torques],
            textposition='top center',
            line=dict(color='#f59e0b', width=3),
            marker=dict(size=12, color='#fbbf24'),
            fill='tozeroy',
            fillcolor='rgba(245, 158, 11, 0.2)',
            name='Torque'
        ))
        fig2.update_layout(
            title="Torque Amplification Through Stages",
            xaxis_title="Stage",
            yaxis_title="Torque (N⋅m)",
            paper_bgcolor="rgb(15, 23, 42)",
            plot_bgcolor="rgb(30, 58, 138)",
            font=dict(color="rgb(248, 250, 252)"),
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # POWER ANALYSIS
    st.markdown('<div class="subheader">⚡ Power Analysis</div>', unsafe_abuse=True)
    
    input_power = (motor_speed * motor_torque) / 9549
    output_power = (results['output_speed'] * results['output_torque']) / 9549
    power_loss = input_power - output_power
    overall_eff = (output_power / input_power * 100) if input_power > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Input Power", f"{input_power:.3f} kW", delta="100%")
    with col2:
        st.metric("Output Power", f"{output_power:.3f} kW", delta=f"{overall_eff:.1f}%")
    with col3:
        st.metric("Power Loss", f"{power_loss:.3f} kW", delta=f"{100-overall_eff:.1f}%")
    with col4:
        st.metric("Efficiency", f"{overall_eff:.1f}%", delta=None)
    
    st.markdown("---")
    
    # SUCCESS MESSAGE
    st.markdown('<div class="success-box">✅ Calculation Completed Successfully!</div>', unsafe_allow_html=True)

else:
    st.info("👈 Click **CALCULATE GEAR TRAIN** button to run simulation")

st.markdown("---")

# FORMULA REFERENCE
with st.expander("📚 Formula Reference"):
    st.markdown("""
    ### Simple Gear Train
    - **Gear Ratio:** r = T_driven / T_driver
    - **Output Speed:** N_out = N_in / r
    - **Output Torque:** T_out = T_in × r × η
    
    ### Compound Gear Train
    - **Overall Ratio:** r_total = r₁ × r₂ × r₃ × ...
    - **Output Speed:** N_out = N_in / r_total
    - **Output Torque:** T_out = T_in × r_total × η^n
    
    ### Rotation Direction
    - **Even stages:** Output = SAME direction as input
    - **Odd stages:** Output = OPPOSITE direction from input
    
    ### Power
    - **P (kW):** (Speed × Torque) / 9549
    """)

st.markdown("---")

# FOOTER
st.markdown("""
<div style='text-align: center; color: #60a5fa; padding: 20px;'>
<b>⚙️ Gear Train Calculator | Mr. Pythons Team</b><br>
Diploma in Mechanical Engineering - Semester 3<br>
<small>Made with ❤️ using Python & Streamlit</small>
</div>
""", unsafe_allow_html=True)
