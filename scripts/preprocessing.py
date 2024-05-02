import re
import os

def remove_references(text):
    references_heading_index = text.find("references")
    # If the "References" heading is found, remove all text starting from that index
    if references_heading_index != -1:
        text = text[:references_heading_index]
    return text

def remove_equations(text):
    text = re.sub(r"\d+", "", text)
    text = re.sub(r'[^\w\s]', "", text)
    text = re.sub(r'\n+', '\n', text)
    return text

def remove_links(text):
    # Remove links starting with http:// or https://
    text = re.sub(r'http[s]?://\S+', '', text)
    return text

def remove_emails(text):
    # Remove email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
    return text

def clean_data(input_file):
    with open(input_file, "r", encoding="utf-8") as file:
        input_text = file.read()

    # Process the text
    processed_text = input_text.lower()  # Convert all letters to lowercase
    processed_text = remove_references(processed_text)
    processed_text = remove_equations(processed_text)
    processed_text = remove_links(processed_text)
    processed_text = remove_emails(processed_text)

    # Create a folder to save the preprocessed data if it doesn't exist
    output_folder = "../datasets/preprocessed_data"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the filename without extension
    filename_without_extension = os.path.splitext(os.path.basename(input_file))[0]

    # Write processed text to a new file in the folder with the same filename
    output_file = os.path.join(output_folder, filename_without_extension + "_preprocessed.txt")
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(processed_text)

    print("Preprocessed data saved to", output_file)

# Provide the folder path containing the PDF files
txt_folder = "../datasets/pdf_to_text"

# List PDF files in the folder
txt_files = [f for f in os.listdir(txt_folder) if f.endswith(".txt")]

# Process one PDF at a time
for txt_file in txt_files:
    txt_path = os.path.join(txt_folder, txt_file)
    text = clean_data(txt_path)