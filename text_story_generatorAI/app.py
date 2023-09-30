from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = 'YOUR_API_KEY'

# Create a function for story generation
def generate_story(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_prompt = request.form['user_prompt']
    story = generate_story(user_prompt)
    return render_template('index.html', user_prompt=user_prompt, story=story)

if __name__ == '__main__':
    app.run(debug=True)
