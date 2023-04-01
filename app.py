from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import openai
import os
from flask_cors import CORS



pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
openai.api_key = os.getenv("OPENAI_API_KEY", "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")
app = Flask(__name__)
CORS(app)

def generate_response(extracted_text, prompt):
    full_prompt = f"{extracted_text} {prompt}"
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=full_prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

@app.route('/ocr', methods=['POST'])
def ocr():
    file = request.files['image']
    img = Image.open(file.stream)
    extracted_text = pytesseract.image_to_string(img)
    
    prompt = "Can you paraphrase this in a way that is organized, and easy to understand, while mantaining all of the meaning and most of the same wording?"
    # gpt_response = generate_response(extracted_text, prompt)

    return jsonify({'extracted_text': extracted_text})

if __name__ == '__main__':
    app.run()
