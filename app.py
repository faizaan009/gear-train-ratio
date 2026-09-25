import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Gear Train Calculator",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {color: #1f77b4; font-size: 2.5em; font-weight: bold;}
    .sub-header {color: #ff7f0e; font-size: 1.5em; font-weight: bold; margin-top: 20px;}
    .result-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #ff7f0e;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">⚙️ Gear Train Ratio & Speed Calculator</h1>', unsafe_allow_html=True)

# Group Details (Update with your details)
col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Group:** [Your Group Number]\n**Members:** [Member Names]")
with col2:
    st.info("**Course:** Diploma in Mechanical Engineering\n**Semester:** 3")
with col3:
    st.info("**Project:** Simple & Compound Gear Train\n**Tool:** Python + Streamlit")

st.divider()

# Sidebar for inputs
st.markdown('<h2 class="sub-header">📋 Gear Train Configuration</h2>', unsafe_allow_html=True)

col_config1, col_config2 = st.columns(2)

with col_config1:
    st.subheader("Input Parameters")
    
    # Motor speed input
    motor_speed = st.number_input(
        "Input Motor Speed (RPM)",
        min_value=10,
        max_value=10000,
        value=1200,
        step=50,
        help="Speed of the input/driving shaft"
    )
    
    # Motor torque input
    motor_torque = st.number_input(
        "Input Motor Torque (N⋅m)",
        min_value=0.1,
        max_value=1000.0,
        value=50.0,
        step=5.0,
        help="Torque delivered by the input shaft"
    )
    
    # Mechanical efficiency
    efficiency = st.slider(
        "Mechanical Efficiency (%)",
        min_value=50,
        max_value=100,
        value=95,
        step=1,
        help="Accounts for friction losses in bearings and gear mesh"
    ) / 100

with col_config2:
    st.subheader("Train Type Selection")
    train_type = st.radio(
        "Select Gear Train Type:",
        ["Simple Gear Train (1 Stage)", "Compound Gear Train (2 Stages)", "Custom (Up to 4 Stages)"]
    )

st.divider()

# Function to validate gear inputs
def validate_gears(driver_teeth, driven_teeth):
    """Validate gear tooth counts"""
    errors = []
    if driver_teeth <= 0 or driven_teeth <= 0:
        errors.append("❌ Tooth count must be greater than 0")
    if driver_teeth < 12 or driven_teeth < 12:
        errors.append("⚠️ Minimum practical tooth count is 12 (risk of undercut)")
    if driver_teeth > 500 or driven_teeth > 500:
        errors.append("⚠️ Tooth count exceeds 500 (unusually large gear)")
    return errors

# Function to calculate train results
def calculate_gear_train(motor_speed, motor_torque, stages, efficiency):
    """
    Calculate gear train parameters
    stages: list of tuples [(driver_teeth, driven_teeth), ...]
    """
    results = {
        'stage_ratios': [],
        'errors': [],
        'warnings': []
    }
    
    overall_ratio = 1.0
    current_speed = motor_speed
    current_torque = motor_torque
    
    for i, (driver, driven) in enumerate(stages):
        # Validate
        errors = validate_gears(driver, driven)
        if errors:
            results['errors'].extend([f"Stage {i+1}: {e}" for e in errors])
        
        # Calculate ratio
        ratio = driven / driver
        overall_ratio *= ratio
        
        # Calculate stage output
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
    
    # Overall results
    results['overall_ratio'] = overall_ratio
    results['output_speed'] = motor_speed / overall_ratio
    results['output_torque'] = motor_torque * overall_ratio * (efficiency ** len(stages))
    results['num_stages'] = len(stages)
    results['rotation_direction'] = "SAME" if len(stages) % 2 == 0 else "OPPOSITE"
    
    return results

# Input configuration based on selected train type
stages = []

if train_type == "Simple Gear Train (1 Stage)":
    st.subheader("Stage 1: Simple Gear Pair")
    col1, col2 = st.columns(2)
    with col1:
        driver1 = st.number_input(
            "Driver Gear Teeth (Stage 1)",
            min_value=1,
            max_value=500,
            value=20,
            help="Teeth on the driving gear (input)"
        )
    with col2:
        driven1 = st.number_input(
            "Driven Gear Teeth (Stage 1)",
            min_value=1,
            max_value=500,
            value=60,
            help="Teeth on the driven gear (output of this stage)"
        )
    stages = [(driver1, driven1)]

elif train_type == "Compound Gear Train (2 Stages)":
    st.subheader("Stage 1: First Gear Pair")
    col1, col2 = st.columns(2)
    with col1:
        driver1 = st.number_input(
            "Driver Teeth (Stage 1)",
            min_value=1,
            max_value=500,
            value=20,
            key="s1_driver"
        )
    with col2:
        driven1 = st.number_input(
            "Driven Teeth (Stage 1)",
            min_value=1,
            max_value=500,
            value=60,
            key="s1_driven"
        )
    
    st.subheader("Stage 2: Second Gear Pair")
    col1, col2 = st.columns(2)
    with col1:
        driver2 = st.number_input(
            "Driver Teeth (Stage 2)",
            min_value=1,
            max_value=500,
            value=30,
            key="s2_driver"
        )
    with col2:
        driven2 = st.number_input(
            "Driven Teeth (Stage 2)",
            min_value=1,
            max_value=500,
            value=90,
            key="s2_driven"
        )
    stages = [(driver1, driven1), (driver2, driven2)]

else:  # Custom up to 4 stages
    num_stages = st.number_input(
        "Number of Stages",
        min_value=1,
        max_value=4,
        value=2,
        help="Add multiple gear stages"
    )
    
    for i in range(num_stages):
        st.subheader(f"Stage {i+1}: Gear Pair")
        col1, col2 = st.columns(2)
        with col1:
            driver = st.number_input(
                f"Driver Teeth (Stage {i+1})",
                min_value=1,
                max_value=500,
                value=20 + (i*10),
                key=f"custom_driver_{i}"
            )
        with col2:
            driven = st.number_input(
                f"Driven Teeth (Stage {i+1})",
                min_value=1,
                max_value=500,
                value=60 + (i*30),
                key=f"custom_driven_{i}"
            )
        stages.append((driver, driven))

st.divider()

# Calculate results
if st.button("🔧 Calculate Gear Train", use_container_width=True, type="primary"):
    results = calculate_gear_train(motor_speed, motor_torque, stages, efficiency)
    
    # Show errors and warnings
    if results['errors']:
        for error in results['errors']:
            st.markdown(f'<div class="error-box">{error}</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="sub-header">📊 Calculation Results</h2>', unsafe_allow_html=True)
    
    # Summary Results
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="result-box">
        <h3 style="margin-top: 0;">Overall Train Value</h3>
        <h2 style="color: #1f77b4; margin: 10px 0;">{results['overall_ratio']:.4f}</h2>
        <p style="margin: 0; font-size: 0.9em; color: #666;">Gear Ratio Product</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="result-box">
        <h3 style="margin-top: 0;">Output Speed</h3>
        <h2 style="color: #1f77b4; margin: 10px 0;">{results['output_speed']:.2f}</h2>
        <p style="margin: 0; font-size: 0.9em; color: #666;">RPM</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="result-box">
        <h3 style="margin-top: 0;">Output Torque</h3>
        <h2 style="color: #1f77b4; margin: 10px 0;">{results['output_torque']:.2f}</h2>
        <p style="margin: 0; font-size: 0.9em; color: #666;">N⋅m</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        rotation = "🔄 SAME" if results['rotation_direction'] == "SAME" else "🔁 OPPOSITE"
        st.markdown(f"""
        <div class="result-box">
        <h3 style="margin-top: 0;">Output Rotation</h3>
        <h2 style="color: #1f77b4; margin: 10px 0;">{rotation}</h2>
        <p style="margin: 0; font-size: 0.9em; color: #666;">Direction</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Stage-by-stage breakdown
    st.markdown('<h3 class="sub-header">🔍 Stage-by-Stage Breakdown</h3>', unsafe_allow_html=True)
    
    df_stages = pd.DataFrame(results['stage_ratios'])
    df_stages_display = df_stages.copy()
    df_stages_display.columns = ['Stage', 'Driver (T)', 'Driven (T)', 'Ratio', 'Speed (RPM)', 'Torque (N⋅m)']
    df_stages_display['Ratio'] = df_stages_display['Ratio'].apply(lambda x: f"{x:.4f}")
    df_stages_display['Speed (RPM)'] = df_stages_display['Speed (RPM)'].apply(lambda x: f"{x:.2f}")
    df_stages_display['Torque (N⋅m)'] = df_stages_display['Torque (N⋅m)'].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(df_stages_display, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Visualization: Gear Diagram
    st.markdown('<h3 class="sub-header">📐 Gear Train Schematic</h3>', unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.set_xlim(-1, 14)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.axis('off')
    
    x_pos = 0.5
    
    # Input motor
    motor_rect = FancyBboxPatch((x_pos - 0.4, -0.6), 0.8, 1.2, 
                                 boxstyle="round,pad=0.1", 
                                 edgecolor='black', facecolor='#ffcccc', linewidth=2)
    ax.add_patch(motor_rect)
    ax.text(x_pos, 0, f"{motor_speed}\nRPM", ha='center', va='center', fontsize=9, fontweight='bold')
    ax.text(x_pos, -1.5, "Motor Input", ha='center', fontsize=8)
    
    x_pos += 1.5
    
    # Draw each stage
    for i, (driver, driven) in enumerate(stages):
        # Driver gear
        driver_radius = driver / 20
        circle_driver = Circle((x_pos, 0.5), driver_radius, 
                              edgecolor='#2196F3', facecolor='#E3F2FD', linewidth=2)
        ax.add_patch(circle_driver)
        ax.text(x_pos, 0.5, f"{driver}T", ha='center', va='center', fontsize=7, fontweight='bold')
        
        # Driven gear
        driven_radius = driven / 20
        circle_driven = Circle((x_pos + driver_radius + driven_radius, 0.5), driven_radius,
                              edgecolor='#FF9800', facecolor='#FFE0B2', linewidth=2)
        ax.add_patch(circle_driven)
        ax.text(x_pos + driver_radius + driven_radius, 0.5, f"{driven}T", 
               ha='center', va='center', fontsize=7, fontweight='bold')
        
        # Stage label and ratio
        stage_output = results['stage_ratios'][i]['output_speed']
        ax.text(x_pos + driver_radius + driven_radius / 2, -1.5, 
               f"Stage {i+1}\nRatio: {results['stage_ratios'][i]['ratio']:.2f}\n{stage_output:.1f} RPM",
               ha='center', va='top', fontsize=8, bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
        
        x_pos += driver_radius + driven_radius + 1.5
    
    # Output
    output_rect = FancyBboxPatch((x_pos - 0.4, -0.6), 0.8, 1.2,
                                  boxstyle="round,pad=0.1",
                                  edgecolor='black', facecolor='#ccffcc', linewidth=2)
    ax.add_patch(output_rect)
    ax.text(x_pos, 0, f"{results['output_speed']:.1f}\nRPM", ha='center', va='center', fontsize=9, fontweight='bold')
    ax.text(x_pos, -1.5, "Output", ha='center', fontsize=8)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.divider()
    
    # Graph: Speed vs Stage
    st.markdown('<h3 class="sub-header">📈 Speed Reduction Across Stages</h3>', unsafe_allow_html=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    stages_list = ['Input'] + [f'Stage {i+1}' for i in range(len(results['stage_ratios']))]
    speeds = [motor_speed] + [r['output_speed'] for r in results['stage_ratios']]
    torques = [motor_torque] + [r['output_torque'] for r in results['stage_ratios']]
    
    # Speed graph
    ax1.plot(stages_list, speeds, marker='o', linewidth=2.5, markersize=10, color='#2196F3')
    ax1.fill_between(range(len(stages_list)), speeds, alpha=0.3, color='#2196F3')
    ax1.set_ylabel('Speed (RPM)', fontsize=11, fontweight='bold')
    ax1.set_xlabel('Gear Train Stage', fontsize=11, fontweight='bold')
    ax1.set_title('Speed Reduction Through Gear Stages', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    for i, (stage, speed) in enumerate(zip(stages_list, speeds)):
        ax1.text(i, speed + max(speeds)*0.03, f'{speed:.1f}', ha='center', fontsize=9, fontweight='bold')
    
    # Torque graph
    ax2.plot(stages_list, torques, marker='s', linewidth=2.5, markersize=10, color='#FF9800')
    ax2.fill_between(range(len(stages_list)), torques, alpha=0.3, color='#FF9800')
    ax2.set_ylabel('Torque (N⋅m)', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Gear Train Stage', fontsize=11, fontweight='bold')
    ax2.set_title('Torque Amplification Through Gear Stages', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    for i, (stage, torque) in enumerate(zip(stages_list, torques)):
        ax2.text(i, torque + max(torques)*0.03, f'{torque:.1f}', ha='center', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.divider()
    
    # Power relationship
    st.markdown('<h3 class="sub-header">⚡ Power Analysis</h3>', unsafe_allow_html=True)
    
    input_power = (motor_speed * motor_torque) / 9549  # Convert to kW
    output_power = (results['output_speed'] * results['output_torque']) / 9549
    power_loss = input_power - output_power
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Input Power", f"{input_power:.3f} kW")
    with col2:
        st.metric("Output Power", f"{output_power:.3f} kW")
    with col3:
        st.metric("Power Loss", f"{power_loss:.3f} kW")
    with col4:
        efficiency_calc = (output_power / input_power * 100) if input_power > 0 else 0
        st.metric("Overall Efficiency", f"{efficiency_calc:.1f}%")

else:
    st.info("👈 Click **Calculate Gear Train** button to run the simulation")

st.divider()

# Formula Reference
with st.expander("📚 Formula Reference"):
    st.markdown("""
    ### Simple Gear Train
    - **Gear Ratio:** r = T_driven / T_driver
    - **Output Speed:** N_out = N_in / r
    - **Output Torque:** T_out = T_in × r × η
    
    ### Compound Gear Train
    - **Overall Ratio:** r_total = r₁ × r₂ × r₃ × ...
    - **Output Speed:** N_out = N_in / r_total
    - **Output Torque:** T_out = T_in × r_total × η^n (where n = number of stages)
    
    ### Rotation Direction
    - **Even number of stages:** Output rotates in SAME direction as input
    - **Odd number of stages:** Output rotates in OPPOSITE direction to input
    
    ### Power Relationship
    - **Power (kW):** P = (N × T) / 9549, where N is in RPM and T is in N⋅m
    - **Power is conserved:** P_in = P_out (ideally, with efficiency losses)
    """)

st.divider()

# Footer
st.markdown("""
---
**Disclaimer:** This calculator is for educational purposes. Verify results with proper engineering standards and material strength calculations before real-world application.

**Made with ❤️ using Python & Streamlit | Diploma in Mechanical Engineering**
""")
