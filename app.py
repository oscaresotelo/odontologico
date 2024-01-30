import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import numpy as np






# Fetching the API key from the environment variable
# api_key = os.environ.get('GOOGLE_API_KEY')
api_key = 'AIzaSyABFNeXQMQNy-MFlPf9818zmFn5wnuFZHc'
if api_key is None:
    raise ValueError("GOOGLE_API_KEY environment variable is not set. Please set it before running the script.")

# Configuring the GenerativeAI API with the obtained API key
genai.configure(api_key=api_key)

# Creating a GenerativeModel instance
model = genai.GenerativeModel('gemini-pro-vision')

# Function to generate content based on input image and optional prompt
def generate_content(image, prompt=None):
    # Convert Streamlit Image to PIL Image
    if isinstance(image, np.ndarray):
        image_pil = Image.fromarray(image)
    else:
        image_pil = Image.open(image)

    if prompt:
        # Generating content using the model with prompt
        response = model.generate_content([prompt, image_pil])
        response.resolve()

        # Extracting the generated text
        generated_text = response.text.strip()
    else:
        # If no prompt is provided, generate content without prompt
        response = model.generate_content([image_pil])
        response.resolve()

        # Extracting the generated text
        generated_text = response.text.strip()

    return generated_text

# Streamlit Interface with enhanced styling
st.set_page_config(
    page_title="Interpretacion de Imagenes",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
                     .container {
                display: flex;
            }
            .logo-text {
                font-weight:700 !important;
                font-size:30px !important;
                color: black !important;
                padding-top: 50px !important;
            }
            .logo-img {
                float:right;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("estilos.css")
# Sidebar with app information
st.sidebar.title("Acerca")
st.sidebar.info(
    "Esta aplicación utiliza IA para realizar diagnostico, "
)
st.title("Ai-Cito Diagnostico")
# Upload image from the user
uploaded_image = st.file_uploader("Subir una Imagen", type=["jpg", "png", "jpeg"])

# Display the uploaded image with reduced size
if uploaded_image is not None:
    # Resize the image for display
    img = Image.open(uploaded_image)
    resized_img = img.resize((400, 400))

    st.image(resized_img, caption="Imagen Subida", use_column_width=True)

    # Allow the user to enter a prompt
    # prompt = st.text_input("Introduzca un mensaje (opcional)", "")
    prompt = 'Eres un experimentado Odontologo, diagnosticar en lo que se observa solo en la imagen, y sugerir el posible tratamiento relacionado solo a la imagen , y en el caso de necesitar medicamentos , especificar cuales, especificar el numero correcto de piezas dentaria afectada'
    # Submit button to trigger content generation
    if st.button("Generar Diagnostico", key="generate_button"):
        # Add a loading spinner while processing
        with st.spinner("Generando Contenido..."):
            # Process the image and generate content
            generated_text = generate_content(uploaded_image, prompt)

        # Display the generated text with a success message
        st.success("Contenido Generado Exitosamente!")
        st.text("Texto Generado:")
        st.write(generated_text)