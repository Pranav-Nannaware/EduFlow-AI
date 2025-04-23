import json
import os
from typing import Dict, List, Optional, Tuple
import google.generativeai as genai

# Configuration
CONFIG = {
    "user_data_file": "user_profiles.json",
    "courses_data_file": "courses_data.json",
    "gemini_api_key": "AIzaSyD7BoK4jxzGJ6xzYUlzt6arb0rvF0kyuVs",  # Replace with your actual API key
    "quiz_pass_threshold": 70  # Percentage score needed to pass
}

# Initialize Gemini
genai.configure(api_key=CONFIG["gemini_api_key"])
model = genai.GenerativeModel("models/gemini-2.0-flash")    

class EduFlowAI:
    def __init__(self):
        self.current_user: Optional[Dict] = None
        self.courses_data: Dict = self._load_courses_data()
        self.user_profiles: Dict = self._load_user_profiles()
        
    def _load_user_profiles(self) -> Dict:
        """Load user profiles from JSON file or create empty dict"""
        try:
            with open(CONFIG["user_data_file"], 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
            
    def _load_courses_data(self) -> Dict:
        """Load courses data from JSON file"""
        try:
            with open(CONFIG["courses_data_file"], 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Fallback to basic course data if file not found
            return {
                "interests": ["Computer Science", "Electrical", "Mechanical", "Civil", "Biology", "Commerce", "Arts"],
                "courses": {
                    "Computer Science": [
                        {"name": "AI/ML Engineer", "duration": "6 months", "technologies": ["Python", "TensorFlow", "PyTorch"]},
                        {"name": "Web Developer", "duration": "4 months", "technologies": ["HTML", "CSS", "JavaScript"]}
                    ],
                    "Electrical": [
                        {"name": "Electrical Design Engineer", "duration": "8 months", "technologies": ["AutoCAD", "MATLAB"]}
                    ]
                }
            }
    
    def _save_user_profiles(self):
        """Save user profiles to JSON file"""
        with open(CONFIG["user_data_file"], 'w') as f:
            json.dump(self.user_profiles, f, indent=2)
    
    def onboard_user(self):
        """Handle new user onboarding process"""
        print("\n=== EduFlow AI - New User Onboarding ===")
        
        user_id = input("Enter a username: ").strip()
        if user_id in self.user_profiles:
            print("Welcome back! Loading your profile...")
            self.current_user = self.user_profiles[user_id]
            return
            
        print("\nLet's get to know you better!")
        name = input("Your name: ").strip()
        age = input("Your age: ").strip()
        language = self._select_language()
        education = input("Education level (optional): ").strip() or None
        email = input("Contact email (optional): ").strip() or None
        
        # Store basic user info
        self.current_user = {
            "name": name,
            "age": age,
            "language": language,
            "education": education,
            "email": email,
            "interests": [],
            "course_history": []
        }
        
        # Select interests
        self.select_interests()
        
        # Save the new user
        self.user_profiles[user_id] = self.current_user
        self._save_user_profiles()
        print("\nProfile created successfully! Let's explore courses.")
    
    def _select_language(self) -> str:
        """Handle language selection"""
        print("\nPreferred Language:")
        print("1. English")
        print("2. Hindi")
        print("3. Marathi")
        
        while True:
            choice = input("Select (1-3): ").strip()
            if choice == "1":
                return "English"
            elif choice == "2":
                return "Hindi"
            elif choice == "3":
                return "Marathi"
            print("Invalid choice. Please try again.")
    
    def select_interests(self):
        """Let user select interests"""
        print("\nWhat are you most interested in? (Select 1-3)")
        for i, interest in enumerate(self.courses_data["interests"], 1):
            print(f"{i}. {interest}")
        
        selected = []
        while len(selected) < 3:
            try:
                choice = int(input(f"Select interest #{len(selected)+1} (1-{len(self.courses_data['interests'])}): ")) - 1
                if 0 <= choice < len(self.courses_data["interests"]):
                    interest = self.courses_data["interests"][choice]
                    if interest not in selected:
                        selected.append(interest)
                    else:
                        print("You already selected that interest.")
                else:
                    print("Invalid number. Try again.")
            except ValueError:
                print("Please enter a number.")
        
        self.current_user["interests"] = selected
        print(f"\nYour interests: {', '.join(selected)}")
    
    def recommend_courses(self):
        """Recommend courses based on user interests"""
        if not self.current_user:
            print("Please complete onboarding first.")
            return
            
        print("\n=== Recommended Courses ===")
        recommended = []
        
        for interest in self.current_user["interests"]:
            if interest in self.courses_data["courses"]:
                recommended.extend(self.courses_data["courses"][interest])
        
        if not recommended:
            print("No courses found for your interests. We'll expand our offerings soon!")
            return
        
        print("\nBased on your interests, we recommend:")
        for i, course in enumerate(recommended, 1):
            print(f"\n{i}. {course['name']}")
            print(f"   Duration: {course['duration']}")
            print(f"   Key Technologies: {', '.join(course['technologies'])}")
        
        self._select_course(recommended)
    
    def _select_course(self, courses: List[Dict]):
        """Let user select a course from recommendations"""
        while True:
            try:
                choice = int(input("\nSelect a course to explore (number): ")) - 1
                if 0 <= choice < len(courses):
                    selected_course = courses[choice]
                    self.display_course_info(selected_course)
                    break
                print("Invalid selection. Try again.")
            except ValueError:
                print("Please enter a number.")
    
    def display_course_info(self, course: Dict):
        """Display detailed course information with option to skip quiz"""
        print(f"\n=== {course['name']} ===")
        print(f"\nOverview: {course.get('overview', 'Comprehensive course covering all key aspects.')}")
        print(f"\nDuration: {course['duration']}")
        print("\nKey Technologies/Tools:")
        for tech in course['technologies']:
            print(f"- {tech}")
        
        print("\nCareer Outlook:")
        print(course.get('career_outlook', 'Excellent growth potential in this field.'))
        
        # Generate mindmap
        self.generate_mindmap(course)
        
        # Ask if user wants to take the quiz
        while True:
            choice = input("\nWould you like to take the eligibility quiz? (y/n): ").lower()
            if choice == 'y':
                self.run_eligibility_quiz(course)
                break
            elif choice == 'n':
                print("\nYou've chosen to skip the quiz. Proceeding to course materials...")
                self._quiz_passed(course)  # Treat as passed
                break
            else:
                print("Please enter 'y' for yes or 'n' for no.")
    
    def generate_mindmap(self, course: Dict):
        """Generate and display a course mindmap using Gemini"""
        print("\nGenerating Course Mindmap...")
        
        prompt = f"""Create a hierarchical mindmap structure for a {course['name']} course. 
        Include modules, topics, and subtopics. Format as a nested bullet list with clear hierarchy.
        Focus on the key technologies: {', '.join(course['technologies'])}."""
        
        try:
            response = model.generate_content(prompt)
            print("\nCourse Structure:")
            print(response.text)
        except Exception as e:
            print("Couldn't generate mindmap. Here's a basic structure:")
            print("- Module 1: Fundamentals\n  - Topic A\n  - Topic B")
            print("- Module 2: Advanced Concepts\n  - Topic C")
    
    def run_eligibility_quiz(self, course: Dict):
        """Generate and administer an eligibility quiz"""
        print("\n=== Course Eligibility Quiz ===")
        print(f"Answer these questions to check your readiness for {course['name']}")
        
        # Generate quiz questions with Gemini
        questions = self._generate_quiz_questions(course)
        
        if not questions:
            print("Quiz generation failed. Proceeding to course...")
            self._quiz_passed(course)
            return
        
        score = 0
        for i, q in enumerate(questions, 1):
            print(f"\nQ{i}: {q['question']}")
            for j, option in enumerate(q['options'], 1):
                print(f"  {j}. {option}")
            
            while True:
                try:
                    answer = int(input("Your answer (number): ")) - 1
                    if 0 <= answer < len(q['options']):
                        if q['options'][answer] == q['answer']:
                            print("Correct!")
                            score += 1
                        else:
                            print(f"Incorrect. The correct answer is: {q['answer']}")
                        break
                    print("Invalid choice. Try again.")
                except ValueError:
                    print("Please enter a number.")
        
        percentage = (score / len(questions)) * 100
        print(f"\nQuiz Result: {score}/{len(questions)} ({percentage:.0f}%)")
        
        if percentage >= CONFIG["quiz_pass_threshold"]:
            self._quiz_passed(course)
        else:
            self._quiz_failed(course, percentage)
    
    def _generate_quiz_questions(self, course: Dict) -> List[Dict]:
        """Generate MCQ questions using Gemini with more reliable JSON parsing"""
        prompt = f"""Generate 5 multiple choice questions to assess basic eligibility for a {course['name']} course.
        Include 4 options for each question and indicate the correct answer. The course covers: {', '.join(course['technologies'])}.
        
        Format each question exactly like this example between  marks:
        
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
        
        Return ONLY the JSON array between  marks with no other text or commentary."""
        
        try:
            response = model.generate_content(prompt)
            
            # Extract JSON from between  marks if present
            response_text = response.text
            if '' in response_text:
                response_text = response_text.split('')[1]
            
            # Clean the response and parse JSON
            response_text = response_text.strip().replace('', '')
            return json.loads(response_text)
        except Exception as e:
            print(f"Error generating quiz: {e}")
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
    
    def _quiz_passed(self, course: Dict):
        """Handle both quiz pass and skipped quiz scenarios"""
        print(f"\nYou're ready to explore {course['name']}.")
        print("\nNext steps:")
        print("- Access learning materials")
        print("- Start with Module 1")
        print("- Track your progress")
        
        # Store course enrollment
        if "current_course" not in self.current_user:
            self.current_user["current_course"] = course['name']
            self.current_user["course_history"].append({
                "course": course['name'],
                "status": "enrolled",
                "date": "2023-11-15",  # Would use datetime in real implementation
                "quiz_skipped": True  # Track if quiz was skipped
            })
            self._save_user_profiles()

    def _quiz_failed(self, course: Dict, score: float):
        """Handle quiz fail scenario with alternative recommendations"""
        print("\nYour score indicates you might need more preparation for this course.")
        print("\nAI Recommendations:")
        
        # Get AI recommendations
        prompt = f"""A user scored {score}% on a {course['name']} eligibility quiz. 
        Their interests are: {', '.join(self.current_user['interests'])}.
        Suggest 2-3 alternative learning paths or preparatory steps.
        Keep suggestions brief and actionable."""
        
        try:
            response = model.generate_content(prompt)
            print(response.text)
        except Exception as e:
            print("1. Consider introductory courses in this field")
            print("2. Explore related areas that might be better suited")
            print("3. Review fundamental concepts before retaking the quiz")
        
        print("\nOptions:")
        print("1. Try the quiz again")
        print("2. Explore other courses")
        print("3. Get tutor assistance")
        
        choice = input("Select an option: ").strip()
        if choice == "1":
            self.run_eligibility_quiz(course)
        elif choice == "2":
            self.recommend_courses()
        elif choice == "3":
            self.access_ai_tutor()
    
    def access_ai_tutor(self):
        """Interact with the AI tutor"""
        print("\n=== AI Tutor ===")
        print("Ask any question about your courses or learning path. Type 'exit' to quit.")
        
        while True:
            question = input("\nYour question: ").strip()
            if question.lower() in ['exit', 'quit']:
                break
                
            try:
                response = model.generate_content(question)
                print("\nAI Tutor:", response.text)
            except Exception as e:
                print("Sorry, I couldn't process that. Please try again.")
    
    def main_menu(self):
        """Display main menu and handle user choices"""
        while True:
            print("\n=== EduFlow AI Main Menu ===")
            print("1. Recommend Courses")
            print("2. Access AI Tutor")
            print("3. Update Interests")
            print("4. View Profile")
            print("5. Exit")
            
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                self.recommend_courses()
            elif choice == "2":
                self.access_ai_tutor()
            elif choice == "3":
                self.select_interests()
                self._save_user_profiles()
            elif choice == "4":
                self.view_profile()
            elif choice == "5":
                print("Thank you for using EduFlow AI!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def view_profile(self):
        """Display user profile information including quiz status"""
        if not self.current_user:
            print("No user profile loaded.")
            return
            
        print("\n=== Your Profile ===")
        print(f"Name: {self.current_user['name']}")
        print(f"Age: {self.current_user['age']}")
        print(f"Language: {self.current_user['language']}")
        print(f"Interests: {', '.join(self.current_user['interests'])}")
        
        if self.current_user.get('current_course'):
            print(f"\nCurrent Course: {self.current_user['current_course']}")
        
        if self.current_user['course_history']:
            print("\nCourse History:")
            for course in self.current_user['course_history']:
                status = course['status']
                if course.get('quiz_skipped'):
                    status += " (quiz skipped)"
                print(f"- {course['course']} ({status})")


# Main execution
if __name__ == "__main__":
    system = EduFlowAI()
    
    # Check if user wants to load existing profile
    load_existing = input("Do you have an existing profile? (y/n): ").lower() == 'y'
    if load_existing:
        user_id = input("Enter your username: ").strip()
        if user_id in system.user_profiles:
            system.current_user = system.user_profiles[user_id]
            print(f"Welcome back, {system.current_user['name']}!")
        else:
            print("Username not found. Starting new user onboarding.")
            load_existing = False
    
    if not load_existing:
        system.onboard_user()
    
    system.main_menu()