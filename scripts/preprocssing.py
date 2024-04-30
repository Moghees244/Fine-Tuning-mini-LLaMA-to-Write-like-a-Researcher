import pandas as pd
import os, re
import google.generativeai as genai

prompts = """Given the following tweet, assign a sentiment label from the provided categories: 'Positive', 'Extremely Positive', 'Negative',
          or 'Extremely Negative'. You can use your general knowledge and intuition to make your decision. Your response should reflect 
          the predominant sentiment expressed in the tweet. Additionally, provide a brief reason explaining your choice. Format: Label,reason 
          Tweet: """

def setup_model():
    genai.configure(api_key=)

    # Set up the model
    generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048,}

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    return genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config, safety_settings=safety_settings)

def get_label(prompt_type, tweet, model):
    prompt = prompts.get(prompt_type, prompts["zero_shot"]) + tweet
    convo = model.start_chat(history=[])

    convo.send_message(prompt)
    return convo.last.text

def response_parser(response):
    lines = response.strip().split(',')

    label = lines[0].replace('*', '').replace('\'', '').replace('.', '')
    return label, ' '.join(lines[1:]).strip()


if __name__ == "__main__":
    Data = pd.read_csv("Dataset.csv")

    model = setup_model()

    for index, row in Data.iterrows():
        original_tweet = row['OriginalTweet']
        label, reason = response_parser(get_label(2,original_tweet, model))
        print("Label : ", label)
        print("Reason : ", reason)

        df = pd.DataFrame([[original_tweet, "Few Shots", label, reason]], columns=['Tweet', 'Prompt Type', 'Annotation', 'Reason'])
        with open("zero_shot.csv", mode='a', newline='', encoding='utf-8') as file:
            df.to_csv(file, header=not file.tell(), index=False)