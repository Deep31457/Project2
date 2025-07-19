from flask import Flask, render_template, request, jsonify, session
import json
import random
import os
from datetime import datetime
from quiz_game import QuizGame
from question_manager import QuestionManager

app = Flask(__name__)
app.secret_key = 'quiz_game_secret_key_2024'  # Change this in production

class WebQuizGame:
    def __init__(self):
        self.quiz_game = QuizGame()
        self.question_manager = QuestionManager()
        
    def get_categories(self):
        """Get available categories with question counts."""
        categories = []
        for category, difficulties in self.quiz_game.questions.items():
            question_count = sum(len(difficulties[diff]) for diff in difficulties)
            categories.append({
                'name': category,
                'count': question_count
            })
        return categories
    
    def get_quiz_questions(self, category, difficulty, num_questions):
        """Get questions for a quiz session."""
        questions = self.quiz_game.get_questions_for_quiz(category, difficulty, num_questions)
        
        # Format questions for frontend (remove correct answer)
        formatted_questions = []
        for i, q in enumerate(questions):
            formatted_questions.append({
                'id': i,
                'question': q['question'],
                'options': q['options'],
                'explanation': q.get('explanation', ''),
                'difficulty': q.get('difficulty', 'medium')
            })
        
        return formatted_questions, questions  # Return both formatted and original
    
    def calculate_score(self, answers, original_questions):
        """Calculate score based on answers."""
        score = 0
        correct_count = 0
        results = []
        
        for i, (answer, question) in enumerate(zip(answers, original_questions)):
            is_correct = answer == question['correct']
            points = self.quiz_game.get_points(question.get('difficulty', 'medium'))
            
            if is_correct:
                score += points
                correct_count += 1
            
            results.append({
                'question_id': i,
                'user_answer': answer,
                'correct_answer': question['correct'],
                'is_correct': is_correct,
                'points': points if is_correct else 0,
                'explanation': question.get('explanation', '')
            })
        
        accuracy = (correct_count / len(answers)) * 100 if answers else 0
        grade = self.get_grade(accuracy)
        
        return {
            'score': score,
            'correct_count': correct_count,
            'total_questions': len(answers),
            'accuracy': accuracy,
            'grade': grade,
            'results': results
        }
    
    def get_grade(self, accuracy):
        """Get grade based on accuracy."""
        if accuracy >= 90:
            return {"grade": "A+", "message": "Outstanding! You're a quiz master!", "emoji": "🌟"}
        elif accuracy >= 80:
            return {"grade": "A", "message": "Excellent work! You really know your stuff!", "emoji": "🎉"}
        elif accuracy >= 70:
            return {"grade": "B+", "message": "Great job! You're doing well!", "emoji": "👍"}
        elif accuracy >= 60:
            return {"grade": "B", "message": "Good effort! Keep practicing!", "emoji": "👌"}
        elif accuracy >= 50:
            return {"grade": "C+", "message": "Not bad! There's room for improvement!", "emoji": "💪"}
        else:
            return {"grade": "C", "message": "Keep studying and try again!", "emoji": "📚"}
    
    def save_high_score(self, name, score, accuracy, category, difficulty, questions_count, correct_count):
        """Save high score to the leaderboard."""
        score_data = {
            "name": name,
            "score": score,
            "accuracy": accuracy,
            "category": category,
            "difficulty": difficulty,
            "questions": questions_count,
            "correct": correct_count,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        scores = []
        if os.path.exists('high_scores.json'):
            try:
                with open('high_scores.json', 'r') as f:
                    scores = json.load(f)
            except:
                scores = []
        
        scores.append(score_data)
        scores.sort(key=lambda x: x['score'], reverse=True)
        scores = scores[:10]  # Keep top 10
        
        try:
            with open('high_scores.json', 'w') as f:
                json.dump(scores, f, indent=2)
            return True
        except:
            return False
    
    def get_high_scores(self):
        """Get high scores leaderboard."""
        if not os.path.exists('high_scores.json'):
            return []
        
        try:
            with open('high_scores.json', 'r') as f:
                return json.load(f)
        except:
            return []

# Initialize the web quiz game
web_quiz = WebQuizGame()

@app.route('/')
def home():
    """Serve the main quiz game page."""
    return render_template('index.html')

@app.route('/admin')
def admin():
    """Serve the admin panel for question management."""
    return render_template('admin.html')

@app.route('/api/categories')
def get_categories():
    """API endpoint to get available categories."""
    try:
        categories = web_quiz.get_categories()
        return jsonify({'success': True, 'categories': categories})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/start-quiz', methods=['POST'])
def start_quiz():
    """API endpoint to start a new quiz."""
    try:
        data = request.json
        category = data.get('category', 'General Knowledge')
        difficulty = data.get('difficulty', 'mixed')
        num_questions = data.get('num_questions', 10)
        player_name = data.get('player_name', 'Anonymous')
        
        # Get quiz questions
        formatted_questions, original_questions = web_quiz.get_quiz_questions(
            category, difficulty, num_questions
        )
        
        # Store original questions in session for scoring
        session['original_questions'] = original_questions
        session['quiz_config'] = {
            'category': category,
            'difficulty': difficulty,
            'player_name': player_name
        }
        
        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'quiz_id': session.get('quiz_id', 'default')
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/submit-quiz', methods=['POST'])
def submit_quiz():
    """API endpoint to submit quiz answers and get results."""
    try:
        data = request.json
        answers = data.get('answers', [])
        
        # Get original questions from session
        original_questions = session.get('original_questions', [])
        quiz_config = session.get('quiz_config', {})
        
        if not original_questions:
            return jsonify({'success': False, 'error': 'No active quiz session'})
        
        # Calculate results
        results = web_quiz.calculate_score(answers, original_questions)
        
        # Save high score
        web_quiz.save_high_score(
            quiz_config.get('player_name', 'Anonymous'),
            results['score'],
            results['accuracy'],
            quiz_config.get('category', 'Unknown'),
            quiz_config.get('difficulty', 'Unknown'),
            results['total_questions'],
            results['correct_count']
        )
        
        # Clear session
        session.pop('original_questions', None)
        session.pop('quiz_config', None)
        
        return jsonify({'success': True, 'results': results})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/high-scores')
def get_high_scores():
    """API endpoint to get high scores leaderboard."""
    try:
        scores = web_quiz.get_high_scores()
        return jsonify({'success': True, 'scores': scores})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/questions')
def get_all_questions():
    """API endpoint to get all questions for admin panel."""
    try:
        return jsonify({'success': True, 'questions': web_quiz.quiz_game.questions})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/add-question', methods=['POST'])
def add_question():
    """API endpoint to add a new question."""
    try:
        data = request.json
        category = data.get('category')
        difficulty = data.get('difficulty')
        question_text = data.get('question')
        options = data.get('options', [])
        correct_answer = data.get('correct_answer')
        explanation = data.get('explanation', '')
        
        # Validate input
        if not all([category, difficulty, question_text, len(options) == 4, correct_answer is not None]):
            return jsonify({'success': False, 'error': 'Missing required fields'})
        
        # Create question object
        new_question = {
            "question": question_text,
            "options": options,
            "correct": correct_answer,
            "explanation": explanation
        }
        
        # Add to questions
        if category not in web_quiz.quiz_game.questions:
            web_quiz.quiz_game.questions[category] = {"easy": [], "medium": [], "hard": []}
        
        web_quiz.quiz_game.questions[category][difficulty].append(new_question)
        
        # Save to file
        web_quiz.question_manager.questions = web_quiz.quiz_game.questions
        web_quiz.question_manager.save_questions()
        
        return jsonify({'success': True, 'message': 'Question added successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/delete-question', methods=['POST'])
def delete_question():
    """API endpoint to delete a question."""
    try:
        data = request.json
        category = data.get('category')
        difficulty = data.get('difficulty')
        question_index = data.get('question_index')
        
        if not all([category, difficulty, question_index is not None]):
            return jsonify({'success': False, 'error': 'Missing required fields'})
        
        # Delete question
        questions = web_quiz.quiz_game.questions[category][difficulty]
        if 0 <= question_index < len(questions):
            del questions[question_index]
            
            # Save to file
            web_quiz.question_manager.questions = web_quiz.quiz_game.questions
            web_quiz.question_manager.save_questions()
            
            return jsonify({'success': True, 'message': 'Question deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Invalid question index'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/stats')
def get_stats():
    """API endpoint to get question database statistics."""
    try:
        total_questions = 0
        category_stats = {}
        difficulty_stats = {"easy": 0, "medium": 0, "hard": 0}
        
        for category, difficulties in web_quiz.quiz_game.questions.items():
            category_total = 0
            for difficulty, questions in difficulties.items():
                count = len(questions)
                category_total += count
                if difficulty in difficulty_stats:
                    difficulty_stats[difficulty] += count
                total_questions += count
            category_stats[category] = category_total
        
        return jsonify({
            'success': True,
            'stats': {
                'total_questions': total_questions,
                'total_categories': len(web_quiz.quiz_game.questions),
                'category_stats': category_stats,
                'difficulty_stats': difficulty_stats
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)