from dotenv import load_dotenv
import os, re
import google.generativeai as genai

def setup_model():
    load_dotenv()
    genai.configure(api_key=os.getenv("API_KEY"))

    # Set up the model
    generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048,}

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    return genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config, safety_settings=safety_settings)

def process_file(model, input_file, output_folder):
    print(f"Processing '{input_file}'")

    instructions = """Given a research paper's text data, your task is to preprocess the content by removing extraneous details
      such as email addresses, references, trademarks, researcher names, mathematical equations,and any other non-technical content.
        The resulting response should contain only the text of research paper. The Content of research paper is given below:\n"""

    # Read content from input file
    with open(input_file, 'r') as f:
        content = f.read()

    prompt = instructions + content
    
    try:
        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        response = convo.last.text

        output_file_path = os.path.join(output_folder, os.path.splitext(os.path.basename(input_file))[0] + '.txt')

        with open(output_file_path, 'w') as f:
            f.write(response)
        print(f"Processed '{input_file}' and saved response to '{output_file_path}'")

    except Exception as e:
        print(f"Failed to process '{input_file}' due to {e}")


if __name__ == "__main__":
    model = setup_model()

    input_folder = "../datasets/"
    output_folder = "../datasets/preprocessed_data"

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each text file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_folder, filename)
            process_file(model, input_file_path, output_folder)