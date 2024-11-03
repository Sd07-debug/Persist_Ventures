from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Set up your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Store user insights
insights = {
    'symptoms': [],
    'interests': []
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    # Capture user insights
    if "symptom" in user_message.lower():
        insights['symptoms'].append(user_message)
    elif "interest" in user_message.lower():
        insights['interests'].append(user_message)

    # Handle specific inquiries
    if "health" in user_message.lower():
        response = "Can you describe your symptoms?"
    elif "product" in user_message.lower():
        response = "What type of products are you interested in?"
    else:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": user_message}]
        )
        response = response.choices[0].message['content']

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
    
