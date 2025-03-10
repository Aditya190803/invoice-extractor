# Invoice Extractor App

This is a Streamlit-based web application that extracts data from invoice images or PDFs using Google's Gemini AI model. The extracted data is saved as a CSV file, which can be downloaded directly from the app.

## Features
- **Image and PDF Support**: Upload invoice images (JPG, JPEG, PNG) or PDFs to extract data.
- **AI-Powered Extraction**: Uses Google's Gemini AI model to accurately extract invoice data.
- **CSV Export**: Extracted data is saved as a CSV file, which can be downloaded with a single click.
- **User-Friendly Interface**: Simple and intuitive interface powered by Streamlit.

## Prerequisites
Before running the app, ensure you have the following:
- Python 3.11 or higher
- A Google API key for Gemini AI (set as an environment variable or in Streamlit secrets)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/aditya190803/invoice-extractor.git
   cd invoice-extractor
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google API key:
   - Create a `.streamlit/secrets.toml` file and add your API key:
     ```toml
     GEMINI_API_KEY = "your-gemini-api-key"
     ```
     Replace your_gemini_api_key with your actual GEMINI API key.
     Get your [API Key](https://aistudio.google.com/app/apikey) from here.
  
## Running the App
To run the app, use the following command:
```bash
streamlit run app.py
```

Once the app is running, open your browser and navigate to `http://localhost:8501`.

## How to Use
1. **Upload an Invoice**: Click the "Choose an invoice image or PDF..." button to upload an invoice file (supported formats: JPG, JPEG, PNG, PDF).
2. **Extract Data**: Click the "Extract Data" button to process the invoice and extract the data.
3. **View and Download**: The extracted data will be displayed on the screen. You can download the data as a CSV file by clicking the "Download CSV" button.

## Dependencies
- `streamlit`: For the web app interface.
- `Pillow`: For image processing.
- `google-generativeai`: For interacting with Google's Gemini AI model.
- `PyPDF2`: For extracting text from PDF files.
- `csv`: For saving extracted data to a CSV file.

