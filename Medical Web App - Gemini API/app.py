#Author: Duong Phu Dong
#Medical Web App - Gemini API Key
#Language: Python
#Status: Testing

#import necessary modules
import streamlit as st # type: ignore
from pathlib import Path
import google.generativeai as genai # type: ignore

from api_key import api_key

# config genai with api key
genai.configure(api_key=api_key)

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Setup safety setting
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

system_prompts = [
    """
    You are a domain expert in medical image analysis. You are tasked with 
    examining medical images for a renowned hospital.
    Your expertise will help in identifying or 
    discovering any anomalies, diseases, conditions or
    any health issues that might be present in the image.
    
    Your key responsibilites:
    1. Detailed Analysis : Scrutinize and thoroughly examine each image, 
    focusing on finding any abnormalities.
    2. Analysis Report : Document all the findings and 
    clearly articulate them in a structured format.
    3. Recommendations : Basis the analysis, suggest remedies, 
    tests or treatments as applicable.
    4. Treatments : If applicable, lay out detailed treatments 
    which can help in faster recovery.
    
    Important Notes to remember:
    1. Scope of response : Only respond if the image pertains to 
    human health issues.
    2. Clarity of image : In case the image is unclear, 
    note that certain aspects are 
    'Unable to be correctly determined based on the uploaded image'
    3. Disclaimer : Accompany your analysis with the disclaimer: 
    "Consult with a Doctor before making any decisions."
    4. Your insights are invaluable in guiding clinical decisions. 
    Please proceed with the analysis, adhering to the 
    structured approach outlined above.
    
    Please provide the final response with these 4 headings : 
    Detailed Analysis, Analysis Report, Recommendations and Treatments
    
"""
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

#set the page configuration

st.set_page_config(page_title="Insight Circle Analytics", page_icon=":robot:")

#set web title

st.title("Insight Circle Community.png", width=150)

#set the title
st.title("Insight Circle Image Analytics")

#set the subtitle
st.subheader("An application help all users to identify medical images")
uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg", "jpeg"])

submit_button = st.button("Generate the Analysis")

if submit_button:
    #process the uploaded image
    image_data = uploaded_file.getvalue()
    
    image_parts = [
        {
            "mime_type" : "image/jpg",
            "data" : image_data
        }
    ]

    #making our prompt ready
    prompt_parts = [
    image_parts[0],
    system_prompts[0],
    ]

    #generate response
    response = model.generate_content(prompt_parts)
    if response:
        st.title('Detailed analysis based on the uploaded image')
        st.write(response.text)
