import re
import os

def remove_references(text):
    # Remove references like [1], [Author et al., 2020], etc.
    text = re.sub(r'\[\d+\]', '', text)  # Remove [1], [2], etc.
    text = re.sub(r'\[\w+\s*(?:et\s*al\.)?,?\s*\d+\]', '', text)  # Remove [Author et al., year]
    return text

def remove_equations(text):
    # Remove equations enclosed within $...$, $$...$$, or \(...\)
    text = re.sub(r'\$[^\$]*\$', '', text)  # Remove $...$
    text = re.sub(r'\$\$[^\$]*\$\$', '', text)  # Remove $$...$$
    text = re.sub(r'\\\([^\)]*\\\)', '', text)  # Remove \(...\)
    return text

def remove_links(text):
    # Remove links starting with http:// or https://
    text = re.sub(r'http[s]?://\S+', '', text)
    return text

def remove_emails(text):
    # Remove email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
    return text

# Read text from a text file
input_file = "2.txt"
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
