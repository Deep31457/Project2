# 🎯 Ultimate Quiz Game

A comprehensive, interactive quiz game built in Python that allows users to test their knowledge across multiple categories and difficulty levels. Perfect for educational purposes, self-assessment, or just having fun!

## 🌟 Features

### Core Game Features
- **Multiple Categories**: General Knowledge, Science, History, Mathematics, Sports, and more
- **Difficulty Levels**: Easy (1 point), Medium (2 points), Hard (3 points), and Mixed
- **Interactive Interface**: User-friendly command-line interface with emojis and clear formatting
- **Scoring System**: Points-based scoring with performance evaluation and grading
- **High Scores**: Automatic leaderboard tracking with detailed statistics
- **Question Explanations**: Learn from detailed explanations after each answer

### Advanced Features
- **Random Mix Mode**: Questions from all categories for variety
- **Customizable Quiz Length**: Choose from 1-50 questions per session
- **Performance Analytics**: Accuracy percentage and grade evaluation
- **Question Management**: Add, view, edit, and delete questions easily
- **Data Persistence**: Scores and questions saved automatically
- **Import/Export**: Backup and share question databases

## 📁 Project Structure

```
quiz-game/
├── quiz_game.py          # Main game application
├── question_manager.py   # Question database management tool
├── questions.json        # Question database (auto-generated)
├── high_scores.json      # High scores leaderboard (auto-generated)
└── README.md            # This file
```

## 🚀 Quick Start

### Running the Quiz Game
```bash
python quiz_game.py
```

### Managing Questions
```bash
python question_manager.py
```

## 🎮 How to Play

1. **Start the Game**: Run `quiz_game.py` and enter your name
2. **Choose Category**: Select from available categories or "Random Mix"
3. **Select Difficulty**: Choose Easy, Medium, Hard, or Mixed
4. **Set Quiz Length**: Pick how many questions you want (1-50)
5. **Answer Questions**: Type A, B, C, or D for each multiple-choice question
6. **View Results**: See your score, accuracy, grade, and ranking

## 🏆 Scoring System

- **Easy Questions**: 1 point each 🟢
- **Medium Questions**: 2 points each 🟡
- **Hard Questions**: 3 points each 🔴

### Performance Grades
- **A+ (90-100%)**: Outstanding! You're a quiz master! 🌟
- **A (80-89%)**: Excellent work! You really know your stuff! 🎉
- **B+ (70-79%)**: Great job! You're doing well! 👍
- **B (60-69%)**: Good effort! Keep practicing! 👌
- **C+ (50-59%)**: Not bad! There's room for improvement! 💪
- **C (0-49%)**: Keep studying and try again! 📚

## 📊 Question Categories

### Current Categories
1. **General Knowledge** - World facts, geography, basic knowledge
2. **Science** - Biology, chemistry, physics, space
3. **History** - World events, famous people, dates
4. **Mathematics** - Basic math, algebra, calculations
5. **Sports** - Rules, records, famous athletes

### Difficulty Distribution
- **Easy**: Basic knowledge, common facts
- **Medium**: Intermediate level, some specialized knowledge
- **Hard**: Advanced topics, specific details

## 🛠️ Question Management

The `question_manager.py` tool provides comprehensive question database management:

### Features
- **Add Questions**: Interactive question creation with validation
- **View All Questions**: Browse entire database by category/difficulty
- **Statistics**: Analyze question distribution and balance
- **Delete Questions**: Remove unwanted questions safely
- **Import/Export**: Backup and restore question databases
- **New Categories**: Create custom categories easily

### Adding Custom Questions

1. Run the Question Manager:
   ```bash
   python question_manager.py
   ```

2. Select "Add New Question" and follow the prompts:
   - Choose or create a category
   - Select difficulty level
   - Enter question text
   - Provide 4 answer options
   - Specify correct answer
   - Add explanation (optional)

## 🎯 Game Modes

### Category Modes
- **Specific Category**: Focus on one subject area
- **Random Mix**: Questions from all categories for variety

### Difficulty Modes
- **Easy**: Perfect for beginners and casual learning
- **Medium**: Balanced challenge for most users
- **Hard**: Expert level for serious knowledge testing
- **Mixed**: All difficulty levels for comprehensive assessment

### Quiz Length Options
- **Quick (5-10 questions)**: Fast knowledge check
- **Standard (10-20 questions)**: Balanced quiz experience
- **Extended (20+ questions)**: Comprehensive testing session

## 📈 Educational Benefits

### Learning Features
- **Immediate Feedback**: Learn correct answers instantly
- **Detailed Explanations**: Understand concepts behind answers
- **Progress Tracking**: Monitor improvement over time
- **Category Focus**: Target specific knowledge areas
- **Difficulty Progression**: Gradually increase challenge level

### Use Cases
- **Self-Assessment**: Test your knowledge independently
- **Study Aid**: Reinforce learning with practice questions
- **Competition**: Challenge friends and family
- **Education**: Classroom tool for teachers and students
- **Training**: Corporate or professional knowledge testing

## 🔧 Customization

### Adding New Categories
Create questions in new subjects by using the Question Manager or manually editing `questions.json`:

```json
{
  "Your New Category": {
    "easy": [
      {
        "question": "Your question here?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct": 0,
        "explanation": "Your explanation here."
      }
    ],
    "medium": [],
    "hard": []
  }
}
```

### Modifying Game Settings
Edit `quiz_game.py` to customize:
- Point values for different difficulties
- Maximum number of questions
- Grade boundaries
- Display formats

## 🐛 Troubleshooting

### Common Issues

**Q: Game crashes when starting**
A: Ensure you're using Python 3.6+ and all files are in the same directory

**Q: Questions file not found**
A: The game will create default questions automatically. Use Question Manager to add more.

**Q: High scores not saving**
A: Check write permissions in the game directory

**Q: Emojis not displaying properly**
A: Use a modern terminal that supports Unicode characters

### Technical Requirements
- **Python**: 3.6 or higher
- **Dependencies**: Only standard library modules (json, random, time, os, typing)
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **Terminal**: Unicode support recommended for best experience

## 🎨 Interface Preview

```
============================================================
🎯 WELCOME TO THE ULTIMATE QUIZ GAME! 🎯
============================================================
Test your knowledge across different categories and difficulty levels!
Score points for correct answers and see how you rank!
------------------------------------------------------------

========================================
📚 AVAILABLE CATEGORIES
========================================
1. General Knowledge (8 questions)
2. Science (7 questions)
3. History (6 questions)
4. Mathematics (6 questions)
5. Sports (5 questions)
6. Random Mix (All categories)

============================================================
Question 1/10
============================================================
📝 What is the capital of France?

  A. London
  B. Berlin
  C. Paris
  D. Madrid

Your answer (A/B/C/D): C

✅ Correct! +1 points
💡 Paris is the capital and most populous city of France.

Current Score: 1
```

## 🤝 Contributing

Want to add more questions or improve the game? Here's how:

1. **Add Questions**: Use the Question Manager tool or edit `questions.json`
2. **Report Issues**: Submit bug reports or feature requests
3. **Suggest Categories**: Propose new subject areas
4. **Improve Code**: Enhance functionality or user experience

### Question Guidelines
- Keep questions clear and unambiguous
- Provide accurate and educational explanations
- Balance difficulty levels within categories
- Use proper grammar and spelling
- Avoid overly obscure or trivial topics

## 📜 License

This project is open source and available for educational and personal use.

---

🎯 **Ready to test your knowledge? Start the quiz game and see how much you really know!**