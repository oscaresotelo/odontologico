### Health Management APP


import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key= "AIzaSyABFNeXQMQNy-MFlPf9818zmFn5wnuFZHc")
generation_config = {
    "temperature": 0.4,
     "top_p": 1,
     "top_k": 5,
"max_output_tokens": 4096,
}
## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt], generation_config = generation_config)
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="App Salud")
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
st.title("Diagnostico Por Imagen")
# input=st.text_input("Ingrese: ",key="input")
input = ""
uploaded_file = st.file_uploader("Eliga Una Imagen...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen Subida.", use_column_width=True)


submit=st.button("Total de Calorias")

# input_prompt="""
# Eres un experto nutricionista, no seras creativo en la respuesta y analizaras CUIDADOSAMENTE los  alimentos de la imagen, Importate limitarse solo a los alimentos de la imagen,
#              deberas calcular el peso total de cada alimento de la imagen, tambien deberas contar correctamente la cantidad de alimentos, deberas calcular las calorias por cada alimento segun el peso de forma correcta, 
             
#                el formato que con el que mostraras la informacion sera el siguiente: 

#                1. Ítem 1 - número de calorías
#                2. Ítem 2 - número de calorías
#                ----
#                ----
#                importante que lo muestres en ese formato, solo deberas analizar y hacer unicamente referencia a los alimentos de la imagen, no seras creativo en la respueta,
#             Tambien deberas generar una rutina de ejercicios para perder las calorias consumidas
# """
input_prompt = """ realizar diagnostico de la imagen , especificar cuantos dientes estan afectados y nombrarlos y recomendar un tratamiento, usar el sistema de numeracion FDI
"""
## If submit button is clicked

if submit:
    with st.spinner("Diagnosticando....."):
        image_data=input_image_setup(uploaded_file)
        response=get_gemini_repsonse(input_prompt,image_data,input)
        st.subheader("Resultado:")
        st.write(response)

