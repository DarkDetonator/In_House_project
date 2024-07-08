from flask import Flask, request, jsonify, render_template, session, redirect
from nltk.corpus import wordnet

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed to use session

def get_word_info(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return None
    
    # Get the first synset
    synset = synsets[0]
    meaning = synset.definition()
    examples = synset.examples()
    
    return {
        "meaning": meaning,
        "examples": examples
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/modules')
def modules():
    return render_template('modules.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('word').lower()

    if user_input == "navigate home":
        return jsonify({'action': 'navigate', 'url': 'http://127.0.0.1:5001/'})
    elif user_input == "navigate modules":
        return jsonify({'action': 'navigate', 'url': 'http://127.0.0.1:5001/modules'})
    
    word_info = get_word_info(user_input)
    if word_info:
        session['state'] = {
            'word': user_input,
            'meaning': word_info['meaning'],
            'examples': word_info['examples'],
            'example_index': 0
        }
        response = f"Meaning: {word_info['meaning']}"
    else:
        response = "Sorry, I don't know the meaning of that word."

    return jsonify({'response': response})

@app.route('/example', methods=['POST'])
def example():
    if 'state' in session:
        word = session['state']['word']
        examples = session['state']['examples']
        example_index = session['state']['example_index']

        if example_index < len(examples):
            response = f"Example {example_index + 1}: {examples[example_index]}"
            session['state']['example_index'] += 1
        else:
            response = "No more examples available."
    else:
        response = "Please ask for a word meaning first."

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(port=5003, debug=True)
