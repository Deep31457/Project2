import json
import random
import time
from typing import List, Dict, Tuple
import os

class QuizGame:
    def __init__(self):
        self.questions = self.load_questions()
        self.score = 0
        self.total_questions = 0
        self.correct_answers = 0
        self.user_name = ""
        self.current_category = ""
        self.current_difficulty = ""
        
    def load_questions(self) -> Dict:
        """Load questions from the questions file or create default questions."""
        if os.path.exists('questions.json'):
            try:
                with open('questions.json', 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default questions if file doesn't exist
        return {
            "General Knowledge": {
                "easy": [
                    {
                        "question": "What is the capital of France?",
                        "options": ["London", "Berlin", "Paris", "Madrid"],
                        "correct": 2,
                        "explanation": "Paris is the capital and most populous city of France."
                    },
                    {
                        "question": "Which planet is known as the Red Planet?",
                        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                        "correct": 1,
                        "explanation": "Mars is called the Red Planet due to iron oxide on its surface."
                    },
                    {
                        "question": "How many continents are there?",
                        "options": ["5", "6", "7", "8"],
                        "correct": 2,
                        "explanation": "There are 7 continents: Asia, Africa, North America, South America, Antarctica, Europe, and Australia."
                    }
                ],
                "medium": [
                    {
                        "question": "What is the largest ocean on Earth?",
                        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
                        "correct": 3,
                        "explanation": "The Pacific Ocean is the largest ocean, covering about 46% of Earth's water surface."
                    },
                    {
                        "question": "In which year did World War II end?",
                        "options": ["1944", "1945", "1946", "1947"],
                        "correct": 1,
                        "explanation": "World War II ended in 1945 with the surrender of Japan in September."
                    }
                ],
                "hard": [
                    {
                        "question": "What is the smallest country in the world?",
                        "options": ["Monaco", "Vatican City", "San Marino", "Liechtenstein"],
                        "correct": 1,
                        "explanation": "Vatican City is the smallest sovereign state in the world by area and population."
                    }
                ]
            },
            "Science": {
                "easy": [
                    {
                        "question": "What gas do plants absorb from the atmosphere?",
                        "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
                        "correct": 2,
                        "explanation": "Plants absorb carbon dioxide during photosynthesis to create glucose and oxygen."
                    },
                    {
                        "question": "How many bones are in the adult human body?",
                        "options": ["206", "208", "210", "212"],
                        "correct": 0,
                        "explanation": "An adult human body has 206 bones."
                    }
                ],
                "medium": [
                    {
                        "question": "What is the chemical symbol for gold?",
                        "options": ["Go", "Gd", "Au", "Ag"],
                        "correct": 2,
                        "explanation": "Au is the chemical symbol for gold, derived from the Latin word 'aurum'."
                    }
                ],
                "hard": [
                    {
                        "question": "What is the speed of light in vacuum?",
                        "options": ["299,792,458 m/s", "300,000,000 m/s", "299,800,000 m/s", "298,000,000 m/s"],
                        "correct": 0,
                        "explanation": "The speed of light in vacuum is exactly 299,792,458 meters per second."
                    }
                ]
            },
            "History": {
                "easy": [
                    {
                        "question": "Who was the first President of the United States?",
                        "options": ["Thomas Jefferson", "George Washington", "John Adams", "Benjamin Franklin"],
                        "correct": 1,
                        "explanation": "George Washington was the first President of the United States, serving from 1789 to 1797."
                    }
                ],
                "medium": [
                    {
                        "question": "In which year did the Berlin Wall fall?",
                        "options": ["1987", "1988", "1989", "1990"],
                        "correct": 2,
                        "explanation": "The Berlin Wall fell on November 9, 1989, marking the beginning of German reunification."
                    }
                ],
                "hard": [
                    {
                        "question": "Which empire was ruled by Julius Caesar?",
                        "options": ["Greek Empire", "Roman Empire", "Byzantine Empire", "Ottoman Empire"],
                        "correct": 1,
                        "explanation": "Julius Caesar was a Roman general and statesman who played a critical role in the Roman Republic."
                    }
                ]
            }
        }
    
    def display_welcome(self):
        """Display welcome message and get user name."""
        print("=" * 60)
        print("🎯 WELCOME TO THE ULTIMATE QUIZ GAME! 🎯")
        print("=" * 60)
        print("Test your knowledge across different categories and difficulty levels!")
        print("Score points for correct answers and see how you rank!")
        print("-" * 60)
        
        self.user_name = input("Please enter your name: ").strip()
        if not self.user_name:
            self.user_name = "Player"
        
        print(f"\nHello {self.user_name}! Let's start your quiz adventure! 🚀")
        
    def display_categories(self):
        """Display available categories and let user choose."""
        print("\n" + "=" * 40)
        print("📚 AVAILABLE CATEGORIES")
        print("=" * 40)
        
        categories = list(self.questions.keys())
        for i, category in enumerate(categories, 1):
            question_count = sum(len(self.questions[category][diff]) for diff in self.questions[category])
            print(f"{i}. {category} ({question_count} questions)")
        
        print(f"{len(categories) + 1}. Random Mix (All categories)")
        
        while True:
            try:
                choice = int(input(f"\nSelect a category (1-{len(categories) + 1}): "))
                if 1 <= choice <= len(categories):
                    self.current_category = categories[choice - 1]
                    return self.current_category
                elif choice == len(categories) + 1:
                    self.current_category = "Random Mix"
                    return "Random Mix"
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
    
    def display_difficulties(self):
        """Display difficulty levels and let user choose."""
        print("\n" + "=" * 40)
        print("⚡ DIFFICULTY LEVELS")
        print("=" * 40)
        
        difficulties = ["easy", "medium", "hard", "mixed"]
        difficulty_info = {
            "easy": "Easy (1 point per question) 🟢",
            "medium": "Medium (2 points per question) 🟡", 
            "hard": "Hard (3 points per question) 🔴",
            "mixed": "Mixed (All difficulties) 🌈"
        }
        
        for i, diff in enumerate(difficulties, 1):
            print(f"{i}. {difficulty_info[diff]}")
        
        while True:
            try:
                choice = int(input(f"\nSelect difficulty (1-{len(difficulties)}): "))
                if 1 <= choice <= len(difficulties):
                    self.current_difficulty = difficulties[choice - 1]
                    return self.current_difficulty
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
    
    def get_questions_for_quiz(self, category: str, difficulty: str, num_questions: int = 10) -> List[Dict]:
        """Get questions based on selected category and difficulty."""
        all_questions = []
        
        if category == "Random Mix":
            # Get questions from all categories
            for cat in self.questions:
                if difficulty == "mixed":
                    for diff in self.questions[cat]:
                        all_questions.extend(self.questions[cat][diff])
                else:
                    if difficulty in self.questions[cat]:
                        all_questions.extend(self.questions[cat][diff])
        else:
            # Get questions from specific category
            if difficulty == "mixed":
                for diff in self.questions[category]:
                    all_questions.extend(self.questions[category][diff])
            else:
                if difficulty in self.questions[category]:
                    all_questions.extend(self.questions[category][diff])
        
        # Add difficulty info to questions for scoring
        for q in all_questions:
            if 'difficulty' not in q:
                # Determine difficulty based on the difficulty level or infer from point structure
                if difficulty != "mixed":
                    q['difficulty'] = difficulty
                else:
                    # For mixed, we'll assign based on question complexity (this is a simplified approach)
                    q['difficulty'] = 'medium'  # Default for mixed
        
        # Shuffle and return requested number of questions
        random.shuffle(all_questions)
        return all_questions[:min(num_questions, len(all_questions))]
    
    def get_points(self, difficulty: str) -> int:
        """Get points based on difficulty level."""
        points_map = {"easy": 1, "medium": 2, "hard": 3}
        return points_map.get(difficulty, 2)
    
    def ask_question(self, question: Dict, question_num: int, total: int) -> bool:
        """Ask a single question and return whether it was answered correctly."""
        print("\n" + "=" * 60)
        print(f"Question {question_num}/{total}")
        print("=" * 60)
        
        print(f"📝 {question['question']}")
        print()
        
        # Display options
        for i, option in enumerate(question['options']):
            print(f"  {chr(65 + i)}. {option}")
        
        # Get user answer
        while True:
            answer = input("\nYour answer (A/B/C/D): ").strip().upper()
            if answer in ['A', 'B', 'C', 'D']:
                user_choice = ord(answer) - ord('A')
                break
            else:
                print("❌ Please enter A, B, C, or D.")
        
        # Check if correct
        is_correct = user_choice == question['correct']
        correct_answer = question['options'][question['correct']]
        
        if is_correct:
            points = self.get_points(question.get('difficulty', 'medium'))
            self.score += points
            self.correct_answers += 1
            print(f"\n✅ Correct! +{points} points")
        else:
            print(f"\n❌ Incorrect. The correct answer was: {chr(65 + question['correct'])}. {correct_answer}")
        
        # Show explanation if available
        if 'explanation' in question:
            print(f"💡 {question['explanation']}")
        
        print(f"\nCurrent Score: {self.score}")
        
        # Small pause for better user experience
        time.sleep(2)
        
        return is_correct
    
    def display_final_results(self):
        """Display final quiz results and performance analysis."""
        print("\n" + "=" * 60)
        print("🏆 QUIZ COMPLETED! 🏆")
        print("=" * 60)
        
        accuracy = (self.correct_answers / self.total_questions) * 100 if self.total_questions > 0 else 0
        
        print(f"Player: {self.user_name}")
        print(f"Category: {self.current_category}")
        print(f"Difficulty: {self.current_difficulty.title()}")
        print(f"Questions Answered: {self.total_questions}")
        print(f"Correct Answers: {self.correct_answers}")
        print(f"Accuracy: {accuracy:.1f}%")
        print(f"Final Score: {self.score} points")
        
        # Performance evaluation
        print("\n" + "🎯 PERFORMANCE EVALUATION")
        print("-" * 40)
        
        if accuracy >= 90:
            grade = "A+ 🌟"
            message = "Outstanding! You're a quiz master!"
        elif accuracy >= 80:
            grade = "A 🎉"
            message = "Excellent work! You really know your stuff!"
        elif accuracy >= 70:
            grade = "B+ 👍"
            message = "Great job! You're doing well!"
        elif accuracy >= 60:
            grade = "B 👌"
            message = "Good effort! Keep practicing!"
        elif accuracy >= 50:
            grade = "C+ 💪"
            message = "Not bad! There's room for improvement!"
        else:
            grade = "C 📚"
            message = "Keep studying and try again!"
        
        print(f"Grade: {grade}")
        print(f"Message: {message}")
        
        # Save high score
        self.save_score()
    
    def save_score(self):
        """Save the score to a high scores file."""
        score_data = {
            "name": self.user_name,
            "score": self.score,
            "accuracy": (self.correct_answers / self.total_questions) * 100,
            "category": self.current_category,
            "difficulty": self.current_difficulty,
            "questions": self.total_questions,
            "correct": self.correct_answers,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        scores = []
        if os.path.exists('high_scores.json'):
            try:
                with open('high_scores.json', 'r') as f:
                    scores = json.load(f)
            except:
                scores = []
        
        scores.append(score_data)
        # Keep only top 10 scores
        scores.sort(key=lambda x: x['score'], reverse=True)
        scores = scores[:10]
        
        try:
            with open('high_scores.json', 'w') as f:
                json.dump(scores, f, indent=2)
            print("\n💾 Score saved to high scores!")
        except:
            print("\n❌ Could not save score.")
    
    def show_high_scores(self):
        """Display the high scores."""
        if not os.path.exists('high_scores.json'):
            print("\n📈 No high scores yet. Be the first to set a record!")
            return
        
        try:
            with open('high_scores.json', 'r') as f:
                scores = json.load(f)
        except:
            print("\n❌ Could not load high scores.")
            return
        
        if not scores:
            print("\n📈 No high scores yet. Be the first to set a record!")
            return
        
        print("\n" + "=" * 60)
        print("🏆 HIGH SCORES LEADERBOARD 🏆")
        print("=" * 60)
        
        for i, score in enumerate(scores, 1):
            print(f"{i:2d}. {score['name']:15s} - {score['score']:3d} pts "
                  f"({score['accuracy']:5.1f}%) - {score['category']} - {score['difficulty']}")
        
        print("=" * 60)
    
    def run_quiz(self):
        """Main quiz execution method."""
        # Get number of questions
        while True:
            try:
                num_questions = int(input(f"\nHow many questions would you like? (1-50, default 10): ") or "10")
                if 1 <= num_questions <= 50:
                    break
                else:
                    print("❌ Please enter a number between 1 and 50.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Get questions for the quiz
        questions = self.get_questions_for_quiz(self.current_category, self.current_difficulty, num_questions)
        
        if not questions:
            print("❌ No questions available for this selection. Please try different options.")
            return
        
        self.total_questions = len(questions)
        
        print(f"\n🎮 Starting quiz with {self.total_questions} questions!")
        print(f"📚 Category: {self.current_category}")
        print(f"⚡ Difficulty: {self.current_difficulty.title()}")
        
        input("\nPress Enter to start...")
        
        # Ask all questions
        for i, question in enumerate(questions, 1):
            self.ask_question(question, i, self.total_questions)
        
        # Show final results
        self.display_final_results()
    
    def main_menu(self):
        """Display main menu and handle user choices."""
        while True:
            print("\n" + "=" * 40)
            print("🎯 QUIZ GAME MAIN MENU")
            print("=" * 40)
            print("1. 🎮 Start New Quiz")
            print("2. 🏆 View High Scores")
            print("3. ❓ How to Play")
            print("4. 👋 Exit")
            
            choice = input("\nSelect an option (1-4): ").strip()
            
            if choice == "1":
                category = self.display_categories()
                difficulty = self.display_difficulties()
                self.run_quiz()
                
                # Ask if they want to play again
                while True:
                    play_again = input("\nWould you like to play again? (y/n): ").strip().lower()
                    if play_again in ['y', 'yes']:
                        # Reset scores for new game
                        self.score = 0
                        self.correct_answers = 0
                        self.total_questions = 0
                        break
                    elif play_again in ['n', 'no']:
                        return
                    else:
                        print("❌ Please enter 'y' for yes or 'n' for no.")
                        
            elif choice == "2":
                self.show_high_scores()
                
            elif choice == "3":
                self.show_how_to_play()
                
            elif choice == "4":
                print(f"\n👋 Thanks for playing, {self.user_name}! See you next time!")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-4.")
    
    def show_how_to_play(self):
        """Show game instructions."""
        print("\n" + "=" * 60)
        print("❓ HOW TO PLAY")
        print("=" * 60)
        print("🎯 Welcome to the Ultimate Quiz Game!")
        print()
        print("📝 GAME RULES:")
        print("• Choose a category or select 'Random Mix' for variety")
        print("• Pick your difficulty level (Easy, Medium, Hard, or Mixed)")
        print("• Answer multiple-choice questions by typing A, B, C, or D")
        print("• Earn points based on difficulty:")
        print("  - Easy questions: 1 point each")
        print("  - Medium questions: 2 points each") 
        print("  - Hard questions: 3 points each")
        print()
        print("🏆 SCORING:")
        print("• Your final score depends on correct answers and difficulty")
        print("• Accuracy percentage shows your performance")
        print("• High scores are saved automatically")
        print()
        print("💡 TIPS:")
        print("• Read questions carefully")
        print("• Explanations are provided after each answer")
        print("• Challenge yourself with harder difficulties for more points!")
        print("=" * 60)
    
    def run(self):
        """Main entry point for the quiz game."""
        try:
            self.display_welcome()
            self.main_menu()
        except KeyboardInterrupt:
            print(f"\n\n👋 Thanks for playing, {self.user_name}! See you next time!")
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please restart the game.")

if __name__ == "__main__":
    game = QuizGame()
    game.run()