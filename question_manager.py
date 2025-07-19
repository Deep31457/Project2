import json
import os
from typing import Dict, List

class QuestionManager:
    def __init__(self):
        self.questions_file = 'questions.json'
        self.questions = self.load_questions()
    
    def load_questions(self) -> Dict:
        """Load questions from the JSON file."""
        if os.path.exists(self.questions_file):
            try:
                with open(self.questions_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading questions: {e}")
                return {}
        return {}
    
    def save_questions(self):
        """Save questions to the JSON file."""
        try:
            with open(self.questions_file, 'w') as f:
                json.dump(self.questions, f, indent=2)
            print("✅ Questions saved successfully!")
        except Exception as e:
            print(f"❌ Error saving questions: {e}")
    
    def add_question(self):
        """Interactive function to add a new question."""
        print("\n" + "=" * 50)
        print("📝 ADD NEW QUESTION")
        print("=" * 50)
        
        # Get category
        categories = list(self.questions.keys())
        print("\nExisting categories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        print(f"{len(categories) + 1}. Create new category")
        
        while True:
            try:
                choice = int(input(f"\nSelect category (1-{len(categories) + 1}): "))
                if 1 <= choice <= len(categories):
                    category = categories[choice - 1]
                    break
                elif choice == len(categories) + 1:
                    category = input("Enter new category name: ").strip()
                    if category:
                        if category not in self.questions:
                            self.questions[category] = {"easy": [], "medium": [], "hard": []}
                        break
                    else:
                        print("❌ Category name cannot be empty.")
                else:
                    print("❌ Invalid choice.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Get difficulty
        print("\nDifficulty levels:")
        difficulties = ["easy", "medium", "hard"]
        for i, diff in enumerate(difficulties, 1):
            print(f"{i}. {diff.title()}")
        
        while True:
            try:
                choice = int(input(f"\nSelect difficulty (1-{len(difficulties)}): "))
                if 1 <= choice <= len(difficulties):
                    difficulty = difficulties[choice - 1]
                    break
                else:
                    print("❌ Invalid choice.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Get question details
        question_text = input("\nEnter the question: ").strip()
        if not question_text:
            print("❌ Question cannot be empty.")
            return
        
        print("\nEnter 4 answer options:")
        options = []
        for i in range(4):
            option = input(f"Option {chr(65 + i)}: ").strip()
            if not option:
                print("❌ Option cannot be empty.")
                return
            options.append(option)
        
        while True:
            try:
                correct = input("\nWhich option is correct? (A/B/C/D): ").strip().upper()
                if correct in ['A', 'B', 'C', 'D']:
                    correct_index = ord(correct) - ord('A')
                    break
                else:
                    print("❌ Please enter A, B, C, or D.")
            except:
                print("❌ Please enter A, B, C, or D.")
        
        explanation = input("\nEnter explanation (optional): ").strip()
        
        # Create question object
        new_question = {
            "question": question_text,
            "options": options,
            "correct": correct_index,
            "explanation": explanation if explanation else f"The correct answer is {options[correct_index]}."
        }
        
        # Add to questions
        if category not in self.questions:
            self.questions[category] = {"easy": [], "medium": [], "hard": []}
        
        self.questions[category][difficulty].append(new_question)
        
        print(f"\n✅ Question added to {category} - {difficulty.title()}!")
        self.save_questions()
    
    def view_questions(self):
        """Display all questions organized by category and difficulty."""
        print("\n" + "=" * 60)
        print("📚 ALL QUESTIONS")
        print("=" * 60)
        
        for category, difficulties in self.questions.items():
            print(f"\n🏷️  {category.upper()}")
            print("-" * 40)
            
            for difficulty, questions in difficulties.items():
                if questions:
                    print(f"\n{difficulty.title()} ({len(questions)} questions):")
                    for i, q in enumerate(questions, 1):
                        print(f"  {i}. {q['question']}")
                        for j, option in enumerate(q['options']):
                            marker = "✓" if j == q['correct'] else " "
                            print(f"     {chr(65 + j)}. {option} {marker}")
                        if q.get('explanation'):
                            print(f"     💡 {q['explanation']}")
                        print()
    
    def view_statistics(self):
        """Display statistics about the question database."""
        print("\n" + "=" * 50)
        print("📊 QUESTION DATABASE STATISTICS")
        print("=" * 50)
        
        total_questions = 0
        category_stats = {}
        difficulty_stats = {"easy": 0, "medium": 0, "hard": 0}
        
        for category, difficulties in self.questions.items():
            category_total = 0
            for difficulty, questions in difficulties.items():
                count = len(questions)
                category_total += count
                difficulty_stats[difficulty] += count
                total_questions += count
            category_stats[category] = category_total
        
        print(f"Total Questions: {total_questions}")
        print(f"Total Categories: {len(self.questions)}")
        
        print("\n📚 Questions by Category:")
        for category, count in category_stats.items():
            percentage = (count / total_questions * 100) if total_questions > 0 else 0
            print(f"  {category}: {count} ({percentage:.1f}%)")
        
        print("\n⚡ Questions by Difficulty:")
        for difficulty, count in difficulty_stats.items():
            percentage = (count / total_questions * 100) if total_questions > 0 else 0
            print(f"  {difficulty.title()}: {count} ({percentage:.1f}%)")
        
        print("\n🎯 Recommendations:")
        if total_questions < 50:
            print("  • Consider adding more questions for a richer experience")
        
        # Find categories with few questions
        low_categories = [cat for cat, count in category_stats.items() if count < 5]
        if low_categories:
            print(f"  • Add more questions to: {', '.join(low_categories)}")
        
        # Check difficulty balance
        min_diff = min(difficulty_stats.values())
        max_diff = max(difficulty_stats.values())
        if max_diff > min_diff * 2:
            print("  • Consider balancing difficulty levels")
    
    def delete_question(self):
        """Interactive function to delete a question."""
        print("\n" + "=" * 50)
        print("🗑️  DELETE QUESTION")
        print("=" * 50)
        
        # Select category
        categories = list(self.questions.keys())
        if not categories:
            print("❌ No categories found.")
            return
        
        print("\nSelect category:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        
        while True:
            try:
                choice = int(input(f"\nSelect category (1-{len(categories)}): "))
                if 1 <= choice <= len(categories):
                    category = categories[choice - 1]
                    break
                else:
                    print("❌ Invalid choice.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Select difficulty
        difficulties = ["easy", "medium", "hard"]
        available_difficulties = [d for d in difficulties if self.questions[category][d]]
        
        if not available_difficulties:
            print(f"❌ No questions found in {category}.")
            return
        
        print(f"\nDifficulties in {category}:")
        for i, diff in enumerate(available_difficulties, 1):
            count = len(self.questions[category][diff])
            print(f"{i}. {diff.title()} ({count} questions)")
        
        while True:
            try:
                choice = int(input(f"\nSelect difficulty (1-{len(available_difficulties)}): "))
                if 1 <= choice <= len(available_difficulties):
                    difficulty = available_difficulties[choice - 1]
                    break
                else:
                    print("❌ Invalid choice.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Select question
        questions = self.questions[category][difficulty]
        print(f"\nQuestions in {category} - {difficulty.title()}:")
        for i, q in enumerate(questions, 1):
            print(f"{i}. {q['question'][:60]}{'...' if len(q['question']) > 60 else ''}")
        
        while True:
            try:
                choice = int(input(f"\nSelect question to delete (1-{len(questions)}): "))
                if 1 <= choice <= len(questions):
                    question_index = choice - 1
                    break
                else:
                    print("❌ Invalid choice.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Confirm deletion
        question_to_delete = questions[question_index]
        print(f"\n⚠️  Are you sure you want to delete this question?")
        print(f"Question: {question_to_delete['question']}")
        
        confirm = input("\nType 'yes' to confirm deletion: ").strip().lower()
        if confirm == 'yes':
            del self.questions[category][difficulty][question_index]
            print("✅ Question deleted successfully!")
            self.save_questions()
        else:
            print("❌ Deletion cancelled.")
    
    def main_menu(self):
        """Main menu for the question manager."""
        while True:
            print("\n" + "=" * 50)
            print("🛠️  QUIZ QUESTION MANAGER")
            print("=" * 50)
            print("1. 📝 Add New Question")
            print("2. 👀 View All Questions")
            print("3. 📊 View Statistics")
            print("4. 🗑️  Delete Question")
            print("5. 💾 Export Questions")
            print("6. 📁 Import Questions")
            print("7. 🚪 Exit")
            
            choice = input("\nSelect an option (1-7): ").strip()
            
            if choice == "1":
                self.add_question()
            elif choice == "2":
                self.view_questions()
            elif choice == "3":
                self.view_statistics()
            elif choice == "4":
                self.delete_question()
            elif choice == "5":
                self.export_questions()
            elif choice == "6":
                self.import_questions()
            elif choice == "7":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-7.")
    
    def export_questions(self):
        """Export questions to a backup file."""
        filename = input("\nEnter filename for export (e.g., backup.json): ").strip()
        if not filename:
            filename = f"questions_backup_{int(time.time())}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.questions, f, indent=2)
            print(f"✅ Questions exported to {filename}")
        except Exception as e:
            print(f"❌ Error exporting questions: {e}")
    
    def import_questions(self):
        """Import questions from a file."""
        filename = input("\nEnter filename to import from: ").strip()
        if not os.path.exists(filename):
            print("❌ File not found.")
            return
        
        try:
            with open(filename, 'r') as f:
                imported_questions = json.load(f)
            
            # Merge with existing questions
            for category, difficulties in imported_questions.items():
                if category not in self.questions:
                    self.questions[category] = {"easy": [], "medium": [], "hard": []}
                
                for difficulty, questions in difficulties.items():
                    if difficulty in ["easy", "medium", "hard"]:
                        self.questions[category][difficulty].extend(questions)
            
            self.save_questions()
            print("✅ Questions imported successfully!")
        except Exception as e:
            print(f"❌ Error importing questions: {e}")

if __name__ == "__main__":
    import time
    manager = QuestionManager()
    manager.main_menu()