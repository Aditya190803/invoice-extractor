import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import csv
import PyPDF2
from io import BytesIO
import base64  # For encoding PDF to base64

# Configure the API key
os.getenv("GOOGLE_API_KEY")
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

# Function to embed PDF in Streamlit sidebar
def embed_pdf_in_sidebar(file_path):
    with open(file_path, "rb") as file:
        base64_pdf = base64.b64encode(file.read()).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" style="border:none;"></iframe>'
    st.sidebar.markdown(pdf_display, unsafe_allow_html=True)

# Initialize the Streamlit app
st.set_page_config(page_title="Invoice Extractor", layout="wide")

# Sidebar for example files
st.sidebar.title("Test the App")
st.sidebar.write("Use the example files below to test the app.")

# Example files
example_files = {
    "Example Invoice Image": "example_invoice.jpg",
    "Example Invoice PDF": "example_invoice.pdf",
}

# Display example files in the sidebar
selected_file = None
for file_name, file_path in example_files.items():
    st.sidebar.write(f"**{file_name}**")
    
    if file_path.endswith(('.jpg', '.jpeg', '.png')):
        # Display the image in the sidebar
        image = Image.open(file_path)
        st.sidebar.image(image, caption=file_name, use_container_width=True)
    elif file_path.endswith('.pdf'):
        # Embed the PDF in the sidebar
        st.sidebar.write("**PDF Preview:**")
        embed_pdf_in_sidebar(file_path)
    
    # Add a button to use the file as input
    if st.sidebar.button(f"Use {file_name}"):
        selected_file = file_path

# Initialize session state
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "response" not in st.session_state:
    st.session_state.response = None

# If an example file is selected, load it
if selected_file:
    with open(selected_file, "rb") as file:
        st.session_state.uploaded_file = BytesIO(file.read())
        st.session_state.uploaded_file.name = selected_file  # Set the file name for type detection

# Main app
st.title("Invoice Extractor")

uploaded_file = st.file_uploader("Or choose your own invoice image or PDF...", type=["jpg", "jpeg", "png", "pdf"])

# If a file is uploaded manually, override the example file
if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images or PDFs as invoices &
               you will have to extract all the data from the invoice.
               """

if st.session_state.uploaded_file is not None:
    if st.session_state.uploaded_file.name.endswith(('.jpg', '.jpeg', '.png')):
        image = Image.open(st.session_state.uploaded_file)
        st.image(image, caption="Uploaded Image.", use_container_width=True)
    elif st.session_state.uploaded_file.name.endswith('.pdf'):
        st.write("PDF file uploaded.")

    if st.button("Extract Data"):
        if st.session_state.uploaded_file.name.endswith(('.jpg', '.jpeg', '.png')):
            image_data = input_image_setup(st.session_state.uploaded_file)
            st.session_state.response = get_gemini_response(input_prompt, image=image_data)
        elif st.session_state.uploaded_file.name.endswith('.pdf'):
            pdf_text = extract_text_from_pdf(st.session_state.uploaded_file)
            st.session_state.response = get_gemini_response(input_prompt, pdf_text=pdf_text)

if st.session_state.response:
    st.subheader("Extracted Data")
    st.write(st.session_state.response)

    # Save the extracted data to a CSV file
    csv_filename = "invoice_data.csv"
    save_to_csv(st.session_state.response, csv_filename)
    st.success("Data saved to invoice_data.csv")

    # Add a download button for the CSV file
    with open(csv_filename, "rb") as file:
        btn = st.download_button(
            label="Download CSV",
            data=file,
            file_name=csv_filename,
            mime="text/csv",
        )