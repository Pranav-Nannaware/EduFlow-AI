# EduFlow AI - Developer Documentation

This document provides technical details for developers looking to understand, modify, or extend the EduFlow AI platform. It covers the application architecture, code organization, key components, and extension points.

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Core Components](#core-components)
- [Data Models](#data-models)
- [Flask Application Structure](#flask-application-structure)
- [Template System](#template-system)
- [AI Integration](#ai-integration)
- [Key Workflows](#key-workflows)
- [Adding New Features](#adding-new-features)
- [Testing](#testing)

## Architecture Overview

EduFlow AI follows a Model-View-Controller (MVC) pattern:
- **Model**: The `EduFlowAI` class in `main.py` handles data manipulation and business logic
- **View**: Jinja2 templates in the `/templates` directory render the UI
- **Controller**: Route handlers in `app.py` process requests and connect models with views

The application uses:
- Flask for the web framework
- Google's Gemini API for AI capabilities
- JSON files for data persistence
- Bootstrap for frontend styling
- JavaScript for client-side interactivity

## Core Components

### EduFlowAI Class (main.py)

The core functionality is encapsulated in the `EduFlowAI` class:

```python
class EduFlowAI:
    def __init__(self):
        self.current_user: Optional[Dict] = None
        self.courses_data: Dict = self._load_courses_data()
        self.user_profiles: Dict = self._load_user_profiles()
```

Key methods include:
- `_load_user_profiles()`: Loads user data from JSON file
- `_load_courses_data()`: Loads course information
- `_save_user_profiles()`: Persists user data
- `select_interests()`: Manages user interest selection
- `recommend_courses()`: Generates personalized recommendations
- `run_eligibility_quiz()`: Administers course assessments
- `access_ai_tutor()`: Provides AI-powered assistance

### Flask Application (app.py)

The Flask application connects the EduFlowAI class with web routes:

```python
app = Flask(__name__)
app.secret_key = 'eduflow_secret_key'

# Create an instance of EduFlowAI
eduflow = EduFlowAI()

@app.route('/')
def home():
    """Display the landing page"""
    return render_template('index.html')
```

Key route handlers:
- User authentication routes (`/login`, `/register`)
- Dashboard and profile routes
- Course-related routes (`/courses`, `/course/<course_name>`)
- Quiz routes (`/take_quiz/<course_name>`, `/evaluate_quiz`)
- AI tutor interface (`/tutor`)

## Data Models

### User Profile Structure

```json
{
  "username": {
    "name": "User's Name",
    "age": "25",
    "language": "English",
    "education": "Graduate",
    "email": "user@example.com",
    "interests": ["Computer Science", "Electrical", "Biology"],
    "current_course": "AI/ML Engineer",
    "course_history": [
      {
        "course": "Web Developer",
        "status": "enrolled",
        "date": "2023-11-15",
        "quiz_skipped": true
      }
    ]
  }
}
```

### Course Data Structure

```json
{
  "interests": ["Computer Science", "Electrical", "Mechanical", "Civil", "Biology", "Commerce", "Arts"],
  "courses": {
    "Computer Science": [
      {
        "name": "AI/ML Engineer",
        "duration": "6 months",
        "technologies": ["Python", "TensorFlow", "PyTorch"],
        "overview": "Course description...",
        "career_outlook": "Career information..."
      }
    ]
  }
}
```

## Flask Application Structure

### Route Organization

Routes are organized by functional area:
1. **Authentication routes**: Login, register, logout
2. **Onboarding routes**: Interest selection
3. **Dashboard routes**: Main dashboard view
4. **Course routes**: Course listing, details, enrollment
5. **Quiz routes**: Taking quizzes, evaluating results
6. **Profile routes**: User profile management
7. **AI routes**: AI tutor interaction

### Session Management

The application uses Flask's session mechanism to track authenticated users:

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('username')
        
        if user_id in eduflow.user_profiles:
            # Set user in session
            session['user_id'] = user_id
            eduflow.current_user = eduflow.user_profiles[user_id]
            return redirect(url_for('dashboard'))
```

Authentication is enforced using session checks:

```python
@app.route('/dashboard')
def dashboard():
    """Display user dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = eduflow.current_user
    return render_template('dashboard.html', user=user)
```

## Template System

### Template Inheritance

The application uses Jinja2 template inheritance with a base template:

```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{% block title %}EduFlow AI{% endblock %}</title>
    <!-- CSS includes -->
</head>
<body>
    <!-- Navigation -->
    <main class="container py-4">
        {% block content %}{% endblock %}
    </main>
    <!-- Footer -->
    {% block scripts %}{% endblock %}
</body>
</html>
```

Child templates extend this base:

```html
<!-- dashboard.html -->
{% extends 'base.html' %}

{% block title %}Dashboard - EduFlow AI{% endblock %}

{% block content %}
    <!-- Dashboard content -->
{% endblock %}
```

### Form Handling

Forms use standard HTML POST methods with CSRF protection:

```html
<form method="POST" action="{{ url_for('login') }}" class="needs-validation" novalidate>
    <div class="mb-4">
        <label for="username" class="form-label">Username</label>
        <input type="text" class="form-control" id="username" name="username" required>
    </div>
    <button type="submit" class="btn btn-primary">Sign In</button>
</form>
```

## AI Integration

### Initializing the Gemini API

```python
# Initialize Gemini
genai.configure(api_key=CONFIG["gemini_api_key"])
model = genai.GenerativeModel("models/gemini-2.0-flash")
```

### AI-Powered Features

1. **Mindmap Generation**: Creates course structure visualizations
2. **Quiz Generation**: Creates assessment questions
3. **Learning Recommendations**: Suggests next steps after quiz results
4. **AI Tutor**: Provides conversational learning assistance

### Prompt Engineering

Effective prompts are critical for the AI components:

```python
def generate_mindmap(course):
    """Generate a course mindmap using Gemini"""
    prompt = f"""Create a hierarchical mindmap structure for a {course['name']} course. 
    Include modules, topics, and subtopics. Format as a nested bullet list with clear hierarchy.
    Focus on the key technologies: {', '.join(course['technologies'])}."""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return fallback_mindmap
```

## Key Workflows

### User Registration Flow

1. User submits registration form (`/register`)
2. System validates and creates user profile
3. User is redirected to interest selection (`/select_interests`)
4. User selects at least 3 interests
5. System saves preferences and redirects to dashboard (`/dashboard`)

### Course Enrollment Flow

1. User browses course recommendations
2. User selects a course to view details (`/course/<course_name>`)
3. User either takes eligibility quiz or skips it
4. If taking quiz:
   - System generates and displays quiz questions
   - User submits answers
   - System evaluates responses and shows results
   - If passed, user is enrolled; if failed, recommendations are shown
5. If skipping quiz:
   - User is directly enrolled in the course
6. System updates user profile with enrollment data

## Adding New Features

### Adding a New Course Category

1. Modify the `courses_data.json` file:
```json
{
  "interests": ["Computer Science", "Electrical", "NEW_CATEGORY"],
  "courses": {
    "NEW_CATEGORY": [
      {
        "name": "New Course Name",
        "duration": "X months",
        "technologies": ["Tech1", "Tech2"],
        "overview": "Course description..."
      }
    ]
  }
}
```

### Adding a New Quiz Type

1. Create a new quiz generation function in `app.py`:
```python
def generate_advanced_quiz(course):
    """Generate advanced quiz questions"""
    prompt = f"""Create advanced assessment questions for {course['name']}..."""
    # Implementation details
```

2. Add a new route for the advanced quiz:
```python
@app.route('/advanced_quiz/<course_name>')
def advanced_quiz(course_name):
    # Implementation details
```

3. Create a template for the new quiz type:
```html
<!-- templates/advanced_quiz.html -->
{% extends 'base.html' %}
<!-- Quiz content -->
```

### Extending User Profiles

To add new user profile fields:

1. Modify the registration form in `register.html`
2. Update the registration route in `app.py`:
```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Get existing fields
    # Get new field
    new_field = request.form.get('new_field')
    
    # Update user profile
    eduflow.current_user = {
        # Existing fields
        "new_field": new_field
    }
```

3. Update profile display in `profile.html`

## Testing

### Manual Testing Procedures

1. **User Authentication Testing**:
   - Test registration with valid/invalid data
   - Test login with correct/incorrect credentials
   - Test session persistence

2. **Course System Testing**:
   - Verify recommendations match user interests
   - Test course detail page displays correctly
   - Verify mindmap generation works properly

3. **Quiz Testing**:
   - Test quiz generation contains valid questions
   - Verify scoring mechanism works correctly
   - Test pass/fail scenarios and recommendations

4. **AI Tutor Testing**:
   - Test conversation flow and response quality
   - Verify context awareness across multiple messages
   - Test error handling for API failures

### Adding Automated Tests

A test directory structure could be added:

```
eduflow-ai/
├── tests/
│   ├── test_auth.py     # Authentication tests
│   ├── test_courses.py  # Course system tests
│   ├── test_quiz.py     # Quiz functionality tests
│   └── test_ai.py       # AI integration tests
```

Example test case:

```python
# test_auth.py
def test_user_registration():
    with app.test_client() as client:
        response = client.post('/register', data={
            'username': 'testuser',
            'name': 'Test User',
            'age': '25',
            'language': 'English'
        })
        assert response.status_code == 302  # Redirect
        assert 'user_id' in session
```

## Performance Considerations

1. **AI API Optimization**:
   - Cache common AI responses
   - Implement rate limiting for API calls
   - Use batch processing where possible

2. **Data Storage**:
   - Consider migrating to a database for larger user bases
   - Implement proper indexing for faster lookups

3. **Frontend Optimization**:
   - Minify CSS and JavaScript
   - Implement lazy loading for images
   - Use client-side caching 