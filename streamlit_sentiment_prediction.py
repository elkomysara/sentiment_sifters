import mlflow.pyfunc
import streamlit as st
import pandas as pd

# Load the model from the MLflow model registry or from a specific path

import mlflow.pyfunc

# Load the model from the MLflow registry




# Title of the Streamlit App
st.markdown("<h1 style='text-align: center;text-decoration: underline;color:GoldenRod'>Sentiment Prediction </h1>", unsafe_allow_html=True)



import mlflow

client = mlflow.tracking.MlflowClient()

def model_name():
    name = None  # Initialize the variable
    for rm in client.search_registered_models():
        name = rm.name
    return name

model_name = model_name()  # Replace with your actual model name
if model_name:
    latest_version = client.get_latest_versions(model_name, stages=["None"])[0].version
    model_uri = f"models:/{model_name}/{latest_version}"
    model = mlflow.pyfunc.load_model(model_uri)
else:
    print("No registered models found.")



# Step 1: Choose Input Mode
input_mode = st.radio(
    "Choose your input mode:",
    ("CSV File", "Single Review Form", "Both")
)

# Step 2: Conditional Input based on selected mode
if input_mode == "CSV File" or input_mode == "Both":
    st.header("Upload CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Load and display the CSV file
        data = pd.read_csv(uploaded_file)
        st.write("Preview of the uploaded file:")
        st.dataframe(data.head())
        
        # Predict if CSV file is uploaded
        if st.button("Predict Sentiment for CSV"):
            try:
                predictions = model.predict(data)  # Assuming 'data' has a column compatible with the model
                data["Predicted Sentiment"] = predictions
                st.write("Prediction Results:")
                st.dataframe(data)
            except Exception as e:
                st.error(f"An error occurred while predicting sentiments: {e}")

# Step 3: Single Review Form Input
if input_mode == "Single Review Form" or input_mode == "Both":
    st.header("Single Review Form")
    with st.form("single_review_form"):
        review_text = st.text_area("Enter a single review text:", placeholder="Enter the review text here")
        submit_button = st.form_submit_button("Predict Sentiment for Single Review")
    
    # Predict for single review if form is submitted
    if submit_button and review_text:
        try:
            input_data = pd.DataFrame({"review_text": [review_text]})
            prediction = model.predict(input_data)
            st.write("Predicted Sentiment for Single Review:")
            st.success(prediction[0])
        except Exception as e:
            st.error(f"An error occurred while predicting sentiment: {e}")