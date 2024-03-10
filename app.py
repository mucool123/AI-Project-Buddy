from flask import Flask, request, render_template, redirect, url_for
import pytesseract
from PIL import Image
import io
import openai

app = Flask(__name__)
openai.api_key = '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'

@app.route('/', methods=['GET'])
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file:
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        extracted_text = pytesseract.image_to_string(image)
        explanation, prompts = generate_explanation_and_prompts(extracted_text)
        return render_template('explanation.html', explanation=explanation, prompts=prompts)

def generate_explanation_and_prompts(text):
    # Start a chat session with the model
    chat_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the appropriate chat model
        messages=[
            {"role": "system", "content": "You are a helpful assistant that explains text in simple terms and provides examples. Also reply in the language in which input is given to you."},
            {"role": "user", "content": f"{text}"},
        ],
    )
    
    # Extract the model's response
    explanation = chat_response['choices'][0]['message']['content']
    
    # Generate follow-up prompts (if necessary, you can send additional messages in the chat to do this)
    prompts = [
        "Explain this in details.",
        "Why is this important and its applications?",
        "How does this apply in real-world scenarios?"
    ]  # This is an example; you may need to adjust based on your application's needs
    
    return explanation, prompts


@app.route('/handle_prompt', methods=['POST'])
def handle_prompt():
    user_prompt = request.form['prompt']
    # Assuming you want to continue the chat based on the original explanation
    # You might need to store the original chat session's ID or context if you want a continuous conversation
    chat_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_prompt},
        ],
    )
    response_text = chat_response['choices'][0]['message']['content']
    return render_template('prompt_response.html', response=response_text)


if __name__ == '__main__':
    app.run(debug=True)
