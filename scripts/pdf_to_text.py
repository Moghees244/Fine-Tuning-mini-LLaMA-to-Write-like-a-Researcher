import os
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Provide the folder path containing the PDF files
pdf_folder = "../dataset/pdfs"

# List PDF files in the folder
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

# Process one PDF at a time
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_folder, pdf_file)
    
    # Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Create a file name for the text file
    text_file = os.path.splitext(pdf_file)[0] + ".txt"
    
    # Write the text to a file with the same name as the PDF
    with open(text_file, "w", encoding="utf-8") as file:
        file.write(text)

    print(f"Text extracted from {pdf_file} and saved into {text_file}")
