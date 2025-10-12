"""
Skin Cancer Detection Web App using Streamlit
Run with: streamlit run app.py
"""

import streamlit as st
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Skin Cancer Detection",
    page_icon="🔬",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Class names
CLASS_NAMES = [
    'Actinic keratoses',
    'Basal cell carcinoma',
    'Benign keratosis',
    'Dermatofibroma',
    'Melanoma',
    'Melanocytic nevi',
    'Vascular lesions'
]

# Risk information
RISK_INFO = {
    'Melanoma': {'level': 'HIGH', 'color': '#dc3545'},
    'Basal cell carcinoma': {'level': 'HIGH', 'color': '#dc3545'},
    'Actinic keratoses': {'level': 'MODERATE', 'color': '#ffc107'},
    'Dermatofibroma': {'level': 'MODERATE', 'color': '#ffc107'},
    'Benign keratosis': {'level': 'LOW', 'color': '#28a745'},
    'Melanocytic nevi': {'level': 'LOW', 'color': '#28a745'},
    'Vascular lesions': {'level': 'LOW', 'color': '#28a745'}
}

@st.cache_resource
def load_model(model_path='best_skin_cancer_model.h5'):
    """Load the trained model"""
    try:
        model = keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def preprocess_image(image, img_size=(224, 224)):
    """Preprocess uploaded image"""
    img = image.convert('RGB')
    img = img.resize(img_size)
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict(model, image):
    """Make prediction on image"""
    img_array = preprocess_image(image)
    predictions = model.predict(img_array, verbose=0)
    return predictions[0]

def create_probability_chart(predictions, class_names):
    """Create interactive bar chart of predictions"""
    fig = go.Figure(data=[
        go.Bar(
            y=class_names,
            x=predictions * 100,
            orientation='h',
            marker=dict(
                color=['#dc3545' if p == max(predictions) else '#4CAF50' for p in predictions],
                line=dict(color='white', width=2)
            ),
            text=[f'{p*100:.1f}%' for p in predictions],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title='Prediction Probabilities',
        xaxis_title='Confidence (%)',
        yaxis_title='Diagnosis',
        height=400,
        xaxis=dict(range=[0, 100]),
        showlegend=False
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🔬 Skin Lesion Analyzer</h1>', unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
    ⚠️ **IMPORTANT MEDICAL DISCLAIMER**

    This AI model is for **educational and demonstration purposes ONLY**.

    **DO NOT use this tool for:**
    - ❌ Actual medical diagnosis
    - ❌ Self-diagnosis or self-treatment
    - ❌ Delaying professional medical consultation

    **ALWAYS consult a qualified healthcare provider** for proper medical evaluation, diagnosis, and treatment of any skin concerns.
""")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 About")
        st.write("""
        This application uses deep learning to analyze skin lesions and provide preliminary classifications.
        
        **Supported Classifications:**
        - Melanoma
        - Basal Cell Carcinoma
        - Melanocytic Nevi
        - And 4 more types
        """)
        
        st.header("📖 How to Use")
        st.write("""
        1. Upload a clear image of the skin lesion
        2. Ensure good lighting and focus
        3. Review the AI analysis
        4. Consult a dermatologist for diagnosis
        """)
        
        st.header("⚙️ Model Info")
        model_path = st.text_input("Model Path", "best_skin_cancer_model.h5")
    
    # Load model
    model = load_model(model_path)
    
    if model is None:
        st.error("❌ Failed to load model. Please check the model path.")
        return
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose a skin lesion image...",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear image of the skin lesion"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_container_width=True)
            
            # Predict button
            if st.button('🔍 Analyze Image', type='primary', use_container_width=True):
                with st.spinner('Analyzing image...'):
                    predictions = predict(model, image)
                    st.session_state.predictions = predictions
                    st.session_state.analyzed = True
    
    with col2:
        st.header("📊 Analysis Results")
        
        if 'analyzed' in st.session_state and st.session_state.analyzed:
            predictions = st.session_state.predictions
            predicted_idx = np.argmax(predictions)
            predicted_class = CLASS_NAMES[predicted_idx]
            confidence = predictions[predicted_idx] * 100
            
            # Display prediction
            risk_info = RISK_INFO.get(predicted_class, {'level': 'UNKNOWN', 'color': '#6c757d'})
            
            st.markdown(f"""
                <div style='padding: 1.5rem; background-color: {risk_info['color']}20; 
                border-left: 5px solid {risk_info['color']}; border-radius: 5px;'>
                    <h3 style='margin: 0; color: {risk_info['color']};'>
                        Predicted Diagnosis
                    </h3>
                    <h2 style='margin: 0.5rem 0;'>{predicted_class}</h2>
                    <p style='margin: 0; font-size: 1.2rem;'>
                        Confidence: <strong>{confidence:.2f}%</strong>
                    </p>
                    <p style='margin: 0.5rem 0 0 0;'>
                        Risk Level: <strong>{risk_info['level']}</strong>
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Top 3 predictions
            st.subheader("🏆 Top 3 Predictions")
            top_3_idx = np.argsort(predictions)[-3:][::-1]
            
            for i, idx in enumerate(top_3_idx, 1):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.write(f"**{i}. {CLASS_NAMES[idx]}**")
                with col_b:
                    st.write(f"{predictions[idx]*100:.2f}%")
            
            # Probability chart
            st.plotly_chart(
                create_probability_chart(predictions, CLASS_NAMES),
                use_container_width=True
            )
            
            # Recommendations
            st.subheader("💡 Recommendations")
            if risk_info['level'] == 'HIGH':
                st.error("""
                    **Urgent Action Required:**
                    - Consult a dermatologist immediately
                    - Do not delay seeking professional medical advice
                    - Early detection significantly improves treatment outcomes
                """)
            elif risk_info['level'] == 'MODERATE':
                st.warning("""
                    **Medical Consultation Advised:**
                    - Schedule an appointment with a dermatologist
                    - Monitor the lesion for any changes
                    - Take photos to track progression
                """)
            else:
                st.info("""
                    **General Monitoring:**
                    - Continue to monitor the lesion
                    - Consult a doctor if you notice changes
                    - Perform regular self-examinations
                """)
            
            # Download results
            if st.button("📥 Download Report"):
                report = f"""
SKIN LESION ANALYSIS REPORT
{'='*50}

Predicted Diagnosis: {predicted_class}
Confidence: {confidence:.2f}%
Risk Level: {risk_info['level']}

Top 3 Predictions:
"""
                for i, idx in enumerate(top_3_idx, 1):
                    report += f"{i}. {CLASS_NAMES[idx]}: {predictions[idx]*100:.2f}%\n"
                
                st.download_button(
                    label="Download Report",
                    data=report,
                    file_name="skin_lesion_report.txt",
                    mime="text/plain"
                )
        else:
            st.info("👈 Upload an image and click 'Analyze Image' to see results")
    
    # Additional information
    with st.expander("ℹ️ About Skin Cancer Types"):
        st.write("""
        **Melanoma:** The most serious type of skin cancer. Requires immediate medical attention.
        
        **Basal Cell Carcinoma:** The most common type of skin cancer. Usually slow-growing.
        
        **Benign Keratosis:** Non-cancerous skin growth. Generally harmless.
        
        **Melanocytic Nevi:** Common moles. Usually benign but should be monitored.
        
        **Actinic Keratoses:** Pre-cancerous spots. Should be evaluated by a dermatologist.
        
        **Dermatofibroma:** Benign skin nodule. Usually harmless.
        
        **Vascular Lesions:** Lesions involving blood vessels. Usually benign.
        """)

if __name__ == "__main__":
    main()