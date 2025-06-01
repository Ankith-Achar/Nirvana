from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
from datetime import timedelta
import asyncio
import logging
from chat import ChatManager
from phobia import PhobiaExplainer
from models import db, User, DiaryEntry
from signup import signup_bp
from admin import admin_bp
import diary
from response import calculate_score, get_diagnosis, get_remedies

# Initialize Flask app and logging
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# App configuration
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', os.urandom(24))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=7)

# Initialize database
db.init_app(app)

app.register_blueprint(signup_bp)
app.register_blueprint(admin_bp)

# Initialize chat manager and phobia explainer
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("No API key found. Please set GOOGLE_API_KEY in .env file")

chat_manager = ChatManager(api_key)
phobia_explainer = PhobiaExplainer()


# Auth Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session.permanent = True
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('home'))
        else:
            return render_template('auth/login.html', error='Invalid username or password')

    return render_template('auth/login.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/about')
def about():
    return render_template('auth/aboutus.html')

@app.route('/contact')
def contact():
    return render_template('auth/contactus.html')

# Chatbot Routes
@app.route('/chatbot')
def chatbot():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Initialize chat history in session if it doesn't exist
    if 'chat_history' not in session:
        session['chat_history'] = []
        session['chat_history'].append({
            "role": "assistant",
            "content": f"Hi {session['username']}! I'm Nova. I'm here to listen and support you. How are you feeling today?"
        })
        session.modified = True
    
    return render_template('chat.html', chat_history=session.get('chat_history', []))

@app.route('/send_message', methods=['POST'])
async def send_message():
    if 'user_id' not in session:
        return jsonify({'error': 'Please log in to continue'}), 401
    
    user_input = request.json.get('message', '')
    
    # Validate input
    is_valid, error_message = chat_manager.validate_input(user_input)
    if not is_valid:
        return jsonify({'error': error_message})
    
    # Initialize chat history if not present
    if 'chat_history' not in session:
        session['chat_history'] = []
        session['chat_history'].append({
            "role": "assistant",
            "content": f"Hi {session['username']}! I'm Nova. I'm here to listen and support you. How are you feeling today?"
        })
        session.modified = True
    
    # Add user message to chat history
    session['chat_history'].append({"role": "user", "content": user_input})
    session.modified = True  # Ensure session updates
    
    # Generate response
    response, response_time = await chat_manager.generate_response(
        user_input,
        session['chat_history']
    )
    
    # Add assistant's response to chat history
    session['chat_history'].append({"role": "assistant", "content": response})
    session.modified = True
    
    return jsonify({
        'response': response,
        'response_time': response_time
    })

@app.route('/typing_status', methods=['POST'])
def typing_status():
    if 'user_id' not in session:
        return jsonify({'error': 'Please log in to continue'}), 401
    
    status = request.json.get('typing', False)
    return jsonify({'status': 'ok'})

@app.route('/clear', methods=['POST'])
def clear_chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Only clear chat history, not the entire session
    session.pop('chat_history', None)
    return redirect(url_for('chatbot'))

# Phobia Routes
@app.route('/phobia')
def phobia():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('phobia.html', username=session['username'])

@app.route('/explain_fear', methods=['POST'])
def explain_fear():
    if 'user_id' not in session:
        return jsonify({'error': 'Please log in to continue'}), 401
    
    fear = request.json.get('fear', '')
    if not fear:
        return jsonify({'error': 'Please enter a fear to explain'}), 400
    
    try:
        logger.info(f"Processing request for fear: {fear}")
        explanation = phobia_explainer.get_explanation(fear)
        return jsonify({'explanation': explanation})
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': 'Failed to process the request. Please try again.'}), 500

# ----- DIARY ROUTES -----
@app.route('/diary')
def diary_home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    entries = diary.get_all_entries()
    return render_template('diary.html', entries=entries, is_search=False, username=session['username'])

@app.route('/diary/add', methods=['POST'])
def diary_add():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    title = request.form['title']
    content = request.form['content']
    diary.add_entry(title, content)
    return redirect(url_for('diary_home'))

@app.route('/diary/delete/<int:entry_id>')
def diary_delete(entry_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if diary.delete_entry(entry_id):
        flash('Entry deleted successfully', 'success')
    else:
        flash('Failed to delete entry', 'error')
    return redirect(url_for('diary_home'))

@app.route('/diary/search', methods=['GET'])
def diary_search():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    title = request.args.get('title', '')
    date = request.args.get('date', '')
    entries = diary.search_entries(title, date)
    return render_template('diary.html', entries=entries, is_search=True, username=session['username'])

# Questionnaire routes
@app.route('/test')
def test_home():
    """Home page that lists all questionnaire links"""
    questionnaires = [
        {'name': 'Depression', 'url': 'depression'},
        {'name': 'ADHD', 'url': 'adhd'},
        {'name': 'PTSD', 'url': 'ptsd'},
        {'name': 'Bipolar', 'url': 'bipolar'},
        {'name': 'Anxiety', 'url': 'anxiety'},
        {'name': 'OCD', 'url': 'ocd'}
    ]
    return render_template('questionnaire/test_home.html', questionnaires=questionnaires)

@app.route('/<form_name>')
def questionnaire(form_name):
    """Dynamically loads the form for a specific condition"""
    try:
        return render_template(f"questionnaire/{form_name}.html")
    except:
        return redirect(url_for('test_home'))

@app.route('/submit', methods=['POST'])
def submit():
    """Processes the form data and returns the result page"""
    if request.method == 'POST':
        form_data = request.form
        condition = form_data.get('condition')
        questionnaire_type = form_data.get('questionnaire_type', '')
 
        exclude_from_score = form_data.getlist('exclude_from_score')
        
        answers = []
        i = 1
        while True:
            answer_key = f'q{i}'
            if answer_key in form_data and answer_key not in exclude_from_score:
                try:
                    answers.append(int(form_data.get(answer_key)))
                except (ValueError, TypeError):
                    pass  
            else:
                if i > 1:  
                    break
            i += 1
        
        num_options = int(form_data.get('num_options', 0))
        
        max_points = (num_options - 1) if num_options > 0 else None
        
        raw_score, max_score, percentage = calculate_score(answers, max_points)
        status, diagnosis = get_diagnosis(percentage)
        remedies = get_remedies(condition)
        
        return render_template(
            'questionnaire/response.html',
            condition=condition.capitalize(),
            raw_score=raw_score,
            max_score=max_score,
            percentage=percentage,
            status=status,
            diagnosis=diagnosis,
            remedies=remedies
        )
    return redirect(url_for('test_home'))

# Error Handling
@app.errorhandler(500)
def handle_error(error):
    return jsonify({
        'error': 'An error occurred. Please try again later.',
        'details': str(error)
    }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)