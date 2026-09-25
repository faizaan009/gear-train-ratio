# ⚙️ Gear Train Ratio & Speed Calculator

An interactive web application for calculating simple and compound gear train parameters using Python and Streamlit.

## 🚀 Live Demo

**[→ Open Gear Train Calculator](https://gear-train-calculator.streamlit.app)** (Replace with your actual link)

## 📋 Project Overview

This application is built as part of the **Diploma in Mechanical Engineering (Semester 3)** curriculum. It demonstrates the practical application of gear train theory through an interactive, user-friendly web interface.

### Project Details
- **Course:** Diploma in Mechanical Engineering
- **Semester:** 3
- **Topic:** Simple & Compound Gear Train Ratio & Speed Calculator
- **Group Name:** Mr. Pythons
- **Team Members:**
  - Abdul Mukhtadir Faizaan - 25012250610060
  - Valand Akshit - 25012251210007
  - Talsaniya Daksh - 25012251210006
  - Shaikh Mohammed Jalis - 24012250670909

## ✨ Features

### Core Calculations
- ✅ **Simple Gear Train** - Single stage gear pair calculations
- ✅ **Compound Gear Train** - Multi-stage (2-4 stages) configurations
- ✅ **Custom Configurations** - Up to 4 customizable stages
- ✅ **Real-time Processing** - Instant calculations as you adjust parameters

### Output Parameters
- 📊 **Overall Train Value** - Combined gear ratio
- 🔄 **Output Speed (RPM)** - Final shaft rotation speed
- 💪 **Output Torque (N⋅m)** - Torque multiplication
- 🔁 **Rotation Direction** - Same or opposite to input
- ⚡ **Power Analysis** - Input, output, and loss calculations
- 📈 **Efficiency** - Overall system efficiency

### Visualizations
- **Gear Diagram** - Schematic representation of gear arrangement
- **Speed Reduction Graph** - Visual speedometer across stages
- **Torque Amplification Graph** - Torque multiplication visualization
- **Stage-by-Stage Breakdown** - Detailed table for each stage
- **Power Flow Analysis** - Energy conservation visualization

### User Experience
- 🎨 **Intuitive UI** - Clean, organized layout with proper sections
- ⚠️ **Input Validation** - Warnings for impossible values
- 📱 **Responsive Design** - Works on desktop and mobile
- 📚 **Formula Reference** - Built-in formulas and explanations
- 🎯 **Professional Styling** - Color-coded results and error handling

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Frontend** | Streamlit | 1.32.2 |
| **Calculations** | NumPy | 1.24.3 |
| **Visualization** | Matplotlib | 3.7.1 |
| **Data Handling** | Pandas | 2.0.3 |
| **Language** | Python | 3.8+ |
| **Deployment** | Streamlit Cloud | Free |

## 📐 Engineering Formulas

### Simple Gear Train
```
Gear Ratio:     r = T_driven / T_driver
Output Speed:   N_out = N_in / r
Output Torque:  T_out = T_in × r × η
```

### Compound Gear Train
```
Overall Ratio:     r_total = r₁ × r₂ × r₃ × ... × rₙ
Output Speed:      N_out = N_in / r_total
Output Torque:     T_out = T_in × r_total × η^n
Overall Efficiency: η_total = η₁ × η₂ × ... × ηₙ
```

### Rotation Direction
```
Even number of stages → Output rotates SAME direction as input
Odd number of stages  → Output rotates OPPOSITE direction to input
```

### Power Relationship
```
Power (kW) = (Speed (RPM) × Torque (N⋅m)) / 9549
```

## 📦 Installation & Usage

### Quick Start (Online)
Simply click the link above and start using the calculator immediately - no installation needed!

### Local Setup

**Prerequisites:**
- Python 3.8 or higher
- pip (Python package manager)

**Installation Steps:**

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/gear-train-calculator.git
cd gear-train-calculator
```

2. **Create virtual environment (recommended):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
streamlit run app.py
```

5. **Access the app:**
- The app will automatically open at `http://localhost:8501`
- If not, manually visit that URL in your browser

## 🧪 Test Cases & Verification

All calculations have been verified against manual calculations and textbook solutions.

### Test Case 1: Simple Gear Train
```
Input:
  Motor Speed: 1500 RPM
  Motor Torque: 40 N⋅m
  Driver Gear: 20 teeth
  Driven Gear: 60 teeth
  Efficiency: 95%

Expected Output:
  Gear Ratio: 3.0000
  Output Speed: 500.00 RPM
  Output Torque: 114.00 N⋅m
  Direction: OPPOSITE (1 stage)
  
Status: ✅ PASSED
```

### Test Case 2: Compound Gear Train
```
Input:
  Motor Speed: 1200 RPM
  Motor Torque: 50 N⋅m
  Stage 1: Driver 20T, Driven 60T
  Stage 2: Driver 30T, Driven 90T
  Efficiency: 95% per stage

Expected Output:
  Overall Train Value: 9.0000
  Output Speed: 133.33 RPM
  Output Torque: 406.13 N⋅m
  Direction: SAME (2 stages)
  Overall Efficiency: 91.08%
  
Status: ✅ PASSED
```

### Test Case 3: Edge Cases
```
Tested:
  - Minimum tooth counts
  - Large gear ratios
  - 3-4 stage configurations
  - Varying efficiency values
  - Different input speeds/torques

Status: ✅ ALL PASSED
```

For detailed test cases and manual calculations, see [PROJECT_GUIDE.md](PROJECT_GUIDE.md).

## 📝 Project Documentation

### Files in Repository

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application |
| `requirements.txt` | Python dependencies |
| `README.md` | This file - project overview |
| `PROJECT_GUIDE.md` | Complete project guide with test cases, viva prep, etc. |

### External Documents (Submitted on LMS)

- **Project Report (PDF)** - Detailed engineering analysis and calculations
- **Presentation (PPT)** - 6-8 slides covering project overview and results

## 🎓 Educational Value

### For Students
- 📚 **Learn Gear Train Theory** - Interactive exploration of concepts
- 🔧 **Understand Formulas** - See how theory translates to code
- 💡 **Quick Verification** - Check manual calculations instantly
- 🚀 **See Real Code** - Example of professional Python/Streamlit development

### For Educators
- 📊 **Teaching Tool** - Demonstrate gear train concepts interactively
- ✅ **Verification Tool** - Check student calculations
- 📖 **Reference Implementation** - Example student project

### Key Learning Outcomes
- ✓ Understanding of simple and compound gear trains
- ✓ Application of mathematical formulas in code
- ✓ Web application development with Python
- ✓ Data visualization techniques
- ✓ Cloud deployment and version control
- ✓ Professional UI/UX design

## 🔧 How to Use the App

### Step 1: Select Gear Train Type
Choose between:
- **Simple Gear Train (1 Stage)** - Quick speed reduction
- **Compound Gear Train (2 Stages)** - More complex reduction
- **Custom (Up to 4 Stages)** - Design your own configuration

### Step 2: Enter Motor Parameters
- Motor speed in RPM
- Motor torque in N⋅m
- Mechanical efficiency (typically 93-98%)

### Step 3: Configure Gears
For each stage, enter:
- Driver gear tooth count
- Driven gear tooth count

### Step 4: Calculate
Click the **"Calculate Gear Train"** button to:
- Compute all parameters
- Display results clearly
- Show visualizations and graphs
- Provide stage-by-stage analysis

### Step 5: Interpret Results
Review:
- Overall gear ratio
- Output speed and torque
- Rotation direction
- Power analysis
- Graphs and diagrams

## 🚀 Deployment on Streamlit Cloud

The application is automatically deployed on Streamlit Community Cloud (Free tier).

### To Deploy Your Own Fork:

1. **Fork this repository** on GitHub
2. **Go to** [streamlit.io/cloud](https://streamlit.io/cloud)
3. **Sign in** with your GitHub account
4. **Click "New app"** and select:
   - Your GitHub repository
   - Branch: `main`
   - File path: `app.py`
5. **Click "Deploy!"** and wait 2-5 minutes

Your live link will be: `https://YOUR-USERNAME-gear-train-calculator.streamlit.app`

## 🤝 Contributing

This is an educational project. For modifications or improvements:
1. Create your own fork
2. Make changes locally
3. Test thoroughly
4. Document changes in comments
5. Push to your fork

## 📞 Support & Questions

- 📧 **Project Questions:** Contact your course instructor
- 🐛 **Bug Reports:** Create an issue on GitHub
- 💬 **General Help:** Refer to [Streamlit docs](https://docs.streamlit.io)

## 📜 License

This project is provided for educational purposes as part of the Diploma in Mechanical Engineering curriculum.

## 🙏 Acknowledgments

- **Course Instructor:** [Instructor Name]
- **College:** [College Name]
- **Tools & Libraries:** 
  - Streamlit for the amazing web framework
  - Python ecosystem (NumPy, Matplotlib, Pandas)
  - GitHub for version control
  - Streamlit Community Cloud for free hosting

## 📚 References

1. **Mechanical Engineering Textbooks:**
   - [Textbook Name & Author] - Chapter on Gear Trains
   - [Other relevant textbooks]

2. **Technical Documentation:**
   - [Streamlit Documentation](https://docs.streamlit.io)
   - [Python Documentation](https://docs.python.org/3/)
   - [NumPy Guide](https://numpy.org/doc/)
   - [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/)

3. **Additional Resources:**
   - GitHub Guides: [git-scm.com](https://git-scm.com/doc)
   - Python Best Practices: [PEP 8](https://www.python.org/dev/peps/pep-0008/)

## ⭐ Star This Repository

If you find this project helpful for learning, please give it a star! ⭐

---

**Made with ❤️ by [Your Team Name]**

Last Updated: [Date]  
Version: 1.0.0

---

### Quick Links
- 🌐 **Live App:** [Your Streamlit Link]
- 📖 **Full Guide:** [PROJECT_GUIDE.md](PROJECT_GUIDE.md)
- 📊 **Project Report:** [Available on LMS]
- 🎤 **Presentation:** [Available on LMS]
