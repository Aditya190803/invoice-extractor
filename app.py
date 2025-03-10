import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import csv
import PyPDF2
from io import BytesIO

# Configure the API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Function to load Gemini model and get responses
def get_gemini_response(input, image=None, pdf_text=None):
    model = genai.GenerativeModel('gemini-2.0-flash')
    if image:
        response = model.generate_content([input, image[0]])
    elif pdf_text:
        response = model.generate_content([input, pdf_text])
    return response.text

# Function to setup the image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to save data to CSV
def save_to_csv(data, filename="invoice_data.csv"):
    # Assuming the data is a string that can be split into lines and then into key-value pairs
    lines = data.split('\n')
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for line in lines:
            if ': ' in line:
                key, value = line.split(': ', 1)
                writer.writerow([key, value])

# Initialize the Streamlit app
st.set_page_config(page_title="Invoice Extractor")

uploaded_file = st.file_uploader("Choose an invoice image or PDF...", type=["jpg", "jpeg", "png", "pdf"])
input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images or PDFs as invoices &
               you will have to extract all the data from the invoice.
               """

if uploaded_file is not None:
    if uploaded_file.type.startswith('image'):
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_container_width=True)
    elif uploaded_file.type == "application/pdf":
        st.write("PDF file uploaded.")

    if st.button("Extract Data"):
        if uploaded_file.type.startswith('image'):
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image=image_data)
        elif uploaded_file.type == "application/pdf":
            pdf_text = extract_text_from_pdf(uploaded_file)
            response = get_gemini_response(input_prompt, pdf_text=pdf_text)

        st.subheader("Extracted Data")
        st.write(response)

        # Save the extracted data to a CSV file
        csv_filename = "invoice_data.csv"
        save_to_csv(response, csv_filename)
        st.success("Data saved to invoice_data.csv")

        # Add a download button for the CSV file
        with open(csv_filename, "rb") as file:
            btn = st.download_button(
                label="Download CSV",
                data=file,
                file_name=csv_filename,
                mime="text/csv",
            )