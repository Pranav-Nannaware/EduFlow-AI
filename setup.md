# EduFlow AI - Setup Guide

This guide provides detailed instructions for setting up and running the EduFlow AI platform on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- Pip (Python package manager)
- Git
- A code editor of your choice (VS Code, PyCharm, etc.)
- A Gemini API key from [Google AI Studio](https://makersuite.google.com/)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Pranav-Nannaware/EduFlow-AI.git
cd EduFlow-AI
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to avoid dependency conflicts:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Install all required packages using pip:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- google-generativeai (Gemini API)
- python-dotenv (environment variable management)
- Werkzeug (Flask dependency)

### 4. Configure Environment Variables

Create a `.env` file from the example template:

```bash
# Copy the example file
cp .env.example .env

# Edit the .env file with your favorite text editor
# Replace placeholder values with your actual API keys
```

The `.env` file should contain:

```
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_SECRET_KEY=your_flask_secret_key_here
```

- For `GEMINI_API_KEY`: Get this from [Google AI Studio](https://makersuite.google.com/)
- For `FLASK_SECRET_KEY`: Create a strong random string for session security

### 5. Run the Application

You can run the application in two modes:

#### Web Application (Flask)

```bash
python app.py
```

This will start the web server at http://127.0.0.1:5000

#### Command Line Interface

```bash
python main.py
```

This launches the interactive CLI version of EduFlow AI.

## Verifying Installation

To verify that everything is working correctly:

1. Open your web browser and navigate to http://127.0.0.1:5000
2. You should see the EduFlow AI landing page
3. Register a new account to test the functionality

## Troubleshooting

### API Key Issues

If you encounter errors related to the Gemini API:
- Verify your API key is correct in the `.env` file
- Check that you have internet connectivity
- Ensure you haven't exceeded API usage limits

### Missing Dependencies

If you encounter "ModuleNotFoundError":
- Ensure your virtual environment is activated
- Try reinstalling dependencies: `pip install -r requirements.txt`

### Database Files

On first run, the application will automatically create:
- `user_profiles.json` - Stores user data
- If missing, the application will use the provided `courses_data.json`

### Port Already in Use

If port 5000 is already in use, modify `app.py` to use a different port:

```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change to an available port
```

## Next Steps

Once the application is running:

1. Create a user account
2. Select your interests
3. Explore course recommendations
4. Take quizzes and interact with the AI tutor

## Development Tips

- Flask debug mode is enabled by default for development
- User data is stored in JSON files for simplicity
- Modify templates in the `templates/` directory to customize the UI
- CSS styles can be updated in `static/css/style.css` 