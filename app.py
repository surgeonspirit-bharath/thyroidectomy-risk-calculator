import streamlit as st
import numpy as np

# -----------------------------
# Model coefficients (example)
# -----------------------------
BETA_0 = -5.20
BETA_1 = 0.052
RISK_THRESHOLD = 0.26

# -----------------------------
# Point assignment function
# -----------------------------
def calculate_points(
    neck_circumference,
    mallampati,
    tirads,
    malignancy,
    retrosternal,
    gland_size,
    swe,
    symptoms_duration
):
    points = 0

    # Neck circumference
    if neck_circumference >= 40:
        points += 30

    # Mallampati
    if mallampati in ["III", "IV"]:
        points += 26

    # TIRADS
    if tirads >= 4:
        points += 32

    # Malignancy
    if malignancy == "Yes":
        points += 35

    # Retrosternal extension
    if retrosternal == "Yes":
        points += 28

    # Gland size
    if gland_size > 6:
        points += 24

    # SWE stiffness (baseline 30 kPa)
    swe_points = max(0, (swe - 30) * 0.18)
    points += swe_points

    # Duration of symptoms
    if symptoms_duration > 6:
        points += 15

    return round(points, 1)


# -----------------------------
# Probability function
# -----------------------------
def predict_probability(total_points):
    logit = BETA_0 + BETA_1 * total_points
    return 1 / (1 + np.exp(-logit))


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Thyroidectomy Risk Calculator", layout="centered")

st.title("🩺 Difficult Thyroidectomy Risk Calculator")
st.markdown("Automated Nomogram-Based Clinical Decision Tool")

# -----------------------------
# Input Section
# -----------------------------
st.header("🔍 Preoperative Inputs")

col1, col2 = st.columns(2)

with col1:
    neck = st.number_input("Neck Circumference (cm)", 30.0, 60.0, 38.0)
    mallampati = st.selectbox("Mallampati Class", ["I", "II", "III", "IV"])
    tirads = st.selectbox("TIRADS Score", [1, 2, 3, 4, 5])

    gland = st.number_input("Gland Size (cm)", 2.0, 12.0, 5.0)

with col2:
    malignancy = st.selectbox("Malignancy (FNAC/Imaging)", ["No", "Yes"])
    retrosternal = st.selectbox("Retrosternal Extension", ["No", "Yes"])
    swe = st.number_input("SWE Stiffness (kPa)", 10.0, 150.0, 40.0)
    duration = st.number_input("Duration of Symptoms (months)", 0, 60, 3)

# -----------------------------
# Calculate
# -----------------------------
if st.button("Calculate Risk"):

    total_points = calculate_points(
        neck, mallampati, tirads,
        malignancy, retrosternal,
        gland, swe, duration
    )

    risk = predict_probability(total_points)

    st.subheader("📊 Results")

    st.metric("Total Nomogram Score", total_points)
    st.metric("Predicted Risk", f"{risk:.2%}")

    # Risk classification
    if total_points >= 80:
        st.error("⚠️ High Risk for Difficult Thyroidectomy")
        st.markdown("**Recommendation:** Senior surgeon, advanced planning, nerve monitoring advised.")
    else:
        st.success("✅ Low Risk")
        st.markdown("**Recommendation:** Standard surgical planning appropriate.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Based on interim predictive model (n=200, AUC=0.81)")
