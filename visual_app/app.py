from flask import Flask, render_template, request, jsonify, redirect, session
from flask_cors import CORS
import threading
import logging
import pyttsx3

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5000"], methods=["GET", "POST", "PUT", "DELETE"], headers=["Content-Type", "Authorization"])
app.secret_key = 'f6b0a04c5fa0f6043e9d37f871a64c020ce9e3769cc12c1e'

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine_lock = threading.Lock()

logging.basicConfig(level=logging.DEBUG)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('website_version', None)
    return redirect('http://127.0.0.1:5000/login')

def speak(text):
    with engine_lock:
        engine.say(text)
        engine.runAndWait()

quiz_questions = [
    {
        'question': 'What is the color of the sky?',
        'options': ['blue', 'green', 'red', 'yellow'],
        'answer': 'blue'
    },
    {
        'question': 'What is 2 + 2?',
        'options': ['3', '4', '5', '6'],
        'answer': '4'
    },
    {
        'question': 'What is the capital of France?',
        'options': ['Berlin', 'Madrid', 'Paris', 'Rome'],
        'answer': 'Paris'
    }
]

current_question_index = 0
correct_answers_count = 0
module_completed = False
quiz_active = False  # Track if the quiz is active

def normalize_answer(answer):
    answer = answer.lower().strip()
    if answer in ['4', 'four']:
        return '4'
    return answer

def is_correct_answer(user_answer, correct_answer):
    normalized_user_answer = normalize_answer(user_answer)
    normalized_correct_answer = normalize_answer(correct_answer)
    return normalized_correct_answer in normalized_user_answer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')  # Update this route
def contact():
    return redirect('http://127.0.0.1:5003')  # Redirect to the chatbot Flask app

@app.route('/modules')
def modules():
    return render_template('modules.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/command', methods=['POST'])
def command():
    global current_question_index, correct_answers_count, module_completed, quiz_active
    try:
        data = request.get_json()
        command = data['command']
        page = data.get('page', '')  # Get the page parameter
        logging.debug(f"Received command: {command} on page: {page}")

        if 'home' in command:
            return jsonify({'action': 'navigate', 'url': '/'})
        elif 'about' in command:
            return jsonify({'action': 'navigate', 'url': '/about'})
        elif 'contact' in command:
            return jsonify({'action': 'navigate', 'url': '/contact'})  # Navigate to the chatbot page
        elif 'modules' in command:
            return jsonify({'action': 'navigate', 'url': '/modules'})
        elif 'refresh' in command:
            return jsonify({'action': 'refresh'})
        elif page == 'modules' and 'start' in command:
            logging.debug("Starting audio")
            return jsonify({'action': 'audioControl', 'command': 'start'})
        elif page == 'modules' and 'pause' in command:
            logging.debug("Pausing audio")
            return jsonify({'action': 'audioControl', 'command': 'pause'})
        elif page == 'modules' and 'audio ended' in command:
            logging.debug("Audio ended, navigate to quiz")
            speak('The module audio has ended. Say "quiz" to start the quiz.')
            return jsonify({'action': 'navigate', 'url': '/quiz'})
        elif page == 'modules' and 'quiz' in command:
            logging.debug("Navigating to quiz page")
            return jsonify({'action': 'navigate', 'url': '/quiz'})
        elif page == 'modules' and 'complete module' in command:
            logging.debug("Manually marking module as completed")
            module_completed = True
            speak('Module 1 has been manually marked as completed.')
            return jsonify({'action': 'response', 'message': 'Module 1 has been manually marked as completed.'})
        elif page == 'modules' and 'status' in command:
            if module_completed:
                return jsonify({'action': 'response', 'message': 'Module 1 is already completed.'})
            else:
                return jsonify({'action': 'response', 'message': 'Module 1 is not yet completed.'})
        elif page == 'quiz':
            if 'start quiz' in command:
                logging.debug("Starting quiz")
                correct_answers_count = 0
                current_question_index = 0  # Reset quiz to the first question
                quiz_active = True
                question = quiz_questions[current_question_index]
                speak(question['question'] + '. Options are ' + ', '.join(question['options']))
                return jsonify({'action': 'quizQuestion', 'question': question['question'], 'options': ', '.join(question['options'])})
            elif quiz_active:
                question = quiz_questions[current_question_index]
                if 'next' in command:
                    current_question_index += 1
                    if current_question_index < len(quiz_questions):
                        question = quiz_questions[current_question_index]
                        speak(question['question'] + '. Options are ' + ', '.join(question['options']))
                        return jsonify({'action': 'quizQuestion', 'question': question['question'], 'options': ', '.join(question['options'])})
                    else:
                        quiz_active = False
                        score_message = f'You have completed the quiz with a score of {correct_answers_count} out of {len(quiz_questions)}.'
                        speak(score_message)
                        return jsonify({'action': 'quizCompleted', 'scoreMessage': score_message})
                elif is_correct_answer(command, question['answer']):
                    correct_answers_count += 1
                    speak('Correct answer.')
                    playFeedback(True)
                    return jsonify({'action': 'quizFeedback', 'correct': True, 'moduleCompleted': False})
                else:
                    speak('Incorrect answer. Please try again.')
                    playFeedback(False)
                    return jsonify({'action': 'quizFeedback', 'correct': False, 'moduleCompleted': False})
            else:
                return jsonify({'action': 'response', 'message': 'The quiz is not active.'})

        logging.debug("Command not recognized or page not specified.")
        return jsonify({'action': 'response', 'message': 'Command not recognized.'})
    except Exception as e:
        logging.error(f"Error processing command: {e}")
        return jsonify({'action': 'response', 'message': 'An error occurred while processing the command.'})


if __name__ == '__main__':
    app.run(port=5001, debug=True)
