import streamlit as st
import joblib
import numpy as np
import pandas as pd
from prediction import predict_diabetes
from reco import get_recommendations
from utils import calculate_bmi, bmi_category, calculate_health_score

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="DiaCare AI",
    page_icon="🩺",
    layout="wide"
)

# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("diacare_model.pkl")

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main{
    background:#f4f9fc;
}

.title{
    text-align:center;
    font-size:42px;
    color:#0077b6;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    font-size:20px;
    color:gray;
}

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.1);
}

</style>
""",unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.image(
    "https://img.icons8.com/color/96/stethoscope.png",
    width=80
)

st.sidebar.title("DiaCare AI")

menu=st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📝 Health Assessment",
        "ℹ About"
    ]
)

# -----------------------------
# HOME
# -----------------------------
if menu=="🏠 Home":

    st.markdown(
        "<h1 class='title'>🩺 DiaCare AI</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p class='subtitle'>Smart Diabetes Risk Assessment & Lifestyle Advisor</p>",
        unsafe_allow_html=True
    )

    st.write("")

    c1,c2,c3=st.columns(3)

    with c1:
        st.metric(
            "Model",
            "Random Forest"
        )

    with c2:
        st.metric(
            "Classes",
            "3"
        )

    with c3:
        st.metric(
            "Features",
            "9"
        )

    st.write("---")

    st.markdown("""
### Welcome 👋

DiaCare AI predicts

🟢 No Diabetes

🟡 Pre-Diabetes

🔴 Diabetes

using Machine Learning.

### Features

✅ Automatic BMI

✅ Health Score

✅ Diabetes Risk

✅ Diet Plan

✅ Exercise Plan

✅ Water Intake

✅ Sleep Recommendation

✅ PDF Health Report

Select **Health Assessment** from the sidebar to begin.
""")

# -----------------------------
# ABOUT
# -----------------------------
elif menu=="ℹ About":

    st.title("About DiaCare AI")

    st.write("""

DiaCare AI is an intelligent healthcare application developed using

• Python

• Streamlit

• Machine Learning

• Random Forest Classifier

Dataset:

CDC BRFSS 2015 Diabetes Health Indicators

Prediction Classes

🟢 No Diabetes

🟡 Pre-Diabetes

🔴 Diabetes

""")

# -----------------------------
# HEALTH ASSESSMENT
# -----------------------------
elif menu=="📝 Health Assessment":

    st.title("Health Assessment")

    left,right=st.columns(2)

    with left:

        age=st.slider(
            "Age",
            18,
            100,
            30
        )

        gender=st.selectbox(
            "Gender",
            [
                "Male",
                "Female"
            ]
        )

        height=st.number_input(
            "Height (cm)",
            100,
            250,
            170
        )

        weight=st.number_input(
            "Weight (kg)",
            20,
            200,
            70
        )

        high_bp=st.selectbox(
            "High Blood Pressure",
            [
                "No",
                "Yes"
            ]
        )

    with right:

        high_chol=st.selectbox(
            "High Cholesterol",
            [
                "No",
                "Yes"
            ]
        )

        smoker=st.selectbox(
            "Smoking",
            [
                "No",
                "Yes"
            ]
        )

        activity=st.selectbox(
            "Physical Activity",
            [
                "Yes",
                "No"
            ]
        )

        fruits=st.selectbox(
            "Eat Fruits Regularly",
            [
                "Yes",
                "No"
            ]
        )

        veggies=st.selectbox(
            "Eat Vegetables Regularly",
            [
                "Yes",
                "No"
            ]
        )

    bmi=calculate_bmi(
        height,
        weight
    )

    st.write("---")

    st.metric(
        "BMI",
        f"{bmi:.2f}"
    )

    st.info(
        bmi_category(bmi)
    )

    predict_button=st.button(
        "🩺 Predict Diabetes Risk",
        use_container_width=True
    )

    if predict_button:

        sex=1 if gender=="Male" else 0
        bp=1 if high_bp=="Yes" else 0
        chol=1 if high_chol=="Yes" else 0
        smoke=1 if smoker=="Yes" else 0
        act=1 if activity=="Yes" else 0
        fruit=1 if fruits=="Yes" else 0
        veg=1 if veggies=="Yes" else 0

        prediction,confidence=predict_diabetes(
            model,
            bp,
            chol,
            bmi,
            smoke,
            act,
            fruit,
            veg,
            sex,
            age
        )

        health_score=calculate_health_score(
            bmi,
            bp,
            chol,
            smoke,
            act,
            fruit,
            veg
        )

        st.write("---")
                # -----------------------------
        # Result Display
        # -----------------------------

        st.subheader("📊 Prediction Result")

        if prediction == 0:
            st.success("🟢 No Diabetes Detected")
            risk_level = "Low Risk"

        elif prediction == 1:
            st.warning("🟡 Pre-Diabetes Detected")
            risk_level = "Medium Risk"

        else:
            st.error("🔴 Diabetes Detected")
            risk_level = "High Risk"

        st.metric("Confidence Score", f"{confidence*100:.2f}%")
        st.metric("Health Score", f"{health_score}/100")
        st.info(f"Risk Level: {risk_level}")

        # -----------------------------
        # Recommendations
        # -----------------------------

        st.write("---")
        st.subheader("🥗 Lifestyle Recommendations")

        recommendations = get_recommendations(
            bmi=bmi,
            bp=bp,
            chol=chol,
            smoke=smoke,
            activity=act,
            fruit=fruit,
            veg=veg,
            age=age,
            prediction=prediction
        )

        st.markdown("### 🍎 Diet Plan")
        for item in recommendations["diet"]:
            st.write("•", item)

        st.markdown("### 🏃 Exercise Plan")
        for item in recommendations["exercise"]:
            st.write("•", item)

        st.markdown("### 💧 Water Intake")
        st.write(recommendations["water"])

        st.markdown("### 😴 Sleep Recommendation")
        st.write(recommendations["sleep"])

        # -----------------------------
        # Health Summary Card
        # -----------------------------

        st.write("---")

        st.markdown(f"""
        <div class="card">
            <h3>📋 Health Summary</h3>
            <p><b>BMI:</b> {bmi:.2f}</p>
            <p><b>Risk Level:</b> {risk_level}</p>
            <p><b>Health Score:</b> {health_score}/100</p>
            <p><b>Prediction Confidence:</b> {confidence*100:.2f}%</p>
        </div>
        """, unsafe_allow_html=True)

        # -----------------------------
        # Future Extension Note
        # -----------------------------

        