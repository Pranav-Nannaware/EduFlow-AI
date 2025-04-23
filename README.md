# EduFlow AI - AI-Powered Learning Platform

EduFlow AI is an intelligent educational platform that leverages Google's Gemini AI to deliver personalized learning experiences. The application provides course recommendations based on user interests, interactive quizzes with AI-generated questions, and an AI tutor to assist with learning.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Integration](#api-integration)
- [User Journey](#user-journey)
- [Future Enhancements](#future-enhancements)

## Overview

EduFlow AI transforms the traditional learning experience by:
- Creating personalized learning paths based on user preferences
- Providing AI-powered course recommendations 
- Generating interactive quizzes to test knowledge
- Offering an AI tutor for 24/7 assistance
- Visualizing course content with AI-generated mindmaps

## Features

### User Management
- User registration and profile creation
- Interest selection and preference tracking
- Personalized dashboard for each user

### Course System
- Interest-based course recommendations
- Detailed course information pages
- Course structure visualization with AI-generated mindmaps
- Career outlook and job potential information

### Assessment System
- AI-generated eligibility quizzes
- Instant scoring and feedback
- Alternative learning path recommendations for users who don't pass

### AI Tutor
- Interactive chat interface
- Context-aware learning assistance
- Course-specific knowledge support

## Technology Stack

### Backend
- Python 3.x
- Flask web framework
- Google Generative AI (Gemini 2.0 Flash API)
- JSON for data storage

### Frontend
- HTML5, CSS3, JavaScript
- Bootstrap 5 framework
- Font Awesome icons
- Responsive design for mobile and desktop

## Project Structure

```
eduflow-ai/
├── app.py                # Flask application main file
├── main.py               # Core EduFlowAI class implementation
├── static/               # Static assets
│   ├── css/              # Stylesheet files
│   │   └── style.css     # Custom CSS styles
│   ├── js/               # JavaScript files
│   │   └── script.js     # Custom JavaScript functionality
│   └── images/           # Image assets
├── templates/            # HTML templates
│   ├── base.html         # Base template with common elements
│   ├── index.html        # Landing page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── select_interests.html  # Interest selection page
│   ├── dashboard.html    # User dashboard
│   ├── courses.html      # Course listings
│   ├── course_details.html  # Individual course page
│   ├── quiz.html         # Quiz interface
│   ├── quiz_results.html # Quiz results page
│   ├── profile.html      # User profile page
│   └── tutor.html        # AI tutor interface
├── user_profiles.json    # User data storage (created on first run)
└── courses_data.json     # Course information (created on first run)
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/eduflow-ai.git
cd eduflow-ai
```

2. Install required packages:
```bash
pip install flask google-generativeai
```

3. Add your Google Gemini API key:
   - Obtain an API key from [Google AI Studio](https://makersuite.google.com/)
   - Update the `CONFIG["gemini_api_key"]` value in `main.py`

4. Run the application:
```bash
python app.py
```

5. Access the web interface at `http://127.0.0.1:5000`

## Usage

### User Registration and Onboarding
1. Visit the homepage and click "Get Started"
2. Create an account with a username and basic information
3. Select at least 3 interests to personalize your experience
4. Explore your personalized dashboard

### Course Exploration
1. Browse recommended courses on your dashboard
2. Use filters and search to find specific courses
3. View detailed course information, including:
   - Course overview and requirements
   - Technical skills covered
   - Career opportunities
   - Course structure mindmap

### Taking a Course
1. Take the eligibility quiz to assess your readiness
2. Review your quiz results and recommendations
3. Enroll in the course (with or without passing the quiz)
4. Track your enrolled courses on your dashboard

### Using the AI Tutor
1. Navigate to the AI Tutor page
2. Ask questions about course content or general knowledge
3. Receive detailed, personalized responses

## API Integration

EduFlow AI integrates with Google's Gemini API for several AI-powered features:

### Mindmap Generation
```python
def generate_mindmap(course):
    prompt = f"""Create a hierarchical mindmap structure for a {course['name']} course. 
    Include modules, topics, and subtopics. Format as a nested bullet list with clear hierarchy.
    Focus on the key technologies: {', '.join(course['technologies'])}."""
    
    response = model.generate_content(prompt)
    return response.text
```

### Quiz Generation
```python
def generate_quiz_questions(course):
    prompt = f"""Generate 5 multiple choice questions to assess basic eligibility for a {course['name']} course.
    Include 4 options for each question and indicate the correct answer. The course covers: {', '.join(course['technologies'])}.
    
    Format each question as JSON...
    """
    
    response = model.generate_content(prompt)
    return json.loads(processed_response)
```

### Recommendations After Failed Quiz
```python
def get_ai_recommendations(course, score):
    prompt = f"""A user scored {score}% on a {course['name']} eligibility quiz. 
    Their interests are: {', '.join(eduflow.current_user['interests'])}.
    Suggest 2-3 alternative learning paths or preparatory steps.
    Keep suggestions brief and actionable."""
    
    response = model.generate_content(prompt)
    return response.text
```

## User Journey

1. **Registration**: User creates an account with basic information
2. **Interest Selection**: User selects at least 3 interest areas
3. **Dashboard**: User views personalized course recommendations
4. **Course Selection**: User explores course details and structure
5. **Eligibility Assessment**: User takes an AI-generated quiz
6. **Course Enrollment**: User enrolls in the course (with or without quiz)
7. **Learning Support**: User accesses AI tutor for assistance
8. **Profile Management**: User tracks progress and updates preferences

## Future Enhancements

- **Learning Path Tracking**: Visual progression through course modules
- **User Collaboration**: Discussion forums and peer learning
- **Advanced Assessment**: Adaptive quizzes that adjust to user knowledge
- **Content Generation**: AI-generated course materials and examples
- **Mobile Application**: Native mobile experience for iOS and Android
- **Learning Analytics**: Detailed insights into learning patterns and progress
- **Certificate Generation**: Completion certificates for finished courses

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Generative AI for powering the AI features
- Flask framework for web application development
- Bootstrap for responsive UI components 