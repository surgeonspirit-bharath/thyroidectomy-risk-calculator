import streamlit as st

# Thyroidectomy Risk Calculator

st.title('Thyroidectomy Risk Calculator')

st.write('This app calculates the risk associated with thyroidectomy based on various parameters.')

# User input fields
age = st.number_input('Age', min_value=0)
sex = st.selectbox('Sex', options=['Male', 'Female'])
comorbidities = st.multiselect('Comorbidities', options=['Diabetes', 'Hypertension', 'Cardiovascular Disease'])
medications = st.text_input('Medications', 'Enter medications separated by commas')

# Risk assessment logic can be adjusted based on the actual risk models used
risk_score = 0
if age > 60:
    risk_score += 1
if sex == 'Male':
    risk_score += 1
if 'Diabetes' in comorbidities:
    risk_score += 1
if 'Hypertension' in comorbidities:
    risk_score += 1
if 'Cardiovascular Disease' in comorbidities:
    risk_score += 2

# Displaying the risk score
st.write(f'Calculated Risk Score: {risk_score}')

if st.button('Submit'):
    st.success('Risk assessment submitted!')
