import streamlit as st
import os
from datetime import datetime
from model.model import predict

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Plant Disease Detection",
    page_icon="🌿",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* Main background with low opacity leaf effect */
.stApp {
    background:
        linear-gradient(rgba(5, 28, 32, 0.92), rgba(5, 28, 32, 0.95)),
        url("https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1600&q=80");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
}

/* Hide default Streamlit menu/footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 4px;
    letter-spacing: 1px;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #b7f7b7;
    margin-bottom: 25px;
}

.glass-card {
    background: rgba(3, 37, 42, 0.72);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid rgba(120, 255, 150, 0.22);
    box-shadow: 0 10px 28px rgba(0,0,0,0.35);
    margin-bottom: 18px;
    backdrop-filter: blur(6px);
}

.metric-card {
    background: rgba(6, 48, 54, 0.78);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid rgba(120, 255, 150, 0.18);
    text-align: center;
    min-height: 120px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.25);
}

.metric-title {
    font-size: 14px;
    color: #d6f8d6;
    margin-bottom: 6px;
}

.metric-value {
    font-size: 30px;
    font-weight: 800;
    color: #8dff8d;
}

.metric-sub {
    font-size: 13px;
    color: #d7e8e8;
}

.result-box-danger {
    background: linear-gradient(135deg, rgba(145, 20, 35, 0.92), rgba(230, 55, 55, 0.92));
    padding: 24px;
    border-radius: 18px;
    color: white;
    border: 1px solid rgba(255,255,255,0.18);
    margin-bottom: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.30);
}

.result-box-success {
    background: linear-gradient(135deg, rgba(17, 153, 142, 0.92), rgba(56, 239, 125, 0.92));
    padding: 24px;
    border-radius: 18px;
    color: white;
    border: 1px solid rgba(255,255,255,0.18);
    margin-bottom: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.30);
}

.result-title {
    font-size: 14px;
    letter-spacing: 1px;
    opacity: 0.9;
}

.result-main {
    font-size: 32px;
    font-weight: 900;
    margin-top: 5px;
}

.result-sub {
    font-size: 17px;
    opacity: 0.95;
}

.section-heading {
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 12px;
}

.small-text {
    font-size: 15px;
    color: #eaf7f7;
    line-height: 1.7;
}

.feature-line {
    margin: 7px 0;
    font-size: 15px;
}

.progress-bg {
    background: rgba(255,255,255,0.12);
    border-radius: 18px;
    height: 30px;
    width: 100%;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.12);
}

.progress-green {
    background: linear-gradient(90deg, #43a047, #8bc34a);
    height: 30px;
    border-radius: 18px;
    text-align: right;
    padding-right: 12px;
    line-height: 30px;
    font-weight: 800;
    color: white;
}

.progress-red {
    background: linear-gradient(90deg, #e53935, #ff5252);
    height: 30px;
    border-radius: 18px;
    text-align: right;
    padding-right: 12px;
    line-height: 30px;
    font-weight: 800;
    color: white;
}

.history-item {
    background: rgba(255,255,255,0.08);
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    border: 1px solid rgba(255,255,255,0.10);
}

.download-card {
    background: rgba(3, 37, 42, 0.82);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(120, 255, 150, 0.20);
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
MODEL_ACCURACY = "96.94%"
VALIDATION_ACCURACY = "88.79%"
TOTAL_CLASSES = "38"

disease_info = {
    "Apple___Apple_scab": {
        "name": "Apple Scab",
        "cause": "Fungal infection caused by Venturia inaequalis.",
        "symptoms": "Dark olive-green or black scabby spots on leaves and fruits.",
        "affected": "Apple leaves and fruits.",
        "solution": "Apply sulfur-based fungicide or captan spray. Remove infected leaves and avoid overhead watering.",
        "prevention": "Maintain proper air circulation, remove fallen infected leaves, and use resistant varieties."
    },
    "Apple___Black_rot": {
        "name": "Apple Black Rot",
        "cause": "Fungal disease caused by Botryosphaeria obtusa.",
        "symptoms": "Brown leaf spots, fruit rot, and branch cankers.",
        "affected": "Apple leaves, fruits, and branches.",
        "solution": "Remove infected fruits/leaves and apply Mancozeb or copper-based fungicide.",
        "prevention": "Prune infected branches and keep orchard clean."
    },
    "Apple___Cedar_apple_rust": {
        "name": "Cedar Apple Rust",
        "cause": "Fungal disease spread between apple and cedar/juniper plants.",
        "symptoms": "Yellow-orange spots on leaves.",
        "affected": "Apple leaves.",
        "solution": "Use fungicide sprays like myclobutanil during early infection stage.",
        "prevention": "Avoid planting apple trees near cedar or juniper trees."
    },
    "Corn_(maize)___Common_rust_": {
        "name": "Corn Common Rust",
        "cause": "Fungal infection caused by Puccinia sorghi.",
        "symptoms": "Small reddish-brown pustules on leaves.",
        "affected": "Corn leaves.",
        "solution": "Use resistant varieties and apply fungicide if infection is severe.",
        "prevention": "Use disease-free seeds and monitor crop regularly."
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "name": "Corn Gray Leaf Spot",
        "cause": "Fungal disease caused by Cercospora zeae-maydis.",
        "symptoms": "Long rectangular gray or brown lesions on leaves.",
        "affected": "Corn leaves.",
        "solution": "Apply foliar fungicide and remove infected crop residue.",
        "prevention": "Crop rotation and resistant hybrids help reduce disease."
    },
    "Grape___Black_rot": {
        "name": "Grape Black Rot",
        "cause": "Fungal infection caused by Guignardia bidwellii.",
        "symptoms": "Brown circular spots on leaves and black shriveled berries.",
        "affected": "Grape leaves and fruits.",
        "solution": "Apply fungicide and remove infected berries and leaves.",
        "prevention": "Improve air circulation and avoid wet leaves."
    },
    "Grape___Esca_(Black_Measles)": {
        "name": "Grape Esca Black Measles",
        "cause": "Complex fungal disease affecting grapevine wood.",
        "symptoms": "Tiger-stripe leaf patterns and dark spots on berries.",
        "affected": "Grape leaves, berries, and vines.",
        "solution": "Prune infected vines and avoid plant stress conditions.",
        "prevention": "Use clean pruning tools and proper vineyard management."
    },
    "Potato___Early_blight": {
        "name": "Potato Early Blight",
        "cause": "Fungal infection caused by Alternaria solani.",
        "symptoms": "Brown concentric ring spots on older leaves.",
        "affected": "Potato leaves.",
        "solution": "Use copper-based fungicide or chlorothalonil. Remove infected leaves.",
        "prevention": "Avoid overhead irrigation and rotate crops."
    },
    "Potato___Late_blight": {
        "name": "Potato Late Blight",
        "cause": "Water mold pathogen Phytophthora infestans.",
        "symptoms": "Dark water-soaked lesions and rapid leaf decay.",
        "affected": "Potato leaves and tubers.",
        "solution": "Apply fungicide immediately and destroy infected plants.",
        "prevention": "Use certified disease-free seed potatoes and avoid excess moisture."
    },
    "Tomato___Bacterial_spot": {
        "name": "Tomato Bacterial Spot",
        "cause": "Bacterial infection caused by Xanthomonas species.",
        "symptoms": "Small dark water-soaked spots on leaves and fruits.",
        "affected": "Tomato leaves and fruits.",
        "solution": "Use copper sprays and remove infected leaves.",
        "prevention": "Avoid wetting foliage and use disease-free seeds."
    },
    "Tomato___Early_blight": {
        "name": "Tomato Early Blight",
        "cause": "Fungal infection caused by Alternaria solani.",
        "symptoms": "Dark circular spots with concentric rings.",
        "affected": "Tomato leaves and stems.",
        "solution": "Apply copper fungicide and remove lower infected leaves.",
        "prevention": "Use mulch, crop rotation, and avoid water splash."
    },
    "Tomato___Late_blight": {
        "name": "Tomato Late Blight",
        "cause": "Pathogen Phytophthora infestans.",
        "symptoms": "Large dark lesions and white mold under humid conditions.",
        "affected": "Tomato leaves, stems, and fruits.",
        "solution": "Apply fungicide and remove infected plants quickly.",
        "prevention": "Avoid humid conditions and use resistant varieties."
    },
    "Tomato___Leaf_Mold": {
        "name": "Tomato Leaf Mold",
        "cause": "Fungal infection caused by Passalora fulva.",
        "symptoms": "Yellow spots on upper leaf surface and mold below.",
        "affected": "Tomato leaves.",
        "solution": "Improve ventilation and apply fungicide if needed.",
        "prevention": "Avoid high humidity and overcrowding."
    },
    "Tomato___Septoria_leaf_spot": {
        "name": "Tomato Septoria Leaf Spot",
        "cause": "Fungal disease caused by Septoria lycopersici.",
        "symptoms": "Small circular spots with gray centers.",
        "affected": "Tomato leaves.",
        "solution": "Remove infected leaves and apply fungicide.",
        "prevention": "Avoid overhead watering and maintain plant spacing."
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "name": "Tomato Spider Mites",
        "cause": "Damage caused by two-spotted spider mites.",
        "symptoms": "Yellow speckling, webbing, and leaf drying.",
        "affected": "Tomato leaves.",
        "solution": "Use insecticidal soap or neem oil spray.",
        "prevention": "Maintain humidity and regularly inspect leaves."
    },
    "Tomato___Target_Spot": {
        "name": "Tomato Target Spot",
        "cause": "Fungal infection caused by Corynespora cassiicola.",
        "symptoms": "Brown circular lesions with target-like rings.",
        "affected": "Tomato leaves.",
        "solution": "Apply fungicide and remove infected plant debris.",
        "prevention": "Crop rotation and good sanitation."
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "name": "Tomato Yellow Leaf Curl Virus",
        "cause": "Viral disease spread by whiteflies.",
        "symptoms": "Yellow curled leaves and stunted plant growth.",
        "affected": "Tomato leaves and whole plant.",
        "solution": "Control whiteflies and remove infected plants.",
        "prevention": "Use resistant varieties and insect nets."
    },
    "Tomato___Tomato_mosaic_virus": {
        "name": "Tomato Mosaic Virus",
        "cause": "Viral infection spread through contact and tools.",
        "symptoms": "Mosaic pattern, leaf distortion, and reduced growth.",
        "affected": "Tomato leaves.",
        "solution": "Remove infected plants and disinfect tools.",
        "prevention": "Use virus-free seeds and avoid tobacco contact near plants."
    }
}

# ---------------- HELPER FUNCTIONS ----------------
def clean_label(label):
    return label.replace("___", " - ").replace("_", " ")

def get_disease_details(label):
    if "healthy" in label.lower():
        return {
            "name": "Healthy Plant",
            "cause": "No disease detected.",
            "symptoms": "Leaf appears healthy.",
            "affected": "No affected part detected.",
            "solution": "No chemical treatment is required.",
            "prevention": "Continue proper watering, sunlight, soil care, and regular monitoring."
        }

    return disease_info.get(label, {
        "name": clean_label(label),
        "cause": "Specific cause is not available in the current knowledge base.",
        "symptoms": "Visible symptoms may include leaf spots, discoloration, or damage.",
        "affected": "Plant leaves.",
        "solution": "Specific treatment is not available in the current database. Please consult an agriculture expert.",
        "prevention": "Maintain proper irrigation, remove infected leaves, and monitor the plant regularly."
    })

def get_severity(confidence_percent, result):
    if "healthy" in result.lower():
        return "No Risk", "Healthy"

    if confidence_percent >= 90:
        return "High", "Severe Infection"
    elif confidence_percent >= 80:
        return "Medium", "Moderate Infection"
    elif confidence_percent >= 70:
        return "Low", "Mild Infection"
    else:
        return "Unclear", "Low confidence prediction"

def safe_percent(value):
    value = max(0, min(100, value))
    return value

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">🌿 Smart Plant Disease Detection System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-Powered Leaf Disease Detection with Treatment Recommendation</div>', unsafe_allow_html=True)

# ---------------- TOP METRICS ----------------
top1, top2, top3, top4, top5 = st.columns(5)

with top1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Classes</div>
        <div class="metric-value">{TOTAL_CLASSES}</div>
        <div class="metric-sub">Diseases + Healthy</div>
    </div>
    """, unsafe_allow_html=True)

with top2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Training Accuracy</div>
        <div class="metric-value">{MODEL_ACCURACY}</div>
        <div class="metric-sub">On Training Data</div>
    </div>
    """, unsafe_allow_html=True)

with top3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Validation Accuracy</div>
        <div class="metric-value">{VALIDATION_ACCURACY}</div>
        <div class="metric-sub">On Validation Data</div>
    </div>
    """, unsafe_allow_html=True)

with top4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Model Used</div>
        <div class="metric-value">CNN</div>
        <div class="metric-sub">Deep Learning Model</div>
    </div>
    """, unsafe_allow_html=True)

with top5:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Input Type</div>
        <div class="metric-value">Image</div>
        <div class="metric-sub">Upload / Camera</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- MAIN LAYOUT ----------------
left, right = st.columns([1, 4])

with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📥 Input Panel</div>', unsafe_allow_html=True)

    input_choice = st.radio(
        "Choose Input Method",
        ["Upload Image", "Camera Capture"]
    )

    uploaded_file = None
    camera_file = None

    if input_choice == "Upload Image":
        uploaded_file = st.file_uploader("Upload leaf image", type=["jpg", "jpeg", "png"])
    else:
        camera_file = st.camera_input("Capture leaf image")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🧠 System Features</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="small-text">
        <div class="feature-line">✔ CNN-based disease detection</div>
        <div class="feature-line">✔ Image upload and camera input</div>
        <div class="feature-line">✔ Confidence score</div>
        <div class="feature-line">✔ Severity level prediction</div>
        <div class="feature-line">✔ Treatment recommendation</div>
        <div class="feature-line">✔ Prevention tips</div>
        <div class="feature-line">✔ Report generation & download</div>
        <div class="feature-line">✔ History of predictions</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📚 Dataset Info</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="small-text">
        <b>Source:</b> Kaggle / PlantVillage Dataset<br>
        <b>Total Classes:</b> 38<br>
        <b>Image Type:</b> Plant leaf images<br>
        <b>Training Split:</b> 90%<br>
        <b>Validation Split:</b> 10%
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FILE PROCESSING ----------------
file_path = None

if uploaded_file is not None:
    file_path = "temp_leaf.jpg"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

elif camera_file is not None:
    file_path = "temp_leaf.jpg"
    with open(file_path, "wb") as f:
        f.write(camera_file.getbuffer())

# ---------------- RIGHT PANEL ----------------
with right:
    if file_path is None:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">📌 Project Overview</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="small-text">
        This project is an AI-based plant disease detection system using a Convolutional Neural Network.
        It accepts plant leaf images through upload or camera capture and predicts whether the leaf is healthy
        or affected by disease. The system also provides confidence score, severity level, treatment recommendation,
        prevention tips, and downloadable diagnosis report.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        with st.spinner("Analyzing leaf image using trained CNN model..."):
            result, confidence = predict(file_path)

        confidence_percent = safe_percent(confidence * 100)
        uncertainty_percent = safe_percent(100 - confidence_percent)
        clean_result = clean_label(result)
        details = get_disease_details(result)
        severity, severity_text = get_severity(confidence_percent, result)

        is_invalid = confidence_percent < 60

        if is_invalid:
            clean_result = "Invalid or unclear leaf image"
            status = "Invalid Input"
            severity = "Unclear"
            severity_text = "Please upload clear leaf image"
            details = {
                "name": "Invalid Input",
                "cause": "The uploaded image is not clear or may not be a plant leaf.",
                "symptoms": "No valid leaf disease symptoms detected.",
                "affected": "Not applicable.",
                "solution": "Please upload or capture a clear plant leaf image.",
                "prevention": "Avoid human face, background objects, blurry images, or non-leaf images."
            }
        else:
            status = "Healthy" if "healthy" in result.lower() else "Disease Detected"

        # Add history
        st.session_state.history.insert(0, {
            "result": clean_result,
            "confidence": confidence_percent,
            "time": datetime.now().strftime("%I:%M %p")
        })
        st.session_state.history = st.session_state.history[:5]

        # Result box
        box_class = "result-box-success" if status == "Healthy" else "result-box-danger"
        icon = "✅" if status == "Healthy" else "⚠️"

        st.markdown(f"""
        <div class="{box_class}">
            <div class="result-title">PREDICTION RESULT</div>
            <div class="result-main">{icon} {clean_result}</div>
            <div class="result-sub">{status}</div>
        </div>
        """, unsafe_allow_html=True)

        # Result metrics
        r1, r2, r3 = st.columns(3)

        with r1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Severity Level</div>
                <div class="metric-value">{severity}</div>
                <div class="metric-sub">{severity_text}</div>
            </div>
            """, unsafe_allow_html=True)

        with r2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Confidence Score</div>
                <div class="metric-value">{confidence_percent:.2f}%</div>
                <div class="metric-sub">Model Confidence</div>
            </div>
            """, unsafe_allow_html=True)

        with r3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Prediction Status</div>
                <div class="metric-value">{status}</div>
                <div class="metric-sub">Classification Output</div>
            </div>
            """, unsafe_allow_html=True)

        # Middle row
        img_col, analysis_col, history_col = st.columns([1.1, 1.2, 1])

        with img_col:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">🖼️ Image Preview</div>', unsafe_allow_html=True)
            st.image(file_path, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with analysis_col:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">📊 Prediction Analysis</div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="small-text"><b>Confidence Progress</b></div>
            <div class="progress-bg">
                <div class="progress-green" style="width:{confidence_percent}%;">{confidence_percent:.2f}%</div>
            </div>

            <br>
            <div class="small-text"><b>Confidence vs Uncertainty</b></div>
            <br>

            <div class="small-text">Confidence</div>
            <div class="progress-bg">
                <div class="progress-green" style="width:{confidence_percent}%;">{confidence_percent:.2f}%</div>
            </div>

            <br>
            <div class="small-text">Uncertainty</div>
            <div class="progress-bg">
                <div class="progress-red" style="width:{uncertainty_percent}%;">{uncertainty_percent:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with history_col:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">🕘 Recent Predictions</div>', unsafe_allow_html=True)

            for item in st.session_state.history:
                st.markdown(f"""
                <div class="history-item">
                    <b>{item["result"]}</b><br>
                    Confidence: {item["confidence"]:.2f}%<br>
                    Time: {item["time"]}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # Details row
        d1, d2, d3 = st.columns(3)

        with d1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">📘 Disease Information</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="small-text">
                <b>Disease Name:</b> {details["name"]}<br><br>
                <b>Cause:</b> {details["cause"]}<br><br>
                <b>Symptoms:</b> {details["symptoms"]}<br><br>
                <b>Affected Part:</b> {details["affected"]}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with d2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">💊 Treatment Recommendation</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="small-text">
                {details["solution"]}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with d3:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">🛡️ Prevention Tips</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="small-text">
                {details["prevention"]}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Report
        report = f"""
AI-BASED PLANT DISEASE DIAGNOSIS REPORT

Generated On: {datetime.now().strftime("%d-%m-%Y %I:%M %p")}

Prediction Result: {clean_result}
Status: {status}
Confidence Score: {confidence_percent:.2f}%
Severity Level: {severity} - {severity_text}

Disease Information:
Disease Name: {details["name"]}
Cause: {details["cause"]}
Symptoms: {details["symptoms"]}
Affected Part: {details["affected"]}

Treatment Recommendation:
{details["solution"]}

Prevention Tips:
{details["prevention"]}

Model Details:
Model Used: Convolutional Neural Network (CNN)
Training Accuracy: {MODEL_ACCURACY}
Validation Accuracy: {VALIDATION_ACCURACY}
Total Classes: {TOTAL_CLASSES}

Dataset:
Source: Kaggle / PlantVillage Dataset
Image Type: Plant Leaf Images
Training Split: 90%
Validation Split: 10%

Note:
This result is generated by an AI-based prediction system. For severe crop infection, expert consultation is recommended.
"""

        st.markdown('<div class="download-card">', unsafe_allow_html=True)
        dl1, dl2 = st.columns([2, 1])
        with dl1:
            st.markdown('<div class="section-heading">📄 Download Diagnosis Report</div>', unsafe_allow_html=True)
            st.markdown('<div class="small-text">Get complete prediction, disease information, treatment and prevention details in a text report.</div>', unsafe_allow_html=True)

        with dl2:
            st.download_button(
                label="⬇️ Download Report",
                data=report,
                file_name="plant_disease_diagnosis_report.txt",
                mime="text/plain",
                use_container_width=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

        if os.path.exists(file_path):
            os.remove(file_path)