import json
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import google.generativeai as genai
from main import CONFIG, EduFlowAI

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'eduflow_secret_key'  # Replace with a secure key in production

# Initialize Gemini
genai.configure(api_key=CONFIG["gemini_api_key"])
model = genai.GenerativeModel("models/gemini-2.0-flash")

# Create an instance of EduFlowAI
eduflow = EduFlowAI()

@app.route('/')
def home():
    """Display the landing page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        user_id = request.form.get('username')
        
        if user_id in eduflow.user_profiles:
            # Set user in session
            session['user_id'] = user_id
            eduflow.current_user = eduflow.user_profiles[user_id]
            return redirect(url_for('dashboard'))
        else:
            flash('Username not found. Please register first.')
            return redirect(url_for('register'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if request.method == 'POST':
        user_id = request.form.get('username')
        name = request.form.get('name')
        age = request.form.get('age')
        language = request.form.get('language')
        education = request.form.get('education') or None
        email = request.form.get('email') or None
        
        # Check if username exists
        if user_id in eduflow.user_profiles:
            flash('Username already exists. Please choose another.')
            return redirect(url_for('register'))
        
        # Create user profile
        eduflow.current_user = {
            "name": name,
            "age": age,
            "language": language,
            "education": education,
            "email": email,
            "interests": [],
            "course_history": []
        }
        
        # Store user in session
        session['user_id'] = user_id
        
        # Save user profile
        eduflow.user_profiles[user_id] = eduflow.current_user
        eduflow._save_user_profiles()
        
        return redirect(url_for('select_interests'))
    
    return render_template('register.html')

@app.route('/select_interests', methods=['GET', 'POST'])
def select_interests():
    """Handle interest selection"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        selected_interests = request.form.getlist('interests')
        
        # Store selected interests
        eduflow.current_user['interests'] = selected_interests
        eduflow._save_user_profiles()
        
        return redirect(url_for('dashboard'))
    
    interests = eduflow.courses_data["interests"]
    return render_template('select_interests.html', interests=interests)

@app.route('/dashboard')
def dashboard():
    """Display user dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = eduflow.current_user
    return render_template('dashboard.html', user=user)

@app.route('/courses')
def courses():
    """Display recommended courses"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    recommended = []
    for interest in eduflow.current_user["interests"]:
        if interest in eduflow.courses_data["courses"]:
            recommended.extend(eduflow.courses_data["courses"][interest])
    
    return render_template('courses.html', courses=recommended)

@app.route('/course/<course_name>')
def course_details(course_name):
    """Display course details"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Find the course
    course = None
    for interest in eduflow.courses_data["courses"]:
        for c in eduflow.courses_data["courses"][interest]:
            if c['name'] == course_name:
                course = c
                break
    
    if not course:
        flash('Course not found.')
        return redirect(url_for('courses'))
    
    # Generate mindmap
    mindmap = generate_mindmap(course)
    
    return render_template('course_details.html', course=course, mindmap=mindmap)

@app.route('/take_quiz/<course_name>')
def take_quiz(course_name):
    """Display course quiz"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Find the course
    course = None
    for interest in eduflow.courses_data["courses"]:
        for c in eduflow.courses_data["courses"][interest]:
            if c['name'] == course_name:
                course = c
                break
    
    if not course:
        flash('Course not found.')
        return redirect(url_for('courses'))
    
    # Generate quiz questions
    questions = generate_quiz_questions(course)
    
    # Store questions in session for evaluation
    session['quiz_questions'] = questions
    session['quiz_course'] = course_name
    
    return render_template('quiz.html', questions=questions, course=course)

@app.route('/evaluate_quiz', methods=['POST'])
def evaluate_quiz():
    """Evaluate quiz answers"""
    if 'user_id' not in session or 'quiz_questions' not in session:
        return redirect(url_for('login'))
    
    questions = session['quiz_questions']
    course_name = session['quiz_course']
    
    # Find the course
    course = None
    for interest in eduflow.courses_data["courses"]:
        for c in eduflow.courses_data["courses"][interest]:
            if c['name'] == course_name:
                course = c
                break
    
    # Calculate score
    score = 0
    for i, question in enumerate(questions):
        user_answer = request.form.get(f'q{i}')
        correct_answer = question['answer']
        
        if user_answer == correct_answer:
            score += 1
    
    percentage = (score / len(questions)) * 100
    
    # Update user profile
    if "current_course" not in eduflow.current_user:
        eduflow.current_user["current_course"] = course_name
        
    eduflow.current_user["course_history"].append({
        "course": course_name,
        "status": "enrolled" if percentage >= CONFIG["quiz_pass_threshold"] else "failed",
        "date": "2023-11-15",  # Would use datetime in real implementation
        "quiz_score": percentage,
        "quiz_skipped": False
    })
    eduflow._save_user_profiles()
    
    # Get recommendations if failed
    recommendations = None
    if percentage < CONFIG["quiz_pass_threshold"]:
        recommendations = get_ai_recommendations(course, percentage)
    
    # Clear quiz data from session
    session.pop('quiz_questions', None)
    session.pop('quiz_course', None)
    
    return render_template('quiz_results.html', 
                          score=score, 
                          total=len(questions), 
                          percentage=percentage,
                          passed=(percentage >= CONFIG["quiz_pass_threshold"]),
                          course=course,
                          recommendations=recommendations)

@app.route('/skip_quiz/<course_name>')
def skip_quiz(course_name):
    """Skip the quiz and directly enroll in the course"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Find the course
    course = None
    for interest in eduflow.courses_data["courses"]:
        for c in eduflow.courses_data["courses"][interest]:
            if c['name'] == course_name:
                course = c
                break
    
    if not course:
        flash('Course not found.')
        return redirect(url_for('courses'))
    
    # Update user profile
    if "current_course" not in eduflow.current_user:
        eduflow.current_user["current_course"] = course_name
        
    eduflow.current_user["course_history"].append({
        "course": course_name,
        "status": "enrolled",
        "date": "2023-11-15",  # Would use datetime in real implementation
        "quiz_skipped": True
    })
    eduflow._save_user_profiles()
    
    flash(f'You have been enrolled in {course_name}!')
    return redirect(url_for('dashboard'))

@app.route('/profile')
def profile():
    """Display user profile"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('profile.html', user=eduflow.current_user)

@app.route('/tutor', methods=['GET', 'POST'])
def tutor():
    """AI tutor interaction"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        question = request.form.get('question')
        
        try:
            response = model.generate_content(question)
            answer = response.text
        except Exception as e:
            answer = "Sorry, I couldn't process that question. Please try again."
        
        return render_template('tutor.html', question=question, answer=answer)
    
    return render_template('tutor.html')

@app.route('/logout')
def logout():
    """Handle user logout"""
    session.clear()
    return redirect(url_for('home'))

def generate_mindmap(course):
    """Generate a course mindmap using Gemini"""
    prompt = f"""Create a hierarchical mindmap structure for a {course['name']} course. 
    Include modules, topics, and subtopics. Format as a nested bullet list with clear hierarchy.
    Focus on the key technologies: {', '.join(course['technologies'])}."""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return """
        - Module 1: Fundamentals
          - Topic A: Introduction
          - Topic B: Basic Concepts
        - Module 2: Advanced Concepts
          - Topic C: Practical Applications
        """

def generate_quiz_questions(course):
    """Generate MCQ questions using Gemini"""
    prompt = f"""Generate 5 multiple choice questions to assess basic eligibility for a {course['name']} course.
    Include 4 options for each question and indicate the correct answer. The course covers: {', '.join(course['technologies'])}.
    
    Format each question exactly like this example between triple backticks:
    
    ```
    [
        {{
            "question": "What does HTML stand for?",
            "options": [
                "Hyper Text Markup Language",
                "Home Tool Markup Language",
                "Hyperlinks and Text Markup Language",
                "Hyper Text Making Language"
            ],
            "answer": "Hyper Text Markup Language"
        }},
        {{
            "question": "Which language styles web pages?",
            "options": [
                "HTML",
                "CSS",
                "JavaScript",
                "Python"
            ],
            "answer": "CSS"
        }}
    ]
    ```
    
    Return ONLY the JSON array between triple backticks with no other text or commentary."""
    
    try:
        response = model.generate_content(prompt)
        
        # Extract JSON from between triple backticks if present
        response_text = response.text
        if '```' in response_text:
            response_text = response_text.split('```')[1]
        
        # Clean the response and parse JSON
        response_text = response_text.strip().replace('json', '').replace('```', '')
        return json.loads(response_text)
    except Exception as e:
        # Fallback to some default questions
        return [
            {
                "question": "What does HTML stand for?",
                "options": [
                    "Hyper Text Markup Language",
                    "Home Tool Markup Language",
                    "Hyperlinks and Text Markup Language",
                    "Hyper Text Making Language"
                ],
                "answer": "Hyper Text Markup Language"
            },
            {
                "question": "Which language styles web pages?",
                "options": [
                    "HTML",
                    "CSS",
                    "JavaScript",
                    "Python"
                ],
                "answer": "CSS"
            }
        ]

def get_ai_recommendations(course, score):
    """Get AI recommendations for failed quiz"""
    prompt = f"""A user scored {score}% on a {course['name']} eligibility quiz. 
    Their interests are: {', '.join(eduflow.current_user['interests'])}.
    Suggest 2-3 alternative learning paths or preparatory steps.
    Keep suggestions brief and actionable."""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return """
        1. Consider introductory courses in this field
        2. Explore related areas that might be better suited
        3. Review fundamental concepts before retaking the quiz
        """

if __name__ == '__main__':
    app.run(debug=True) 